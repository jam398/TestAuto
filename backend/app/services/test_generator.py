import json

from backend.app.models.schemas import (
    EvidenceSnippet,
    GenerateTestsRequest,
    GenerateTestsResponse,
    ProviderMode,
    TestCase,
    TestType,
    TestFramework,
)
from backend.app.services.chunking import TextChunk, chunk_text
from backend.app.services.evaluation import evaluate_generated_response, evaluation_warnings
from backend.app.services.llm_client import FakeLLMClient, LLMClient
from backend.app.services.prompt_builder import build_generation_prompt
from backend.app.services.vector_store import build_retrieval_query, retrieve_relevant_chunks


class GenerationError(RuntimeError):
    pass


HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}


def _first_evidence_snippets(chunks: list[TextChunk], limit: int = 3) -> list[EvidenceSnippet]:
    chunk_text_value = "\n".join(chunk.text for chunk in chunks)
    lines = [line.strip(" -*\t") for line in chunk_text_value.splitlines()]
    useful_lines = [line for line in lines if len(line) >= 12]
    snippets = useful_lines[:limit] or ([chunks[0].text[:160]] if chunks else [])
    return [EvidenceSnippet(snippet=snippet, source="project_context") for snippet in snippets]


def _extract_http_method_and_path(target_name: str) -> tuple[str, str]:
    parts = target_name.strip().split()
    if len(parts) >= 2 and parts[0].upper() in HTTP_METHODS and parts[1].startswith("/"):
        return parts[0].lower(), parts[1]
    if target_name.startswith("/"):
        return "post", target_name
    return "post", "/api/example"


def _pytest_code(target_name: str) -> str:
    method, path = _extract_http_method_and_path(target_name)
    return (
        "def test_generated_valid_request(client):\n"
        f"    response = client.{method}(\"{path}\", json={{\"example\": \"value\"}})\n\n"
        "    assert response.status_code in (200, 201)\n"
    )


def _jest_supertest_code(target_name: str) -> str:
    method, path = _extract_http_method_and_path(target_name)
    return (
        "it('accepts a valid request', async () => {\n"
        f"  const response = await request(app).{method}('{path}').send({{ example: 'value' }});\n\n"
        "  expect([200, 201]).toContain(response.status);\n"
        "});\n"
    )


def _mock_test_case_for_type(test_type: TestType) -> TestCase:
    cases = {
        TestType.API_ENDPOINT: TestCase(
            name="Valid endpoint request returns success",
            type=TestType.API_ENDPOINT,
            description="Checks that the documented endpoint accepts a valid request.",
            input="Valid request body using documented fields.",
            expected_result="Successful response matching the documented status code and body.",
            reason="API endpoint tests verify request and response behavior for the documented route.",
        ),
        TestType.VALIDATION: TestCase(
            name="Missing required field returns validation error",
            type=TestType.VALIDATION,
            description="Checks that missing required fields are rejected.",
            input="Request body missing one documented required field.",
            expected_result="Validation error response.",
            reason="Validation tests enforce required fields and input rules from the context.",
        ),
        TestType.NEGATIVE: TestCase(
            name="Invalid request body fails safely",
            type=TestType.NEGATIVE,
            description="Checks that invalid or malformed input is rejected without being accepted.",
            input="Bad request body with invalid field values.",
            expected_result="Client error response with useful error information.",
            reason="Negative tests verify bad input is handled safely.",
        ),
        TestType.EDGE_CASE: TestCase(
            name="Unusual allowed value is handled",
            type=TestType.EDGE_CASE,
            description="Checks an unusual but possible value implied by the context.",
            input="Unusual value such as zero, empty string, or maximum-like input when supported by context.",
            expected_result="Documented success or validation response depending on the rule.",
            reason="Edge case tests cover unusual values near expected behavior.",
        ),
        TestType.BOUNDARY: TestCase(
            name="Numeric boundary value is enforced",
            type=TestType.BOUNDARY,
            description="Checks exact numeric limits and just-outside values when limits are documented.",
            input="Boundary value such as 0, 100, below minimum, or above maximum.",
            expected_result="Documented success for allowed limits and validation error for outside limits.",
            reason="Boundary tests target exact minimum and maximum rules.",
        ),
        TestType.CONTRACT_SCHEMA: TestCase(
            name="Successful response matches documented schema",
            type=TestType.CONTRACT_SCHEMA,
            description="Checks that the response includes documented fields.",
            input="Valid request that produces a successful response.",
            expected_result="Response body contains the documented fields and structure.",
            reason="Contract/schema tests catch response shape changes.",
        ),
        TestType.ERROR_HANDLING: TestCase(
            name="Documented error response is clean",
            type=TestType.ERROR_HANDLING,
            description="Checks clean error behavior described by the context.",
            input="Request that triggers a documented error path.",
            expected_result="Documented error status and readable error body.",
            reason="Error handling tests verify failures return useful responses.",
        ),
        TestType.SMOKE: TestCase(
            name="Main documented behavior still works",
            type=TestType.SMOKE,
            description="Checks a small sanity path for the documented behavior.",
            input="Minimal valid request or documented health-style check.",
            expected_result="Basic success response.",
            reason="Smoke tests confirm important behavior has not obviously broken.",
        ),
        TestType.UNIT: TestCase(
            name="Function behavior is isolated",
            type=TestType.UNIT,
            description="Checks a small function or module behavior when function context is provided.",
            input="Representative function arguments from the context.",
            expected_result="Expected return value or exception described by the context.",
            reason="Unit tests are useful when the input context describes a function or module.",
        ),
        TestType.INTEGRATION: TestCase(
            name="Documented workflow works end to end",
            type=TestType.INTEGRATION,
            description="Checks multiple documented steps together when a workflow is provided.",
            input="Sequence of documented requests or service calls.",
            expected_result="Final state or response matches the documented workflow.",
            reason="Integration tests verify multiple parts working together when the context supports it.",
        ),
    }
    return cases[test_type]


def _validate_selected_type_alignment(response: GenerateTestsResponse, selected_test_types: list[TestType]) -> None:
    selected = set(selected_test_types)
    unselected = [test_case.type.value for test_case in response.test_cases if test_case.type not in selected]
    if unselected:
        raise GenerationError(f"LLM returned unselected test type(s): {', '.join(sorted(set(unselected)))}.")


def generate_mock_tests(request: GenerateTestsRequest) -> GenerateTestsResponse:
    target_name = request.target_name or "provided context"
    chunks = chunk_text(request.project_context)
    retrieval_query = build_retrieval_query(
        target_name=request.target_name,
        test_framework=request.test_framework.value,
        extra_instructions=request.extra_instructions,
    )
    retrieved = retrieve_relevant_chunks(chunks, query=retrieval_query, top_k=6)
    retrieved_chunks = [item.chunk for item in retrieved] or chunks[:3]
    prompt = build_generation_prompt(
        target_name=request.target_name,
        test_framework=request.test_framework,
        selected_test_types=request.selected_test_types,
        extra_instructions=request.extra_instructions,
        retrieved_chunks=retrieved_chunks,
    )
    FakeLLMClient(response="{}").generate(prompt)
    evidence = _first_evidence_snippets(retrieved_chunks)
    generated_code = (
        _jest_supertest_code(target_name)
        if request.test_framework == TestFramework.JEST_SUPERTEST
        else _pytest_code(target_name)
    )

    test_cases = [_mock_test_case_for_type(test_type) for test_type in request.selected_test_types]

    warnings = []
    if not retrieved:
        warnings.append("No relevant chunks were retrieved, so the mocked output used the first context chunks as fallback evidence.")
    warnings.append("This is deterministic mocked output because OpenAI generation is not active for this request.")

    return GenerateTestsResponse(
        provider_mode=ProviderMode.MOCK,
        selected_test_types=request.selected_test_types,
        summary=f"Generated mocked test plan for {target_name}.",
        test_cases=test_cases,
        generated_code=generated_code,
        evidence=evidence,
        warnings=warnings,
    )


def parse_llm_response(raw_response: str) -> GenerateTestsResponse:
    try:
        payload = json.loads(raw_response)
    except json.JSONDecodeError as exc:
        raise GenerationError("LLM returned invalid JSON.") from exc

    try:
        return GenerateTestsResponse.model_validate(payload)
    except ValueError as exc:
        raise GenerationError("LLM JSON did not match the expected response schema.") from exc


def build_repair_prompt(original_prompt: str, invalid_response: str, error: Exception) -> str:
    return (
        f"{original_prompt}\n\n"
        "The previous response was invalid. Return only valid JSON matching the required schema.\n"
        f"Validation error: {error}\n"
        f"Invalid response:\n{invalid_response}"
    )


def generate_tests_with_llm(request: GenerateTestsRequest, llm_client: LLMClient) -> GenerateTestsResponse:
    chunks = chunk_text(request.project_context)
    retrieval_query = build_retrieval_query(
        target_name=request.target_name,
        test_framework=request.test_framework.value,
        extra_instructions=request.extra_instructions,
    )
    retrieved = retrieve_relevant_chunks(chunks, query=retrieval_query, top_k=6)
    retrieved_chunks = [item.chunk for item in retrieved] or chunks[:3]
    prompt = build_generation_prompt(
        target_name=request.target_name,
        test_framework=request.test_framework,
        selected_test_types=request.selected_test_types,
        extra_instructions=request.extra_instructions,
        retrieved_chunks=retrieved_chunks,
    )

    raw_response = llm_client.generate(prompt)
    try:
        response = parse_llm_response(raw_response)
        _validate_selected_type_alignment(response, request.selected_test_types)
    except GenerationError as first_error:
        repair_prompt = build_repair_prompt(prompt, raw_response, first_error)
        repaired_response = llm_client.generate(repair_prompt)
        response = parse_llm_response(repaired_response)
        _validate_selected_type_alignment(response, request.selected_test_types)

    warnings = [*response.warnings, *evaluation_warnings(evaluate_generated_response(response, request.project_context))]
    return response.model_copy(
        update={
            "provider_mode": ProviderMode.OPENAI,
            "selected_test_types": request.selected_test_types,
            "warnings": warnings,
        }
    )

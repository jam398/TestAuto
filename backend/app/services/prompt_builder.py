from __future__ import annotations

from app.models.schemas import TestFramework, TestType
from app.services.chunking import TextChunk


def format_retrieved_context(chunks: list[TextChunk]) -> str:
    if not chunks:
        return "No retrieved context was available."

    formatted: list[str] = []
    for chunk in chunks:
        source = chunk.metadata.get("source", "project_context")
        index = chunk.metadata.get("chunk_index", "unknown")
        formatted.append(f"[source={source} chunk={index}]\n{chunk.text}")
    return "\n\n".join(formatted)


TEST_TYPE_DEFINITIONS: dict[TestType, str] = {
    TestType.API_ENDPOINT: "API Endpoint Tests: test HTTP request/response behavior.",
    TestType.VALIDATION: "Validation Tests: test required fields, data types, formats, and constraints.",
    TestType.NEGATIVE: "Negative Tests: test invalid or bad input.",
    TestType.EDGE_CASE: "Edge Case Tests: test unusual but possible values.",
    TestType.BOUNDARY: "Boundary Tests: test exact limits and just-outside limits.",
    TestType.CONTRACT_SCHEMA: "Contract / Schema Tests: test expected response structure.",
    TestType.ERROR_HANDLING: "Error Handling Tests: test clean failure behavior.",
    TestType.SMOKE: "Smoke Tests: test basic sanity checks.",
    TestType.UNIT: "Unit Tests: test one function or module in isolation.",
    TestType.INTEGRATION: "Integration Tests: test multiple parts working together.",
}


def format_selected_test_types(selected_test_types: list[TestType]) -> str:
    return "\n".join(f"- {test_type.value}: {TEST_TYPE_DEFINITIONS[test_type]}" for test_type in selected_test_types)


def format_all_test_type_definitions() -> str:
    return "\n".join(f"- {definition}" for definition in TEST_TYPE_DEFINITIONS.values())


def build_generation_prompt(
    *,
    target_name: str | None,
    test_framework: TestFramework,
    selected_test_types: list[TestType],
    extra_instructions: str | None,
    retrieved_chunks: list[TextChunk],
) -> str:
    target = target_name or "Not specified"
    instructions = extra_instructions or "None provided"
    retrieved_context = format_retrieved_context(retrieved_chunks)

    return f"""You are TestPilot AI, a software testing assistant.

Your task is to generate useful test cases for a backend API, function, or software module.

Use only the provided project context and retrieved evidence.
Do not invent behavior that is not supported by the context.
If important information is missing, add a warning instead of making it up.
If likely status codes are suggested without explicit context, mark them as assumptions.
Do not generate authentication tests unless authentication behavior appears in the context.
Return valid JSON matching the GenerateTestsResponse schema.
The generated_code field must contain non-empty starter test code in the selected framework.

Target:
{target}

Target precedence:
If the target is specified, treat it as the principal API, function, or module to test.
Additional instructions may add focus or constraints, but they must not override or replace the specified target.
If additional instructions mention a different target, keep the specified target as primary and add a warning about the conflict.
If the target is not specified, infer the most relevant target only from the provided project context and retrieved evidence.

Test framework:
{test_framework.value}

The user selected these test types:
{format_selected_test_types(selected_test_types)}

Only generate test cases that match these selected types. If a selected type is not supported by the provided context, explain that in warnings.
Do not generate test cases for unselected test types.
Do not invent behavior that is not described in the context.

Definitions:
{format_all_test_type_definitions()}

Extra instructions:
{instructions}

Retrieved context:
{retrieved_context}

Return JSON with:
- provider_mode
- selected_test_types
- summary
- test_cases
- generated_code
- evidence
- warnings

Set provider_mode to "openai".
Set selected_test_types to exactly the selected enum values listed above.
Set generated_code to starter test code, not an empty string.
"""

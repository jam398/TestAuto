import pytest
from pydantic import ValidationError

from app.models.schemas import (
    EvidenceSnippet,
    GenerateTestsRequest,
    GenerateTestsResponse,
    ProviderMode,
    TestCase,
    TestCaseType,
    TestType,
    TestFramework,
)
from app.services.llm_client import FakeLLMClient
from app.services.test_generator import GenerationError, generate_tests_with_llm, parse_llm_response


def test_request_defaults_framework_to_pytest():
    request = GenerateTestsRequest(
        project_context="POST /api/debts creates a debt record with required validation fields."
    )

    assert request.test_framework == TestFramework.PYTEST
    assert request.selected_test_types == [
        TestType.API_ENDPOINT,
        TestType.VALIDATION,
        TestType.NEGATIVE,
        TestType.EDGE_CASE,
        TestType.CONTRACT_SCHEMA,
    ]


def test_request_accepts_valid_selected_test_types():
    request = GenerateTestsRequest(
        project_context="POST /api/debts creates a debt record with required validation fields.",
        selected_test_types=["validation", "boundary", "contract_schema"],
    )

    assert request.selected_test_types == [TestType.VALIDATION, TestType.BOUNDARY, TestType.CONTRACT_SCHEMA]


def test_request_defaults_empty_selected_test_types():
    request = GenerateTestsRequest(
        project_context="POST /api/debts creates a debt record with required validation fields.",
        selected_test_types=[],
    )

    assert request.selected_test_types == [
        TestType.API_ENDPOINT,
        TestType.VALIDATION,
        TestType.NEGATIVE,
        TestType.EDGE_CASE,
        TestType.CONTRACT_SCHEMA,
    ]


def test_request_rejects_invalid_selected_test_type():
    with pytest.raises(ValidationError):
        GenerateTestsRequest(
            project_context="POST /api/debts creates a debt record with required validation fields.",
            selected_test_types=["security"],
        )


def test_request_strips_optional_text():
    request = GenerateTestsRequest(
        project_context="POST /api/debts creates a debt record with required validation fields.",
        target_name="  POST /api/debts  ",
        extra_instructions="  Focus on validation.  ",
    )

    assert request.target_name == "POST /api/debts"
    assert request.extra_instructions == "Focus on validation."


def test_request_rejects_empty_context_after_trim():
    with pytest.raises(ValidationError):
        GenerateTestsRequest(project_context=" " * 40)


def test_response_schema_accepts_valid_payload():
    response = GenerateTestsResponse(
        provider_mode=ProviderMode.MOCK,
        selected_test_types=[TestType.API_ENDPOINT],
        summary="Generated mocked test plan.",
        test_cases=[
            TestCase(
                name="Accepts valid request",
                type=TestType.API_ENDPOINT,
                description="Checks valid input.",
                input="name=Credit Card",
                expected_result="201 Created",
                reason="Confirms the happy path.",
            )
        ],
        generated_code="def test_example():\n    assert True\n",
        evidence=[EvidenceSnippet(snippet="principal: number greater than 0", source="project_context")],
        warnings=[],
    )

    assert response.test_cases[0].type == TestType.API_ENDPOINT
    assert response.evidence[0].source == "project_context"


def test_response_schema_rejects_missing_required_fields():
    with pytest.raises(ValidationError):
        GenerateTestsResponse(
            provider_mode=ProviderMode.MOCK,
            selected_test_types=[TestType.API_ENDPOINT],
            summary="Generated mocked test plan.",
            test_cases=[],
            evidence=[],
            warnings=[],
        )


def test_response_schema_rejects_blank_generated_code():
    with pytest.raises(ValidationError):
        GenerateTestsResponse(
            provider_mode=ProviderMode.MOCK,
            selected_test_types=[TestType.API_ENDPOINT],
            summary="Generated mocked test plan.",
            test_cases=[],
            generated_code="   ",
            evidence=[],
            warnings=[],
        )


def test_parse_llm_response_accepts_valid_json():
    response = parse_llm_response(
        """
        {
          "provider_mode": "openai",
          "selected_test_types": ["api_endpoint"],
          "summary": "Generated plan.",
          "test_cases": [],
          "generated_code": "def test_example(): pass",
          "evidence": [],
          "warnings": []
        }
        """
    )

    assert response.summary == "Generated plan."


def test_parse_llm_response_rejects_invalid_json():
    with pytest.raises(GenerationError):
        parse_llm_response("not json")


def test_parse_llm_response_rejects_blank_generated_code():
    with pytest.raises(GenerationError):
        parse_llm_response(
            """
            {
              "provider_mode": "openai",
              "selected_test_types": ["api_endpoint"],
              "summary": "Generated plan.",
              "test_cases": [],
              "generated_code": "",
              "evidence": [],
              "warnings": []
            }
            """
        )


def test_generate_tests_with_llm_repairs_once_after_invalid_json():
    valid_json = """
    {
      "provider_mode": "openai",
      "selected_test_types": ["api_endpoint", "validation"],
      "summary": "Generated plan mentioning principal APR 100.",
      "test_cases": [
        {
          "name": "Creates valid debt",
          "type": "api_endpoint",
          "description": "Valid principal and APR.",
          "input": "principal=100, apr=10",
          "expected_result": "201 Created",
          "reason": "Covers principal and APR between 0 and 100."
        },
        {
          "name": "Rejects APR above 100",
          "type": "validation",
          "description": "APR above 100 is invalid.",
          "input": "apr=101",
          "expected_result": "400 Bad Request",
          "reason": "APR must be between 0 and 100."
        }
      ],
      "generated_code": "def test_apr_above_100(): pass",
      "evidence": [{"snippet": "apr: number between 0 and 100", "source": "project_context"}],
      "warnings": []
    }
    """
    client = FakeLLMClient(response="not json")
    client_responses = iter(["not json", valid_json])
    client.generate = lambda prompt: next(client_responses)
    request = GenerateTestsRequest(
        project_context="POST /api/debts creates debt. principal greater than 0. apr between 0 and 100."
    )

    response = generate_tests_with_llm(request, client)

    assert response.summary.startswith("Generated plan")
    assert response.provider_mode == ProviderMode.OPENAI
    assert response.selected_test_types == [
        TestType.API_ENDPOINT,
        TestType.VALIDATION,
        TestType.NEGATIVE,
        TestType.EDGE_CASE,
        TestType.CONTRACT_SCHEMA,
    ]

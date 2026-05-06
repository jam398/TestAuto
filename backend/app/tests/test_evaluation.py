from pathlib import Path

import pytest
from pydantic import ValidationError

from backend.app.models.schemas import EvidenceSnippet, GenerateTestsResponse, ProviderMode, TestCase, TestType
from backend.app.services.evaluation import evaluate_generated_response, evaluation_warnings


DEBT_CONTEXT = """
POST /api/debts creates a debt record.
Required fields:
name: string
principal: number greater than 0
apr: number between 0 and 100
minimumPayment: number greater than 0
"""


def test_debt_fixture_exists_and_contains_clean_context():
    fixture = Path(__file__).parent / "fixtures" / "debt_api_context.txt"
    content = fixture.read_text(encoding="utf-8")

    assert "POST /api/debts" in content
    assert "principal: number, must be greater than 0" in content
    assert "apr: number, must be between 0 and 100" in content


def _response(test_cases: list[TestCase], generated_code: str = "def test_example(): pass") -> GenerateTestsResponse:
    return GenerateTestsResponse(
        provider_mode=ProviderMode.MOCK,
        selected_test_types=[TestType.API_ENDPOINT, TestType.VALIDATION],
        summary="Generated API test plan for POST /api/debts.",
        test_cases=test_cases,
        generated_code=generated_code,
        evidence=[EvidenceSnippet(snippet="principal: number greater than 0", source="project_context")],
        warnings=[],
    )


def test_evaluation_passes_for_context_coverage():
    response = _response(
        [
            TestCase(
                name="Creates valid debt",
                type=TestType.API_ENDPOINT,
                description="Valid principal and APR.",
                input="principal=100, apr=10",
                expected_result="201 Created",
                reason="Covers principal and APR between 0 and 100.",
            ),
            TestCase(
                name="Rejects APR above 100",
                type=TestType.VALIDATION,
                description="APR above 100 is invalid.",
                input="apr=101",
                expected_result="400 Bad Request",
                reason="APR must be between 0 and 100.",
            ),
        ]
    )

    results = evaluate_generated_response(response, DEBT_CONTEXT)

    assert all(result.passed for result in results)


def test_evaluation_warnings_reports_missing_coverage():
    response = _response(
        [
            TestCase(
                name="Creates valid debt",
                type=TestType.API_ENDPOINT,
                description="Valid request.",
                input="valid request",
                expected_result="201 Created",
                reason="Covers happy path.",
            )
        ]
    )

    warnings = evaluation_warnings(evaluate_generated_response(response, DEBT_CONTEXT))

    assert "Includes selected test type: validation." in warnings
    assert "Mentions APR constraints when APR appears in context." in warnings
    assert "Mentions principal constraints when principal appears in context." in warnings


def test_response_validation_rejects_empty_generated_code_before_evaluation():
    with pytest.raises(ValidationError):
        _response([], generated_code="")


def test_evaluation_warns_for_unselected_generated_type():
    response = _response(
        [
            TestCase(
                name="Creates valid debt",
                type=TestType.API_ENDPOINT,
                description="Valid request.",
                input="valid request",
                expected_result="201 Created",
                reason="Covers happy path.",
            ),
            TestCase(
                name="APR boundary",
                type=TestType.BOUNDARY,
                description="Boundary request.",
                input="apr=101",
                expected_result="400 Bad Request",
                reason="APR must be between 0 and 100.",
            ),
        ]
    )

    warnings = evaluation_warnings(evaluate_generated_response(response, DEBT_CONTEXT))

    assert "Only includes selected test types." in warnings

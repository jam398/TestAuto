from __future__ import annotations

from dataclasses import dataclass

from backend.app.models.schemas import GenerateTestsResponse


@dataclass(frozen=True)
class EvaluationResult:
    name: str
    passed: bool
    message: str


def evaluate_generated_response(response: GenerateTestsResponse, project_context: str) -> list[EvaluationResult]:
    combined_output = " ".join(
        [
            response.summary,
            response.generated_code,
            " ".join(test_case.name for test_case in response.test_cases),
            " ".join(test_case.description for test_case in response.test_cases),
            " ".join(test_case.expected_result for test_case in response.test_cases),
            " ".join(test_case.reason for test_case in response.test_cases),
        ]
    ).lower()
    context_lower = project_context.lower()

    selected_types = set(response.selected_test_types)
    generated_types = {test_case.type for test_case in response.test_cases}
    has_evidence = bool(response.evidence)
    has_code = bool(response.generated_code.strip())
    mentions_apr_constraint = "apr" not in context_lower or ("apr" in combined_output and "100" in combined_output)
    mentions_principal_constraint = "principal" not in context_lower or "principal" in combined_output
    has_only_selected_types = generated_types.issubset(selected_types)

    results = [
        EvaluationResult("only_selected_types", has_only_selected_types, "Only includes selected test types."),
        EvaluationResult("evidence", has_evidence, "Includes evidence snippets."),
        EvaluationResult("generated_code", has_code, "Includes generated starter code."),
        EvaluationResult("apr_constraint", mentions_apr_constraint, "Mentions APR constraints when APR appears in context."),
        EvaluationResult(
            "principal_constraint",
            mentions_principal_constraint,
            "Mentions principal constraints when principal appears in context.",
        ),
    ]
    for test_type in response.selected_test_types:
        results.append(
            EvaluationResult(
                f"selected_type_{test_type.value}",
                test_type in generated_types,
                f"Includes selected test type: {test_type.value}.",
            )
        )
    return results


def evaluation_warnings(results: list[EvaluationResult]) -> list[str]:
    return [result.message for result in results if not result.passed]

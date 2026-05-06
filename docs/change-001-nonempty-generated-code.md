# Change Note: Nonempty Generated Code

## Metadata

- **ID:** CHANGE-001
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This is a narrow, directly verifiable bug fix for one response field and its prompt/test coverage. It does not change product scope, architecture, or workflow direction.

## Reason For Change

OpenAI mode can return an empty `generated_code` string while still satisfying the current required-field schema. The frontend renders the starter code block correctly, but there is no code to display.

## Scope

In scope:

- Reject blank `generated_code` values during response validation.
- Strengthen the generation prompt so starter code is always requested.
- Add tests for blank generated code rejection.

Out of scope:

- Executing generated tests.
- Adding full code quality evaluation.
- Changing frontend rendering.

## Files Expected To Change

- `backend/app/models/schemas.py`
- `backend/app/services/prompt_builder.py`
- `backend/app/tests/test_schema_validation.py`
- `docs/change-001-nonempty-generated-code.md`

## Change Summary

Completed. `GenerateTestsResponse.generated_code` now rejects empty or whitespace-only code. The prompt explicitly requires starter test code in the selected framework.

## Risk Level

- **Risk:** Low
- **Reason:** The change tightens an existing required field and uses the existing LLM repair path when a provider returns invalid output.

## Verification

- `python -m pytest backend/app/tests/test_schema_validation.py backend/app/tests/test_prompt_builder.py backend/app/tests/test_api_generate_tests.py`
- `python -m pytest backend/app/tests`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Checks Performed:** Added schema and parser tests for blank `generated_code`, updated prompt assertions for non-empty starter code, ran focused backend tests, and ran the full backend suite.
- **Result:** PASS. `python -m pytest backend/app/tests/test_schema_validation.py backend/app/tests/test_prompt_builder.py backend/app/tests/test_api_generate_tests.py` passed with 29 tests. `python -m pytest backend/app/tests` passed with 54 tests.
- **Carry-Forward Notes:** Real OpenAI responses that return blank `generated_code` will now use the existing repair path. If the repaired response is still blank, the request will fail instead of rendering an empty code block.

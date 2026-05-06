# Spec: Selected Test Type Controls

## Metadata

- **ID:** SPEC-007
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** SPEC-002, SPEC-003, SPEC-004
- **Related Sprints:** SPRINT-010

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** First-class selected test types affect product behavior, backend request and response schemas, prompt logic, AI output validation, frontend controls, result display, README documentation, and automated tests.

## Problem Statement

Before SPRINT-010, TestPilot AI let users influence test focus through free-form `extra_instructions` and frontend-only scenario group chips. That helped, but it did not give the backend or prompt builder a first-class, validated list of requested test types. Users should be able to choose the exact kinds of tests they want generated, with useful defaults, while still keeping additional free-form instructions.

## Goals

- Add first-class selected test types to the backend request schema.
- Add selected test types to the backend response schema.
- Replace the SPRINT-009 scenario group chips with a compact multi-select dropdown containing the supported test types.
- Preselect the MVP default test types.
- Preserve the additional instructions field.
- Include selected test types and definitions in the AI prompt.
- Ensure generated test cases are labeled by the selected test type values.
- Reject unknown test type values.
- Document only the supported test types in the README.

## Non-Goals

- Authentication tests.
- Authorization tests.
- Mocked dependency tests.
- Regression tests.
- Performance tests.
- Security tests.
- Disabled, future, advanced, or unavailable test types in the UI.
- Persisting user selections or custom presets.
- Executing generated tests.
- Reintroducing free-form object schemas that break OpenAI strict structured outputs.

## Current State

Verified after SPRINT-010 implementation on 2026-05-04:

- `frontend/src/components/TestGeneratorForm.tsx` renders a selected test type dropdown and keeps additional instructions.
- `GenerateTestsRequest` accepts `project_context`, `target_name`, `test_framework`, `selected_test_types`, and `extra_instructions`.
- `GenerateTestsResponse` includes `provider_mode`, `selected_test_types`, `summary`, `test_cases`, `generated_code`, `evidence`, and `warnings`.
- `TestCase.type` uses the supported selected test type enum values.
- `TestCase.input` remains a string to keep the OpenAI strict structured-output schema valid.
- `docs/references/letter2.md` defined the requested selected test type feature and was read for this spec.

## Proposed Approach

1. Introduce a shared test type enum with exactly the supported values from `letter2.md`.
2. Add `selected_test_types` to `GenerateTestsRequest`.
3. Apply defaults when `selected_test_types` is missing or empty.
4. Add `selected_test_types` to `GenerateTestsResponse`.
5. Update `TestCase.type` to use the selected test type enum values instead of the old broad categories.
6. Keep `TestCase.input` as a string even though `letter2.md` shows an object, because OpenAI strict structured outputs rejected arbitrary object schemas in prior verified implementation.
7. Replace frontend scenario chips with a dropdown multi-select checkbox control.
8. Keep the additional instructions textarea below the test type selector.
9. Include selected test types and definitions in the prompt, with explicit instructions to generate only selected types and warn when a selected type is unsupported by context.
10. Update mock generation, evaluation, README, and automated tests.

## Architecture / Data / Flow Notes

Supported UI labels and enum values:

| UI Label | Enum Value | Default |
|---|---|---|
| API Endpoint Tests | `api_endpoint` | Yes |
| Validation Tests | `validation` | Yes |
| Negative Tests | `negative` | Yes |
| Edge Case Tests | `edge_case` | Yes |
| Boundary Tests | `boundary` | No |
| Contract / Schema Tests | `contract_schema` | Yes |
| Error Handling Tests | `error_handling` | No |
| Smoke Tests | `smoke` | No |
| Unit Tests | `unit` | No |
| Integration Tests | `integration` | No |

Default selected test types:

```text
api_endpoint
validation
negative
edge_case
contract_schema
```

Request shape:

```json
{
  "project_context": "POST /api/debts creates a debt record...",
  "target_name": "POST /api/debts",
  "test_framework": "pytest",
  "selected_test_types": [
    "api_endpoint",
    "validation",
    "negative",
    "edge_case",
    "contract_schema"
  ],
  "extra_instructions": "Focus on validation and negative tests."
}
```

Response shape:

```json
{
  "provider_mode": "openai",
  "selected_test_types": [
    "api_endpoint",
    "validation",
    "negative",
    "edge_case",
    "contract_schema"
  ],
  "summary": "Generated API test plan for POST /api/debts.",
  "test_cases": [],
  "generated_code": "",
  "evidence": [],
  "warnings": []
}
```

Required prompt language:

```text
The user selected these test types:
{selected_test_types}

Only generate test cases that match these selected types. If a selected type is not supported by the provided context, explain that in warnings. Do not invent behavior that is not described in the context.
```

Prompt definitions:

- API Endpoint Tests: test HTTP request/response behavior.
- Validation Tests: test required fields, data types, formats, and constraints.
- Negative Tests: test invalid or bad input.
- Edge Case Tests: test unusual but possible values.
- Boundary Tests: test exact limits and just-outside limits.
- Contract / Schema Tests: test expected response structure.
- Error Handling Tests: test clean failure behavior.
- Smoke Tests: test basic sanity checks.
- Unit Tests: test one function or module in isolation.
- Integration Tests: test multiple parts working together.

## Invariants

- The app must not execute user-submitted code.
- The app must not execute generated tests.
- Only the 10 supported test types may appear in request validation, prompt definitions, frontend controls, README docs, and generated response schemas.
- Unknown selected test type values must be rejected.
- Missing or empty selected test types must use the default list.
- The model must be instructed not to generate unselected test types.
- If selected test types cannot be supported from the provided context, the response must use warnings instead of invented behavior.
- The additional instructions textarea must remain available.
- Strict structured output compatibility must be preserved.
- `TestCase.input` remains a string unless a later verified schema design safely supports structured inputs.

## Risks

- The old scenario chip controls and new test type dropdown could overlap if both are kept.
- Changing `TestCase.type` can break frontend badges, evaluation tests, and mock output if not updated together.
- The model may still generate unsupported selected types if the prompt is weak.
- OpenAI strict schema validation may reject schema changes if defaults or arbitrary object shapes are introduced.
- A dropdown with 10 choices can become cramped on mobile if not styled carefully.

## Verification Strategy

- Backend schema tests:
  - valid selected test types are accepted
  - invalid selected test types are rejected
  - missing `selected_test_types` uses defaults
  - empty `selected_test_types` uses defaults
- Prompt builder tests:
  - selected test types appear in the prompt
  - test type definitions appear in the prompt
  - the prompt says not to invent unsupported behavior
  - the prompt says not to generate unselected types
- API tests:
  - request with selected test types returns them in response
  - request without selected test types uses defaults
  - invalid selected type returns validation error
- Evaluation/mock tests:
  - debt fixture produces default categories in mock mode
  - boundary tests appear only when `boundary` is selected
  - contract/schema tests are present when selected and response fields exist in context
- Frontend checks:
  - build and lint pass
  - dropdown renders all 10 types
  - defaults are selected
  - user can select/deselect types
  - selected types are sent in request payload
  - additional instructions remain editable and submitted
  - mobile layout has no overflow
- README/documentation review:
  - only the supported test types are documented
  - no future/disabled/advanced test types are listed

## Sprint Plan

1. SPRINT-010: Implement selected test type request/response contracts, prompt logic, frontend dropdown, docs, and verification.

## Rollout / Sequencing Notes

SPRINT-010 replaced the SPRINT-009 scenario group chips. Do not reintroduce both controls in the user-facing form. The scenario chips from SPRINT-009 remain useful as proof of the user-control direction but are superseded by this first-class selected test type feature.

## Completion Criteria

- Frontend lets users select from exactly the 10 supported test types.
- Defaults are selected on initial load.
- Backend accepts and validates `selected_test_types`.
- Missing or empty selected types use the default list.
- Invalid selected types are rejected.
- Prompt includes selected test types and definitions.
- Response includes `selected_test_types`.
- Each generated test case is labeled by one of the selected test type enum values.
- README documents only the supported test types.
- Automated backend and frontend tests pass.
- Browser checks pass on desktop and mobile.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-007
- **Spec ID:** SPEC-007
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-007-selected-test-type-controls.md`

### QA Scope

This QA pass reviewed:

- problem statement quality
- goal and non-goal clarity
- current-state accuracy
- proposed approach coherence
- risk and invariant coverage
- verification completeness

### Checks Performed

- [x] Read the full spec
- [x] Compared claims against the live repository where applicable
- [x] Checked for ambiguity, contradictions, and missing requirements
- [x] Checked whether risks, invariants, and verification are concrete
- [x] Checked sprint sequencing if present

### Findings

None.

### Open Questions

- None.

### Final QA Summary

- **What was checked:** Selected test type scope, request/response contracts, prompt requirements, frontend UX direction, strict schema constraints, and verification plan.
- **What was fixed:** The spec explicitly resolves the `letter2.md` object-input example by keeping `TestCase.input` as a string for strict structured-output compatibility.
- **Residual risks:** Prompt compliance still needs implementation-time verification with mocked and real provider paths.
- **Recommendation:** Ready.

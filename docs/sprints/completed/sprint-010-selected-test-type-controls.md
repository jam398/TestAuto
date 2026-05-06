# Sprint: Selected Test Type Controls

## Metadata

- **ID:** SPRINT-010
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** SPEC-007 governs a cross-cutting request/response contract, prompt, backend tests, frontend UX, and README change.

## Goal

Implement first-class selected test type controls so users can choose exactly which supported test categories guide generation.

## Governing Spec

`docs/specs/spec-007-selected-test-type-controls.md`

## Carry-Forward Context

SPRINT-009 added frontend-only scenario chips that compose text into `extra_instructions`. SPEC-007 supersedes that UX with first-class selected test types sent to the backend as structured data. Additional instructions must remain available.

## Scope

In scope:

- Backend `selected_test_types` request validation.
- Backend `selected_test_types` response field.
- Test type enum values matching SPEC-007 exactly.
- Prompt builder selected type section and definitions.
- Mock generation aligned to selected types.
- Evaluation updates for selected type behavior.
- Frontend dropdown multi-select with checkboxes.
- Replacing scenario group chips in the form.
- Result display updates for the new test case type values.
- README supported test types table.
- Automated and browser verification.

Out of scope:

- Keeping old scenario group chips alongside the dropdown.
- Adding unsupported/future/disabled test types.
- Persisting selections.
- Executing generated tests.
- Authentication, authorization, performance, security, regression, or mocked dependency test types.
- Replacing `TestCase.input` with an arbitrary object.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Selected type spec | `docs/specs/spec-007-selected-test-type-controls.md` | Governing spec | Created and QA passed. |
| Scenario preset spec | `docs/specs/spec-006-test-scenario-presets.md` | Superseded UX context | Scenario chips were replaced by selected test type controls. |
| Scenario preset sprint | `docs/sprints/completed/sprint-009-test-scenario-presets.md` | Prior implementation | Completed frontend-only preset chips. |
| Backend schemas | `backend/app/models/schemas.py` | Request/response contract | Implements validated `selected_test_types` with defaults. |
| Prompt builder | `backend/app/services/prompt_builder.py` | Prompt construction | Includes selected test types, definitions, and selected-only instructions. |
| Test generator | `backend/app/services/test_generator.py` | Mock and real orchestration | Propagates selected types into mock and OpenAI responses. |
| Frontend form | `frontend/src/components/TestGeneratorForm.tsx` | Main UI target | Renders selected test type dropdown and additional instructions. |
| Frontend result panel | `frontend/src/components/ResultsPanel.tsx` | Output display | Renders selected type badges for all supported enum values. |

## Files Expected To Change

- `backend/app/models/schemas.py`
- `backend/app/services/prompt_builder.py`
- `backend/app/services/test_generator.py`
- `backend/app/services/evaluation.py`
- `backend/app/api/routes.py`
- `backend/app/tests/test_schema_validation.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_api_generate_tests.py`
- `backend/app/tests/test_evaluation.py`
- `backend/app/tests/test_llm_client.py`
- `frontend/src/types.ts`
- `frontend/src/components/TestGeneratorForm.tsx`
- `frontend/src/components/ResultsPanel.tsx`
- `frontend/src/styles.css`
- `README.md`
- `backend/README.md`
- `frontend/README.md`
- `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md`
- `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`
- `docs/specs/spec-004-testpilot-ai-frontend-ux.md`
- `docs/specs/spec-006-test-scenario-presets.md`
- `docs/sprints/completed/sprint-010-selected-test-type-controls.md`

## Ordered Tasks

### Task 1. Update Backend Schemas

- **Objective:** Add validated selected test types and defaults.
- **Files:** `backend/app/models/schemas.py`, schema tests
- **Changes:** Add `TestType` enum, request `selected_test_types`, response `selected_test_types`, default handling for missing/empty lists, and update `TestCase.type`.
- **Unchanged:** Keep `TestCase.input` as string and preserve no-code-execution boundary.
- **Verify After:** Run schema validation tests.

### Task 2. Update Prompt Builder

- **Objective:** Make selected types part of generation instructions.
- **Files:** `backend/app/services/prompt_builder.py`, prompt builder tests
- **Changes:** Include selected test types, definitions, selected-only instruction, and unsupported-context warning instruction.
- **Unchanged:** Continue grounding output in retrieved context.
- **Verify After:** Run prompt builder tests.

### Task 3. Update Generation And Evaluation

- **Objective:** Ensure mock and real paths return selected types and do not generate unselected categories.
- **Files:** `backend/app/services/test_generator.py`, `backend/app/services/evaluation.py`, API/evaluation tests
- **Changes:** Pass selected types to prompt builder, include selected types in response, update mock cases and warnings, update evaluation expectations.
- **Unchanged:** Automated tests must not call the real provider.
- **Verify After:** Run backend API and evaluation tests.

### Task 4. Replace Frontend Scenario Chips

- **Objective:** Replace scenario chips with a dropdown checkbox multi-select.
- **Files:** `frontend/src/components/TestGeneratorForm.tsx`, `frontend/src/types.ts`, `frontend/src/styles.css`
- **Changes:** Render all 10 supported types, default selected types, helper descriptions, selection count, open/close behavior, and selected type payload.
- **Unchanged:** Keep additional instructions textarea.
- **Verify After:** Run frontend lint/build and browser checks.

### Task 5. Update Result Rendering

- **Objective:** Render new test type labels in results.
- **Files:** `frontend/src/components/ResultsPanel.tsx`, `frontend/src/styles.css`
- **Changes:** Update badge label mapping and styles for all 10 test type enum values.
- **Unchanged:** Do not imply tests were executed.
- **Verify After:** Browser check generated/mocked result rendering.

### Task 6. Update README And Durable Artifacts

- **Objective:** Document the supported test types and final verification.
- **Files:** `README.md`, related specs, this sprint
- **Changes:** Add supported test types table, document dropdown behavior, update supersession notes, record implementation QA.
- **Unchanged:** Do not document unsupported/future/disabled types.
- **Verify After:** Manual doc review.

## Product Rules

- Show only the 10 supported test types from SPEC-007.
- Defaults must be API Endpoint, Validation, Negative, Edge Case, and Contract / Schema.
- Additional instructions remain editable.
- Selected test types must be structured request data, not only prompt text.
- Unknown test type values must fail validation.
- Do not generate unselected test type categories.
- Use warnings when selected test types are not supported by the provided context.
- Do not execute user or generated code.

## Deliverables

- Backend selected test type schema and validation.
- Prompt selected type definitions and selected-only instructions.
- Mock and real generation response support for `selected_test_types`.
- Frontend dropdown multi-select with helper text.
- Updated result badges.
- README supported test types table.
- Automated tests and browser verification.

## Acceptance Criteria

- Frontend lets users select/deselect from exactly 10 implemented test types.
- Default selections are applied.
- Backend accepts selected test types.
- Backend rejects invalid selected test types.
- Missing or empty selected type lists use defaults.
- Prompt includes selected test types and definitions.
- Generated response includes `selected_test_types`.
- Each generated test case uses one of the supported selected type enum values.
- README documents only supported test types.
- Backend and frontend automated checks pass.
- Desktop and mobile browser checks pass.

## Dependencies / Blockers

- None before implementation.

## Risks / Watchouts

- Strict OpenAI schema can reject optional defaults or arbitrary object fields.
- Existing frontend badge styles and mappings must be updated for all 10 enum values.
- The dropdown must remain usable on mobile.
- The scenario chip code should be replaced cleanly to avoid duplicate guidance.

## Sprint Boundary Check

This sprint is bounded to selected test type controls and their request/response/prompt effects. It does not add execution, persistence, accounts, or unsupported test categories.

## Verification

- Automated verification 1: `python -m pytest backend/app/tests/test_schema_validation.py backend/app/tests/test_prompt_builder.py backend/app/tests/test_api_generate_tests.py backend/app/tests/test_evaluation.py`
- Automated verification 2: `python -m pytest backend/app/tests`
- Automated verification 3: `npm.cmd --prefix frontend run build`
- Automated verification 4: `npm.cmd --prefix frontend run lint`
- Manual/browser verification 1: Desktop browser check that the dropdown renders all 10 supported test types, defaults are selected, selections can change, and submitted payload contains `selected_test_types`.
- Manual/browser verification 2: Mobile browser check that the dropdown and labels do not overflow.
- Manual/browser verification 3: Result rendering check for new type badges and response `selected_test_types`.
- Manual verification 4: README review confirms no unsupported/future/disabled test types are documented.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-010
- **Sprint ID:** SPRINT-010
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-010-selected-test-type-controls.md`
- **Spec Path:** `docs/specs/spec-007-selected-test-type-controls.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing spec
- [x] Verified listed assets against the live repository
- [x] Checked scope, non-goals, and task sequencing for drift risk
- [x] Checked verify-after steps and final verification for concreteness
- [x] Read changed files when performing implementation QA
- [x] Compared implementation against original intent, not assumptions

### Findings

None.

### Verification Results

- **Automated:** Final automated results are recorded in the QA Report.
- **Manual:** Sprint document and implementation reviewed against SPEC-007, `docs/references/letter2.md`, and current backend/frontend files.

### Carry-Forward Updates

- Scenario chips from SPRINT-009 were replaced by the selected test type dropdown rather than kept alongside it.

### Final QA Summary

- **What was checked:** Scope, file list, task order, product rules, acceptance criteria, and verification plan.
- **What was fixed:** The sprint explicitly preserves `TestCase.input` as string to avoid reintroducing strict schema failures.
- **Residual risks:** None blocking after automated, browser, and real provider smoke verification.
- **Recommendation:** Complete.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** None.
- **Final Verification Results:** `python -m pytest backend/app/tests/test_schema_validation.py backend/app/tests/test_prompt_builder.py backend/app/tests/test_api_generate_tests.py backend/app/tests/test_evaluation.py backend/app/tests/test_llm_client.py` passed with 33 tests. `python -m pytest backend/app/tests` passed with 47 tests. `npm.cmd --prefix frontend run build` passed. `npm.cmd --prefix frontend run lint` passed. Desktop browser automation confirmed all 10 test types render, five defaults are selected, selections can change, submitted payload includes `selected_test_types`, additional instructions are preserved, and result badges render new types. Mobile browser automation at 390x844 confirmed all 10 options render with no horizontal overflow. A real OpenAI smoke test with selected types `validation`, `boundary`, and `contract_schema` returned matching `selected_test_types` and generated only those test case types.
- **Deviations From Plan:** `backend/README.md` and `frontend/README.md` were also updated to keep local package docs aligned with the completed SPRINT-010 state.
- **Carry-Forward Updates For Next Sprint:** Scenario chips from SPRINT-009 are now replaced by first-class selected test type controls. Future tuning can improve prompt wording, but no blocking gap remains.

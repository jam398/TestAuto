# Sprint: Optional Target Precedence

## Metadata

- **ID:** SPRINT-011
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-003 and SPEC-004 already define `target_name` as optional. This sprint implements bounded UX, prompt, retrieval, tests, and documentation updates without changing the broader product direction.

## Goal

Make the target field truly optional in the frontend while preserving target precedence when a user provides one.

## Governing Specs

- `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`
- `docs/specs/spec-004-testpilot-ai-frontend-ux.md`

## Carry-Forward Context

The backend schema already accepts `target_name` as optional. The frontend currently pre-fills a debt endpoint, which can confuse users into thinking the app is limited to that API. Additional instructions remain useful, but they must not override a provided target.

## Scope

In scope:

- Blank optional target input in the frontend.
- UI copy that explains target is optional and primary when provided.
- Prompt wording that establishes target precedence over conflicting additional instructions.
- Retrieval query behavior that weights target before additional instructions.
- Backend tests for blank target, non-debt APIs, and target/additional-instruction conflicts.
- README documentation for optional target behavior and multiple API examples.

Out of scope:

- Automatic target extraction from pasted context.
- File upload.
- Persistent projects or document libraries.
- Executing generated tests.
- Changing selected test type behavior.

## Files Expected To Change

- `frontend/src/components/TestGeneratorForm.tsx`
- `frontend/src/styles.css`
- `backend/app/services/prompt_builder.py`
- `backend/app/services/test_generator.py`
- `backend/app/services/vector_store.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_retrieval.py`
- `backend/app/tests/test_api_generate_tests.py`
- `README.md`
- `docs/sprints/completed/sprint-011-optional-target-precedence.md`

## Ordered Tasks

### Task 1. Update Frontend Target UX

- **Objective:** Make target optional in practice, not only in the API schema.
- **Files:** `frontend/src/components/TestGeneratorForm.tsx`, `frontend/src/styles.css`
- **Changes:** Remove prefilled target value, label it optional, add short helper copy, and keep payload omission when blank.
- **Verify After:** Frontend lint/build and browser form inspection.

### Task 2. Update Backend Prompt And Retrieval Priority

- **Objective:** Keep provided target as the principal focus even if additional instructions mention another endpoint.
- **Files:** `backend/app/services/prompt_builder.py`, `backend/app/services/vector_store.py`, backend tests
- **Changes:** Add explicit target precedence rules and repeat target in retrieval query weighting before extra instructions.
- **Verify After:** Prompt and retrieval tests.

### Task 3. Add Multi-API Request Tests

- **Objective:** Prove the API works without a target and with non-debt targets.
- **Files:** `backend/app/tests/test_api_generate_tests.py`
- **Changes:** Add blank-target and non-debt API examples.
- **Verify After:** API tests.

### Task 4. Update Documentation And QA

- **Objective:** Explain optional target behavior and record verification.
- **Files:** `README.md`, this sprint
- **Changes:** Add target guidance and example contexts for different API methods/resources.
- **Verify After:** Manual doc review.

## Product Rules

- The frontend target field may be left blank.
- If target is blank, generation uses project context and selected test types without a declared primary target.
- If target is present, it is the principal focus.
- Additional instructions can narrow or add preferences, but must not override a provided target.
- If project context, target, and additional instructions conflict, generated output should follow the target and warn rather than silently switching endpoints.

## Acceptance Criteria

- Target input starts blank.
- Blank target submissions still work.
- Provided targets remain included in request payload.
- Prompt explicitly says target is the primary focus when provided.
- Prompt explicitly says additional instructions must not override target.
- Retrieval query gives the target stronger weight than additional instructions.
- Backend tests cover blank target, non-debt API target, and conflicting additional instructions.
- README explains optional target behavior and gives non-debt API examples.
- Backend tests and frontend lint/build pass.

## Verification

- `python -m pytest backend/app/tests/test_prompt_builder.py backend/app/tests/test_retrieval.py backend/app/tests/test_api_generate_tests.py`
- `python -m pytest backend/app/tests`
- `npm.cmd --prefix frontend run lint`
- `npm.cmd --prefix frontend run build`
- Browser check that target starts blank, can be left blank, can be filled with a non-debt API, and submissions include/omit `target_name` correctly.
- Manual README review.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-011
- **Sprint ID:** SPRINT-011
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-011-optional-target-precedence.md`
- **Spec Paths:** `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`, `docs/specs/spec-004-testpilot-ai-frontend-ux.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing specs
- [x] Verified current `target_name` frontend and backend behavior against the live repository
- [x] Checked scope, non-goals, and acceptance criteria for boundedness
- [x] Checked verification commands for concreteness

### Findings

None.

### Final QA Summary

- **What was checked:** Optional target scope, precedence rules, expected files, tests, and verification.
- **What was fixed:** The sprint explicitly avoids automatic target extraction and file upload.
- **Residual risks:** Browser submit behavior needs implementation-time verification.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** None.
- **Final Verification Results:** `python -m pytest backend/app/tests/test_prompt_builder.py backend/app/tests/test_retrieval.py backend/app/tests/test_api_generate_tests.py` passed with 23 tests. `python -m pytest backend/app/tests` passed with 51 tests. `npm.cmd --prefix frontend run lint` passed. `npm.cmd --prefix frontend run build` passed. Browser automation confirmed the target input starts blank, blank submissions omit `target_name`, a non-debt target `PATCH /api/products/{id}` is submitted when filled, and additional instructions remain separate rather than replacing the target.
- **Deviations From Plan:** `backend/app/services/test_generator.py` was updated to parse HTTP method plus path from targets such as `GET /api/users/{id}` and `PATCH /api/products/{id}` so mocked starter code can demonstrate different API methods.
- **Carry-Forward Updates For Next Sprint:** Automatic target extraction remains out of scope. If added later, it should preserve the rule that explicit target input wins over inferred or additional-instruction targets.

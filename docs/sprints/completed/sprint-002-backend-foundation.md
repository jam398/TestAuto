# Sprint: Backend Foundation

## Metadata

- **ID:** SPRINT-002
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-003 already defines the backend architecture, and this sprint is a bounded first implementation slice with clear verification.

## Goal

Create the FastAPI backend shell, request/response schemas, health endpoint, mocked generate-tests route, and initial backend tests.

## Governing Spec

`docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`

## Carry-Forward Context

SPEC-002 defines the product scope and non-negotiable safety rules. SPEC-003 defines the backend API contract and requires mocked LLM behavior in automated tests. The live repository currently has no backend source tree, package files, or tests.

## Scope

In scope:

- Create the backend project structure.
- Add FastAPI application entrypoint and routing.
- Add Pydantic request and response schemas.
- Add `/health`.
- Add `/api/generate-tests` with deterministic mocked output.
- Add initial backend tests for health, request validation, response shape, and schema validation.

Out of scope:

- Real LLM calls.
- Embeddings, vector storage, or RAG retrieval.
- Frontend implementation.
- User authentication, persistence, repository scanning, or code execution.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Product spec | `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md` | Product scope | Verified present and read. |
| Backend spec | `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md` | Governing spec | Verified present and read. |
| Project letter | `docs/references/letter.md` | Source brief | Verified present and read; has encoding damage that must not be copied into product text. |
| Repository root | `.` | Live app state | Verified no `backend/` or app source exists. |

## Files Expected To Change

- `backend/requirements.txt`
- `backend/README.md`
- `backend/app/__init__.py`
- `backend/app/main.py`
- `backend/app/api/__init__.py`
- `backend/app/api/routes.py`
- `backend/app/models/__init__.py`
- `backend/app/models/schemas.py`
- `backend/app/services/__init__.py`
- `backend/app/services/test_generator.py`
- `backend/app/tests/test_api_generate_tests.py`
- `backend/app/tests/test_schema_validation.py`

## Ordered Tasks

### Task 1. Scaffold Backend

- **Objective:** Create a minimal FastAPI backend package that tests can import.
- **Files:** `backend/requirements.txt`, `backend/app/__init__.py`, `backend/app/main.py`, `backend/app/api/__init__.py`, `backend/app/api/routes.py`
- **Changes:** Add backend dependencies, app factory or app instance, router registration, and `/health`.
- **Unchanged:** No frontend or AI/RAG services.
- **Verify After:** Import the FastAPI app and run the health endpoint test.

### Task 2. Add Schemas

- **Objective:** Define strict request and response models.
- **Files:** `backend/app/models/schemas.py`
- **Changes:** Add `GenerateTestsRequest`, `TestFramework`, `TestCase`, `EvidenceSnippet`, and `GenerateTestsResponse`.
- **Unchanged:** No provider-specific LLM schema.
- **Verify After:** Run schema validation tests for valid and invalid payloads.

### Task 3. Add Mocked Generate Route

- **Objective:** Return deterministic structured output without real AI calls.
- **Files:** `backend/app/api/routes.py`, `backend/app/services/test_generator.py`
- **Changes:** Add `/api/generate-tests` route wired to a mocked generator service.
- **Unchanged:** No embeddings, vector store, real LLM, or code execution.
- **Verify After:** API tests confirm valid requests return the expected response shape.

### Task 4. Add Initial Tests And README

- **Objective:** Establish repeatable backend verification and minimal backend run notes.
- **Files:** `backend/app/tests/test_api_generate_tests.py`, `backend/app/tests/test_schema_validation.py`, `backend/README.md`
- **Changes:** Add Pytest tests for health, validation, default framework, unsupported framework, response shape, and schema parsing.
- **Unchanged:** No claims that RAG or real AI is implemented.
- **Verify After:** Run the backend test command.

## Product Rules

- Treat all user-provided code as text.
- Do not execute generated tests.
- Do not hardcode API keys.
- Do not claim RAG or real LLM generation exists in this sprint.
- Default missing framework to Pytest.

## Deliverables

- Importable FastAPI backend.
- `/health` endpoint.
- `/api/generate-tests` endpoint with mocked structured response.
- Pydantic schemas.
- Initial backend tests.

## Acceptance Criteria

- `GET /health` returns `{ "status": "ok" }`.
- Empty or too-short `project_context` fails validation.
- Unsupported `test_framework` fails validation.
- Missing `test_framework` defaults to `pytest`.
- Valid generate request returns summary, test cases, generated code, evidence, and warnings.
- Backend tests pass without real LLM or embedding calls.

## Dependencies / Blockers

- None.

## Risks / Watchouts

- Mocked output must be clearly scoped so it is not mistaken for real AI generation.
- Schema choices should remain compatible with SPEC-003 and SPEC-004.
- Dependency versions should be verified during implementation before documenting install commands as working.

## Sprint Boundary Check

This sprint creates only the backend foundation and mocked API contract. It deliberately stops before RAG, real LLM calls, and frontend work.

## Verification

- Automated verification 1: `python -m pytest backend/app/tests/test_api_generate_tests.py backend/app/tests/test_schema_validation.py`
- Automated verification 2: `python -m pytest backend/app/tests`
- Manual verification 1: Confirm route handlers do not execute user input or generated code.
- Manual verification 2: Review backend README for no claims of completed RAG or real LLM generation.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-002
- **Sprint ID:** SPRINT-002
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-002-backend-foundation.md`
- **Spec Path:** `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`

### QA Mode

Sprint doc QA

### Checks Performed

- [x] Read the full sprint doc
- [x] Read the governing spec when one exists
- [x] Verified listed assets against the live repository
- [x] Checked scope, non-goals, and task sequencing for drift risk
- [x] Checked verify-after steps and final verification for concreteness

### Findings

None.

### Verification Results

- **Automated:** Not run yet; this is a planned implementation sprint.
- **Manual:** Sprint document reviewed against SPEC-002, SPEC-003, and live repository state.

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** Scope, files, task order, non-goals, and verification were checked against backend foundation requirements.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Dependency install commands must be verified during implementation.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Initial test run passed with Pytest collection warnings because schema classes are named `TestCase`, `TestCaseType`, and `TestFramework`. Added `__test__ = False` to those schema classes and reran verification cleanly.
- **Final Verification Results:** `python -m pip install -r backend/requirements.txt` completed successfully. `python -m pytest backend/app/tests/test_api_generate_tests.py backend/app/tests/test_schema_validation.py` passed with 11 tests. `python -m pytest backend/app/tests` passed with 11 tests. Manual route review confirmed `/api/generate-tests` returns deterministic structured text only and does not execute user input or generated code. Manual README review confirmed it states RAG, embeddings, and real LLM generation are not implemented yet.
- **Deviations From Plan:** None.
- **Carry-Forward Updates For Next Sprint:** SPRINT-003 can build on the completed backend package, schemas, mocked generator, and test structure. The backend dependency install currently uses user-site packages in this environment.

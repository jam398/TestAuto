# Sprint: Structured LLM Generation And Evaluation

## Metadata

- **ID:** SPRINT-005
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-003 defines LLM validation and generation safety rules, and this sprint isolates provider integration risk from retrieval work.

## Goal

Implement structured LLM generation, JSON validation and repair/error handling, deterministic evaluation checks, and provider-safe configuration.

## Governing Spec

`docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`

## Carry-Forward Context

SPRINT-004 should provide retrieved context and evidence. SPEC-003 requires structured JSON validation, missing-information warnings, mocked tests, and environment-based API keys.

## Scope

In scope:

- Real LLM adapter behind the existing LLM client abstraction.
- Environment-based configuration for API key, LLM model, and embedding model.
- Structured JSON response validation.
- One repair attempt or clear backend error for invalid LLM JSON.
- Deterministic evaluation checks for generated output quality.
- Tests that mock LLM calls and do not require real API keys.

Out of scope:

- Running generated tests.
- Executing user code.
- Frontend implementation.
- Adding authentication, saved projects, or external repository access.
- Using a second LLM for evaluation.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Backend spec | `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md` | Governing spec | Verified present and read. |
| Product spec | `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md` | Product and safety scope | Verified present and read. |
| RAG sprint | `docs/sprints/completed/sprint-004-rag-retrieval-layer.md` | Required predecessor | Completed with passing implementation QA. |
| Project letter | `docs/references/letter.md` | Source brief | Verified present and read. |

## Files Expected To Change

- `backend/.env.example`
- `backend/README.md`
- `backend/app/config.py`
- `backend/app/api/routes.py`
- `backend/app/models/schemas.py`
- `backend/app/services/llm_client.py`
- `backend/app/services/test_generator.py`
- `backend/app/services/evaluation.py`
- `backend/app/tests/test_api_generate_tests.py`
- `backend/app/tests/test_schema_validation.py`
- `backend/app/tests/test_evaluation.py`
- `backend/app/tests/test_llm_client.py`

## Ordered Tasks

### Task 1. Add Configuration

- **Objective:** Load provider configuration from environment variables without exposing secrets.
- **Files:** `backend/app/config.py`, `backend/.env.example`, `backend/README.md`
- **Changes:** Add settings for API key, LLM model, and embedding model; document placeholders only.
- **Unchanged:** No hardcoded real secrets.
- **Verify After:** Run tests confirming missing config produces controlled behavior.

### Task 2. Add Real LLM Adapter

- **Objective:** Implement provider calls behind the LLM client abstraction.
- **Files:** `backend/app/services/llm_client.py`, `backend/app/tests/test_llm_client.py`
- **Changes:** Add adapter with structured JSON request/response handling and mockable call path.
- **Unchanged:** Automated tests must not call the provider.
- **Verify After:** Run mocked LLM client tests.

### Task 3. Validate And Repair LLM Output

- **Objective:** Ensure bad model output cannot break the frontend.
- **Files:** `backend/app/services/test_generator.py`, `backend/app/models/schemas.py`, `backend/app/tests/test_schema_validation.py`
- **Changes:** Parse into `GenerateTestsResponse`, reject missing fields, and retry once with a repair prompt or return a clear backend error.
- **Unchanged:** No free-form markdown response contract.
- **Verify After:** Run schema and invalid JSON tests.

### Task 4. Add Evaluation Checks

- **Objective:** Add deterministic checks for output completeness and context coverage.
- **Files:** `backend/app/services/evaluation.py`, `backend/app/tests/test_evaluation.py`
- **Changes:** Check for at least one positive test, one negative or edge test, evidence, generated code, warnings for incomplete context, and constraint coverage for the debt fixture.
- **Unchanged:** No second LLM evaluation.
- **Verify After:** Run evaluation tests.

### Task 5. Integrate Generation Path

- **Objective:** Connect retrieval, prompt building, LLM output validation, and evaluation into `/api/generate-tests`.
- **Files:** `backend/app/api/routes.py`, `backend/app/services/test_generator.py`, `backend/app/tests/test_api_generate_tests.py`
- **Changes:** Return validated structured responses and readable errors.
- **Unchanged:** Still no code execution.
- **Verify After:** Run the full backend test suite.

## Product Rules

- Use only environment variables for secrets.
- Use official provider documentation during implementation before selecting current model names or SDK patterns.
- Do not invent behavior when context is missing; return warnings or explicit assumptions.
- Mock LLM calls in tests.
- Keep generated code as text only.

## Deliverables

- Configured LLM adapter.
- Validated structured generation path.
- Invalid JSON repair or error handling.
- Deterministic evaluation layer.
- `.env.example`.
- Backend tests for generation and evaluation.

## Acceptance Criteria

- Real provider integration is behind a mockable abstraction.
- Missing API key returns a readable backend error when a real call is required.
- Invalid LLM JSON does not reach the frontend.
- Valid LLM JSON parses into `GenerateTestsResponse`.
- Evaluation checks detect missing evidence, missing code, and missing required test categories.
- Backend tests pass without real API calls.

## Dependencies / Blockers

- SPRINT-004 should be completed before implementation starts.
- Current official provider docs must be checked during implementation before choosing model names or SDK usage.

## Risks / Watchouts

- Provider APIs and model names may change; do not rely on stale assumptions.
- Repair prompts can hide recurring schema problems if errors are not tested.
- Generated output may be structurally valid but weak; evaluation checks should flag obvious gaps without pretending to be exhaustive.

## Sprint Boundary Check

This sprint handles AI generation and evaluation only after the backend foundation and RAG retrieval path exist. It does not build frontend UI or execute generated code.

## Verification

- Automated verification 1: `python -m pytest backend/app/tests/test_llm_client.py backend/app/tests/test_schema_validation.py backend/app/tests/test_evaluation.py`
- Automated verification 2: `python -m pytest backend/app/tests`
- Manual verification 1: Review config and `.env.example` for no hardcoded secrets.
- Manual verification 2: Review generation path for no execution of user input or generated tests.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-005
- **Sprint ID:** SPRINT-005
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-005-structured-llm-generation-evaluation.md`
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
- **Manual:** Sprint document reviewed against LLM, validation, security, and test constraints.

### Carry-Forward Updates

- Current official OpenAI docs were checked for the Responses API, structured outputs, Python SDK usage, model guidance, and `text-embedding-3-small`.

### Final QA Summary

- **What was checked:** Provider integration boundaries, schema validation, evaluation scope, and no-code-execution constraints.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Provider API details are intentionally deferred to implementation-time verification.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Backend README became stale after adding the real LLM adapter and configuration behavior; it was updated to describe the SPRINT-005 backend state.
- **Final Verification Results:** Official OpenAI docs checked before provider implementation: `https://developers.openai.com/api/reference/python/`, `https://developers.openai.com/api/docs/guides/structured-outputs`, `https://developers.openai.com/api/docs/models`, and `https://developers.openai.com/api/docs/models/text-embedding-3-small`. `python -m pip install -r backend/requirements.txt` completed successfully. `python -m pytest backend/app/tests/test_llm_client.py backend/app/tests/test_schema_validation.py backend/app/tests/test_evaluation.py` passed with 13 tests. `python -m pytest backend/app/tests` passed with 35 tests after the README update. Manual config review confirmed `.env.example` contains placeholders only and no hardcoded secrets. Manual generation-path review found no execution of user input or generated tests.
- **Deviations From Plan:** The API falls back to deterministic mock output when `OPENAI_API_KEY` is absent so local development and automated tests remain usable. A real LLM call is used only when the API key is configured; direct `OpenAILLMClient` usage raises a readable missing-key error when a real call is required.
- **Carry-Forward Updates For Next Sprint:** SPRINT-006 can integrate the frontend against `/api/generate-tests`. Without an API key, the backend returns deterministic mock output; with `OPENAI_API_KEY`, it uses the real Responses API adapter.

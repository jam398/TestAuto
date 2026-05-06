# Sprint: Provider Configuration Observability

## Metadata

- **ID:** SPRINT-008
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** SPEC-005 defines the response-contract and local secret-loading requirements; this sprint implements that bounded change.

## Goal

Make local `backend/.env` configuration load automatically and show whether generated results came from mock mode or OpenAI mode.

## Governing Spec

`docs/specs/spec-005-provider-configuration-observability.md`

## Carry-Forward Context

SPRINT-005 added OpenAI generation behind an environment-based adapter. Before this sprint, app code read only process env values, and the frontend could not tell users which provider path produced a result.

## Scope

In scope:

- Local backend `.env` loading.
- Provider mode field in backend schema and responses.
- Frontend provider mode display.
- Tests and docs for the new behavior.

Out of scope:

- Running generated tests.
- Adding CI, deployment workflows, auth, persistence, or billing.
- Exposing API key details.
- Changing model choice or provider adapter internals beyond response metadata.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Provider spec | `docs/specs/spec-005-provider-configuration-observability.md` | Governing spec | Created and QA passed. |
| Backend architecture spec | `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md` | Parent spec | Requires env-based secrets and no code execution. |
| Existing LLM sprint | `docs/sprints/completed/sprint-005-structured-llm-generation-evaluation.md` | Prior implementation | Completed with OpenAI adapter and mock fallback. |
| Backend config | `backend/app/config.py` | Env loading | Pre-implementation state read `os.getenv` only. |
| Backend schema | `backend/app/models/schemas.py` | API contract | Pre-implementation state had no provider mode field. |
| Frontend result panel | `frontend/src/components/ResultsPanel.tsx` | UI output | Pre-implementation state rendered result sections but no provider mode. |

## Files Expected To Change

- `backend/requirements.txt`
- `backend/README.md`
- `backend/app/config.py`
- `backend/app/models/schemas.py`
- `backend/app/services/test_generator.py`
- `backend/app/tests/test_api_generate_tests.py`
- `backend/app/tests/test_schema_validation.py`
- `backend/app/tests/test_config.py`
- `frontend/src/types.ts`
- `frontend/src/components/ResultsPanel.tsx`
- `frontend/src/styles.css`
- `README.md`
- `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`
- `docs/sprints/completed/sprint-008-provider-configuration-observability.md`

## Ordered Tasks

### Task 1. Add Env Loading

- **Objective:** Load local backend `.env` values without overriding real environment variables.
- **Files:** `backend/requirements.txt`, `backend/app/config.py`, `backend/app/tests/test_config.py`, `backend/README.md`, `README.md`
- **Changes:** Add dotenv dependency, load root and backend `.env` if present, and test precedence.
- **Unchanged:** No real secrets in committed files.
- **Verify After:** Run config tests.

### Task 2. Add Provider Mode Contract

- **Objective:** Make generation source visible in the API response.
- **Files:** `backend/app/models/schemas.py`, `backend/app/services/test_generator.py`, backend tests
- **Changes:** Add provider enum and populate `mock` or `openai`.
- **Unchanged:** Generated code remains text only.
- **Verify After:** Run schema and API tests.

### Task 3. Render Provider Mode

- **Objective:** Show provider mode in result output without exposing secrets.
- **Files:** `frontend/src/types.ts`, `frontend/src/components/ResultsPanel.tsx`, `frontend/src/styles.css`
- **Changes:** Update types and render a compact status badge.
- **Unchanged:** No landing page or unrelated UI redesign.
- **Verify After:** Run frontend build and lint.

### Task 4. Documentation And QA

- **Objective:** Update durable docs and record verification.
- **Files:** `README.md`, `backend/README.md`, `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`, this sprint
- **Changes:** Document automatic env loading and provider mode behavior.
- **Unchanged:** Do not claim real OpenAI smoke test unless actually run.
- **Verify After:** Review docs for placeholder-only secrets.

## Product Rules

- Never expose API keys or partial key values.
- Provider mode must mean generation source only.
- Mock fallback remains available when no key is configured.
- Real OpenAI calls stay behind the existing adapter.

## Deliverables

- Automatic local env loading.
- `provider_mode` API field.
- Provider badge in frontend results.
- Updated docs and tests.

## Acceptance Criteria

- `get_settings()` can read `backend/.env` values locally.
- Existing process env values win over `.env` values.
- Mock generation returns `provider_mode: "mock"`.
- LLM generation path returns `provider_mode: "openai"` after successful validation.
- Frontend build and lint pass.
- Backend tests pass.

## Dependencies / Blockers

- None for implementation. Real OpenAI smoke testing requires the user-provided key and network.

## Risks / Watchouts

- Tests must isolate environment mutation.
- LLM schema tests must include the new required field.
- UI wording must not imply test execution.

## Sprint Boundary Check

This sprint only improves configuration loading and result observability. It does not change generation scope, execute code, or add deployment features.

## Verification

- Automated verification 1: `python -m pytest backend/app/tests/test_config.py backend/app/tests/test_api_generate_tests.py backend/app/tests/test_schema_validation.py`
- Automated verification 2: `python -m pytest backend/app/tests`
- Automated verification 3: `npm.cmd --prefix frontend run build`
- Automated verification 4: `npm.cmd --prefix frontend run lint`
- Manual verification 1: Review docs and env examples for placeholder-only secrets.
- Manual verification 2: Review result UI wording for provider source only, not execution status.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-008
- **Sprint ID:** SPRINT-008
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-008-provider-configuration-observability.md`
- **Spec Path:** `docs/specs/spec-005-provider-configuration-observability.md`

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
- **Manual:** Sprint document and implementation were reviewed against SPEC-005 and current backend/frontend files.

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** Scope, acceptance criteria, file list, task order, and verification commands.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Real OpenAI smoke testing remains outside this sprint unless requested after local config is verified.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Focused backend tests initially attempted a real OpenAI call after env loading because a config test populated `OPENAI_API_KEY`; API tests were tightened to force mock mode unless they explicitly exercise the LLM client boundary. The mock warning text also contained stale wording that implied real LLM generation was not implemented; it was corrected.
- **Final Verification Results:** `python -m pytest backend/app/tests/test_config.py backend/app/tests/test_api_generate_tests.py backend/app/tests/test_schema_validation.py` passed with 16 tests. `python -m pytest backend/app/tests` passed with 38 tests. `npm.cmd --prefix frontend run build` passed. `npm.cmd --prefix frontend run lint` passed. Manual review confirmed committed env examples contain placeholders only and `provider_mode` exposes only `mock` or `openai`, not secrets or execution status.
- **Deviations From Plan:** None.
- **Carry-Forward Updates For Next Sprint:** Real OpenAI smoke testing was not run in this sprint to avoid spending the user's API key without explicit confirmation. The app is now ready for a deliberate one-request smoke test.

## Post-Completion Fix

- **Date:** 2026-05-04
- **Reason:** Browser testing showed `Generation failed: Failed to fetch` while the backend was healthy at `127.0.0.1:8000`. The frontend fallback used `localhost:8000`, which can resolve differently than the address where Uvicorn is bound.
- **Files Changed:** `frontend/src/lib/api.ts`, `.env.example`, `README.md`, `frontend/README.md`
- **Verification:** `npm.cmd --prefix frontend run build` and `npm.cmd --prefix frontend run lint` passed after the fix.

## Post-Completion Config Fix

- **Date:** 2026-05-04
- **Reason:** Frontend dev config needed to own the local host/port behavior instead of relying only on package script flags, and TypeScript needed Vite-aligned module resolution for the app and config file.
- **Files Changed:** `frontend/vite.config.ts`, `frontend/tsconfig.json`
- **Verification:** `npm.cmd --prefix frontend run build` and `npm.cmd --prefix frontend run lint` passed. The Vite React plugin call was corrected to `react()` during verification.

## Post-Completion Fetch Fix

- **Date:** 2026-05-04
- **Reason:** Browser automation reproduced `Failed to fetch`. The backend returned an unhandled provider exception as HTTP 500 without CORS headers, and the frontend was using an absolute cross-origin backend URL instead of the Vite proxy.
- **Files Changed:** `backend/app/services/llm_client.py`, `backend/app/tests/test_llm_client.py`, `backend/app/models/schemas.py`, `backend/app/services/test_generator.py`, `backend/app/tests/test_schema_validation.py`, `backend/app/tests/test_evaluation.py`, `frontend/src/lib/api.ts`, `frontend/src/types.ts`, `.env.example`, `README.md`, `frontend/README.md`, `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`
- **Verification:** Browser automation first confirmed the fetch/CORS failure became a controlled 502 through Vite proxy. Direct provider testing then showed OpenAI rejected the strict schema because optional/default object properties and arbitrary object input were not valid strict structured-output schema. The response schema was tightened so evidence `source`, response `warnings`, and string `input` are required. `python -m pytest backend/app/tests` passed with 40 tests. `npm.cmd --prefix frontend run build` and `npm.cmd --prefix frontend run lint` passed. A real OpenAI smoke test returned `ProviderMode.OPENAI` with 14 test cases. Browser automation against `http://127.0.0.1:5173` submitted the sample form, received HTTP 200 from `/api/generate-tests`, and verified the UI rendered `OpenAI mode`.

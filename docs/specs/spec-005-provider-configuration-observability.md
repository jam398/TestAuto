# Spec: Provider Configuration Observability

## Metadata

- **ID:** SPEC-005
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** SPEC-003
- **Related Sprints:** SPRINT-008

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** The change affects provider configuration, secret-loading behavior, backend response schema, frontend display, and verification of whether real LLM generation is active.

## Problem Statement

After a developer creates `backend/.env` with an OpenAI API key, the backend should load that file during local development without requiring fragile command-line flags. The app should also make the generation provider visible so users can tell whether a response came from deterministic mock mode or the OpenAI adapter.

## Goals

- Load local backend environment values from `backend/.env` when present.
- Preserve production behavior where real environment variables still work and take precedence.
- Add a non-secret provider mode to generated responses.
- Render provider mode in the frontend result view.
- Keep automated tests independent from real OpenAI calls.

## Non-Goals

- Exposing API keys, partial keys, account IDs, billing state, or provider secrets.
- Executing generated tests.
- Adding authentication, persistence, or deployment automation.
- Replacing the current OpenAI adapter or retrieval approach.

## Current State

Verified on 2026-05-04:

- `backend/app/config.py` reads `OPENAI_API_KEY`, `LLM_MODEL`, and `EMBEDDING_MODEL` with `os.getenv`.
- `backend/.env` is ignored by Git, but it is not loaded automatically by app code.
- `/api/generate-tests` falls back to deterministic mock generation when no API key is present.
- `GenerateTestsResponse` contains summary, test cases, generated code, evidence, and warnings, but no provider/source field.
- The frontend result panel renders output sections but does not show mock versus OpenAI mode.

## Proposed Approach

1. Add local `.env` loading in backend configuration using a small dependency.
2. Keep environment-variable precedence over values from `.env` files.
3. Add a `provider_mode` enum to `GenerateTestsResponse`.
4. Set `provider_mode` to `mock` in deterministic generation and `openai` after real LLM generation succeeds.
5. Update frontend types and result rendering to display provider mode.
6. Update docs and tests to cover the behavior.

## Architecture / Data / Flow Notes

- Backend config should load `backend/.env` and optionally root `.env` for local development.
- `.env` files must stay ignored by Git.
- API response shape becomes:

```json
{
  "provider_mode": "mock"
}
```

or:

```json
{
  "provider_mode": "openai"
}
```

- Provider mode is informational only. It must not include secrets or imply tests were executed.

## Invariants

- Real API keys must never be committed or rendered.
- Tests must not require a real OpenAI key.
- Production environment variables must not be overridden by local `.env` files.
- Provider mode must describe generation source only, not execution status.
- Existing safety boundary remains: generated code is text only.

## Risks

- Loading `.env` automatically could override production values if precedence is wrong.
- Response schema changes can break frontend or LLM structured-output parsing if tests are not updated.
- Users may confuse `openai` mode with executed tests unless UI language stays precise.

## Verification Strategy

- Backend tests for `.env` loading and environment precedence.
- Backend API tests for `provider_mode` in mock responses.
- Schema tests for valid provider mode and invalid values.
- Frontend TypeScript build and lint.
- Manual review that `.env` files remain ignored and docs use placeholders only.

## Sprint Plan

1. SPRINT-008: Implement local env loading and provider mode visibility across backend, frontend, docs, and tests.

## Rollout / Sequencing Notes

This work should complete before real user OpenAI smoke testing so the user can see whether the app is using the real adapter.

## Completion Criteria

- `backend/.env` is loaded during local backend startup without `--env-file`.
- Existing real process environment values take precedence over `.env` values.
- `/api/generate-tests` returns `provider_mode`.
- Frontend displays provider mode without exposing secrets.
- Backend and frontend verification pass.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-005
- **Spec ID:** SPEC-005
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-005-provider-configuration-observability.md`

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

- **What was checked:** Local env loading, provider mode response contract, frontend display, safety boundaries, and verification strategy.
- **What was fixed:** The spec explicitly requires environment precedence and forbids exposing secrets.
- **Residual risks:** Real OpenAI smoke testing still depends on a valid user-provided key and network availability.
- **Recommendation:** Ready.

# Sprint: Core Backend Services

## Metadata

- **ID:** SPRINT-003
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-003 defines the backend service boundaries, and this sprint is a bounded services slice after the backend foundation exists.

## Goal

Implement deterministic text cleaning, chunking, prompt building, and LLM client abstraction without real provider calls.

## Governing Spec

`docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`

## Carry-Forward Context

This sprint depends on SPRINT-002 creating the backend package, schemas, route shell, and initial tests. SPEC-003 requires modular services and mocked LLM behavior in tests.

## Scope

In scope:

- Text cleaning service.
- Chunking service with metadata preservation.
- Prompt builder service.
- LLM client interface or abstraction with fake/test implementation.
- Unit tests for cleaning, chunking, prompt construction, and abstraction behavior.

Out of scope:

- Real embeddings.
- Vector store integration.
- Real LLM calls.
- Frontend implementation.
- Executing user or generated code.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Backend spec | `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md` | Governing spec | Verified present and read. |
| Product spec | `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md` | Safety and product scope | Verified present and read. |
| Backend foundation sprint | `docs/sprints/completed/sprint-002-backend-foundation.md` | Required predecessor | Completed with passing implementation QA. |
| Project letter | `docs/references/letter.md` | Source brief | Verified present and read. |

## Files Expected To Change

- `backend/app/services/chunking.py`
- `backend/app/services/prompt_builder.py`
- `backend/app/services/llm_client.py`
- `backend/app/services/test_generator.py`
- `backend/app/tests/test_chunking.py`
- `backend/app/tests/test_prompt_builder.py`
- `backend/app/tests/test_llm_client.py`

## Ordered Tasks

### Task 1. Add Cleaning And Chunking

- **Objective:** Convert raw user context into stable chunks for later retrieval.
- **Files:** `backend/app/services/chunking.py`, `backend/app/tests/test_chunking.py`
- **Changes:** Add whitespace cleaning, chunk splitting around 500 to 900 characters, overlap around 100 characters, and metadata preservation.
- **Unchanged:** No embeddings or vector store.
- **Verify After:** Run chunking tests for empty, small, long, overlap, and metadata cases.

### Task 2. Add Prompt Builder

- **Objective:** Build reusable prompts from target name, framework, instructions, and retrieved evidence.
- **Files:** `backend/app/services/prompt_builder.py`, `backend/app/tests/test_prompt_builder.py`
- **Changes:** Add prompt assembly that instructs the model to use provided context, return schema-compatible JSON, and warn instead of inventing missing behavior.
- **Unchanged:** No direct LLM SDK calls.
- **Verify After:** Run prompt builder tests for target, framework, evidence, extra instructions, and anti-fabrication rules.

### Task 3. Add LLM Client Abstraction

- **Objective:** Define an interface that later real LLM clients can implement while tests use fakes.
- **Files:** `backend/app/services/llm_client.py`, `backend/app/tests/test_llm_client.py`
- **Changes:** Add minimal protocol/class and fake client behavior for deterministic tests.
- **Unchanged:** No provider-specific implementation.
- **Verify After:** Run abstraction tests confirming no external API call is required.

### Task 4. Wire Services Into Generator

- **Objective:** Let the mocked generator use cleaning, chunking, and prompt-building paths where appropriate.
- **Files:** `backend/app/services/test_generator.py`
- **Changes:** Integrate service calls without changing the public API response contract.
- **Unchanged:** The generate route remains deterministic and offline.
- **Verify After:** Run all backend tests from SPRINT-002 and this sprint.

## Product Rules

- Do not invent behavior unsupported by provided context.
- Do not execute user-provided code.
- Do not call real LLMs in automated tests.
- Keep prompt builder reusable and isolated from route handlers.

## Deliverables

- Cleaning and chunking service.
- Prompt builder service.
- LLM client abstraction.
- Unit tests for core services.

## Acceptance Criteria

- Long context is split into multiple chunks with overlap.
- Small context returns one chunk.
- Empty context is handled consistently with validation rules.
- Chunk metadata includes source information.
- Prompt includes target name, framework, extra instructions when provided, and evidence.
- Prompt includes rules against unsupported invention.
- Tests pass without network or API keys.

## Dependencies / Blockers

- SPRINT-002 should be completed before implementation starts.

## Risks / Watchouts

- Chunking should not become overly clever before real retrieval exists.
- Prompt builder must not contain damaged encoded characters from `letter.md`.
- The LLM abstraction should stay small until real provider integration is implemented.

## Sprint Boundary Check

This sprint builds deterministic core services only. It prepares for RAG and LLM work without implementing those integrations.

## Verification

- Automated verification 1: `python -m pytest backend/app/tests/test_chunking.py backend/app/tests/test_prompt_builder.py backend/app/tests/test_llm_client.py`
- Automated verification 2: `python -m pytest backend/app/tests`
- Manual verification 1: Review service modules for no network calls or code execution.
- Manual verification 2: Review prompt text for evidence and missing-information warnings.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-003
- **Sprint ID:** SPRINT-003
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-003-core-backend-services.md`
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
- **Manual:** Sprint document reviewed against SPEC-003 and predecessor sprint sequencing.

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** The sprint was checked for service-only scope, concrete tests, and no premature provider integration.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Implementation must keep provider-specific code out of this sprint.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** None.
- **Final Verification Results:** `python -m pytest backend/app/tests/test_chunking.py backend/app/tests/test_prompt_builder.py backend/app/tests/test_llm_client.py` passed with 11 tests. `python -m pytest backend/app/tests` passed with 22 tests. Manual service review found no network calls, shell calls, subprocess usage, or code execution paths. Manual prompt review confirmed retrieved evidence, missing-information warnings, anti-fabrication rules, and valid JSON instructions are present.
- **Deviations From Plan:** None.
- **Carry-Forward Updates For Next Sprint:** SPRINT-004 can build on `chunking.py`, `prompt_builder.py`, `llm_client.py`, and the updated mocked generator path. RAG retrieval should keep using deterministic fake embeddings in tests.

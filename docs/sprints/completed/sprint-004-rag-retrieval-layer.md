# Sprint: RAG Retrieval Layer

## Metadata

- **ID:** SPRINT-004
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-003 defines the RAG flow, and this sprint is a bounded retrieval slice that can be verified with fake embeddings.

## Goal

Add embedding and vector retrieval services that return relevant context chunks with metadata for evidence-grounded generation.

## Governing Spec

`docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`

## Carry-Forward Context

This sprint depends on SPRINT-003 implementing chunking and prompt-building services. SPEC-003 requires retrieval to use local vector search and to preserve evidence metadata. Automated tests must use fake embeddings or mocked vector store behavior.

## Scope

In scope:

- Embeddings wrapper interface.
- Local vector store interface and MVP implementation.
- Retrieval query construction.
- Top-k retrieval of chunks with text and metadata.
- Fallback behavior when no chunks are available or no relevant chunks are found.
- Tests using deterministic fake embeddings or mocked vector store behavior.

Out of scope:

- Real LLM generation.
- Executing generated tests.
- Repository ingestion or file upload.
- Complex persistence across users or sessions.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Backend spec | `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md` | Governing spec | Verified present and read. |
| Core services sprint | `docs/sprints/completed/sprint-003-core-backend-services.md` | Required predecessor | Completed with passing implementation QA. |
| Project letter | `docs/references/letter.md` | Source brief | Verified present and read. |

## Files Expected To Change

- `backend/requirements.txt`
- `backend/app/services/embeddings.py`
- `backend/app/services/vector_store.py`
- `backend/app/services/test_generator.py`
- `backend/app/tests/test_retrieval.py`
- `backend/app/tests/test_api_generate_tests.py`

## Ordered Tasks

### Task 1. Add Embeddings Wrapper

- **Objective:** Provide a testable interface for embedding text chunks.
- **Files:** `backend/app/services/embeddings.py`, `backend/app/tests/test_retrieval.py`
- **Changes:** Add embedding interface and deterministic fake embedding support for tests.
- **Unchanged:** No direct provider dependency required in tests.
- **Verify After:** Run retrieval tests confirming deterministic embeddings are used.

### Task 2. Add Vector Store Service

- **Objective:** Store and retrieve chunks with metadata through a local vector search abstraction.
- **Files:** `backend/app/services/vector_store.py`, `backend/app/tests/test_retrieval.py`
- **Changes:** Add store/retrieve functions, top-k handling, empty-store behavior, and metadata return shape.
- **Unchanged:** No user account or long-term project persistence.
- **Verify After:** Run retrieval tests for relevant chunks, metadata, and empty fallback.

### Task 3. Wire Retrieval Into Generator

- **Objective:** Use chunks and retrieved evidence in the generation pipeline while keeping output deterministic.
- **Files:** `backend/app/services/test_generator.py`, `backend/app/tests/test_api_generate_tests.py`
- **Changes:** Add retrieval call path and include retrieved evidence in generated response.
- **Unchanged:** No real LLM call.
- **Verify After:** API tests confirm evidence comes from provided context.

### Task 4. Verify Dependency Choice

- **Objective:** Confirm local vector dependency remains appropriate for MVP.
- **Files:** `backend/requirements.txt`, `backend/README.md`
- **Changes:** Add only required dependencies after checking install/import behavior during implementation.
- **Unchanged:** Do not document unverified install or run commands as working.
- **Verify After:** Run backend test suite in the implementation environment.

## Product Rules

- Evidence snippets must come from user-provided context chunks.
- Retrieval must not execute code or access repositories.
- Tests must not require real embedding API calls.
- Keep vector store implementation replaceable behind a service interface.

## Deliverables

- Embeddings service wrapper.
- Vector store service.
- Retrieval tests.
- Generator path that carries retrieved evidence.

## Acceptance Criteria

- Relevant chunks can be retrieved from provided context.
- Retrieved chunks include text and metadata.
- No chunks or no relevant chunks produces a clear fallback warning or behavior.
- Retrieval can be tested deterministically without network calls.
- Evidence in responses is traceable to user-provided context.

## Dependencies / Blockers

- SPRINT-003 should be completed before implementation starts.

## Risks / Watchouts

- ChromaDB or FAISS dependency setup may be heavier than needed for MVP; implementation should keep the service boundary clean.
- Retrieval scores can create false confidence if surfaced without context.
- Evidence must not be fabricated from prompt output.

## Sprint Boundary Check

This sprint adds retrieval and evidence grounding only. It does not add real LLM generation or frontend rendering.

## Verification

- Automated verification 1: `python -m pytest backend/app/tests/test_retrieval.py`
- Automated verification 2: `python -m pytest backend/app/tests`
- Manual verification 1: Review evidence paths to confirm snippets originate from user context chunks.
- Manual verification 2: Review services for no code execution and no repository access.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-004
- **Sprint ID:** SPRINT-004
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-004-rag-retrieval-layer.md`
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
- **Manual:** Sprint document reviewed against RAG scope and safety constraints.

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** Retrieval scope, evidence requirements, testability, and dependency risk were checked against SPEC-003.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Dependency selection must be verified during implementation.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** Backend README became stale after adding local deterministic retrieval; it was updated to state the SPRINT-004 backend state and clarify that real external embeddings and real LLM generation are still not implemented.
- **Final Verification Results:** `python -m pytest backend/app/tests/test_retrieval.py` passed with 6 tests. `python -m pytest backend/app/tests` passed with 28 tests after the README update. Manual evidence-path review confirmed response evidence is derived from `TextChunk` values created from `project_context`, with fallback to initial context chunks when retrieval returns no positive scores. Manual service review found no code execution, repository access, provider calls, or network calls.
- **Deviations From Plan:** Used a deterministic local embedding client plus in-memory vector store instead of adding ChromaDB/FAISS dependency in this sprint. This keeps the service boundary replaceable and avoids unneeded dependency risk for the MVP retrieval layer.
- **Carry-Forward Updates For Next Sprint:** SPRINT-005 can build on deterministic retrieval and must keep real provider calls behind the existing mockable `LLMClient` abstraction. README should be updated again after real LLM generation is implemented.

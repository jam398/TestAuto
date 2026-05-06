# Spec: TestPilot AI Backend and RAG Architecture

## Metadata

- **ID:** SPEC-003
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** SPEC-002
- **Related Sprints:** SPRINT-002, SPRINT-003, SPRINT-004, SPRINT-005, SPRINT-008, SPRINT-010

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** Backend, RAG, LLM output validation, and safety boundaries are architectural and truth-sensitive.

## Problem Statement

TestPilot AI needs a backend that can validate requests, process user-provided context as text, retrieve relevant evidence, generate structured recommendations through an LLM abstraction, and return validated JSON to the frontend. The backend must be modular and testable so the MVP can grow without becoming a single route that mixes validation, retrieval, prompting, and AI calls.

## Goals

- Define the backend API contract for TestPilot AI.
- Define modular service boundaries for cleaning, chunking, embeddings, vector retrieval, prompting, LLM calls, generation orchestration, and evaluation.
- Define strict Pydantic schemas for request and response validation.
- Define the RAG flow used to ground output in user-provided context.
- Define deterministic backend tests that do not require real LLM calls.

## Non-Goals

- Executing user code or generated tests.
- Authentication, accounts, persistence of user projects, or admin features.
- Full repository ingestion or private repository access.
- Building a complex evaluation system with another LLM.
- Locking the implementation to a provider-specific API shape before implementation verifies the chosen SDK.

## Current State

Verified repository state on 2026-05-04:

- No backend source tree exists.
- No package files, FastAPI app, Pydantic schemas, vector store, LLM client, or backend tests exist yet.
- `docs/references/letter.md` defines the intended backend architecture, API endpoints, schemas, RAG workflow, prompt behavior, evaluation checks, and testing plan.
- SPEC-002 governs product scope and safety constraints.

## Proposed Approach

1. Create a `backend/` FastAPI application with modular service files.
2. Implement `/health` first to establish the app shell.
3. Implement `/api/generate-tests` with request validation and mocked generation before real LLM integration.
4. Add service modules for text cleaning, chunking, prompt building, LLM client abstraction, vector store, generation orchestration, and evaluation.
5. Add embeddings and local vector retrieval after chunking and prompt builder tests pass.
6. Add real LLM generation behind an interface that can be mocked in tests.
7. Validate LLM output through Pydantic before returning it to the frontend.

## Architecture / Data / Flow Notes

Recommended backend structure:

```text
backend/
  app/
    main.py
    config.py
    api/
      routes.py
    models/
      schemas.py
    services/
      chunking.py
      embeddings.py
      vector_store.py
      prompt_builder.py
      llm_client.py
      test_generator.py
      evaluation.py
    tests/
      test_chunking.py
      test_prompt_builder.py
      test_retrieval.py
      test_api_generate_tests.py
      test_schema_validation.py
      test_evaluation.py
  requirements.txt
  README.md
```

Required endpoints:

- `GET /health`
  - Response: `{ "status": "ok" }`
- `POST /api/generate-tests`
  - Request model: `GenerateTestsRequest`
  - Response model: `GenerateTestsResponse`

Required request fields:

- `project_context`: string, required, non-empty, minimum length around 30 characters.
- `target_name`: optional string.
- `test_framework`: enum with `pytest` and `jest_supertest`, default `pytest`.
- `selected_test_types`: optional list of supported test type enum values, defaulting to `api_endpoint`, `validation`, `negative`, `edge_case`, and `contract_schema` when missing or empty.
- `extra_instructions`: optional string.

Required response fields:

- `provider_mode`: enum with `mock` and `openai`, indicating generation source only.
- `selected_test_types`: list of supported test type enum values used for generation.
- `summary`: string.
- `test_cases`: list of `TestCase`.
- `generated_code`: string.
- `evidence`: list of `EvidenceSnippet`.
- `warnings`: list of strings.

For OpenAI strict structured outputs, all response object properties are required. If there are no warnings, `warnings` must be an empty list. Each evidence object must include both `snippet` and `source`.

Required `TestCase` fields:

- `name`: string.
- `type`: enum with `api_endpoint`, `validation`, `negative`, `edge_case`, `boundary`, `contract_schema`, `error_handling`, `smoke`, `unit`, `integration`.
- `description`: string.
- `input`: string describing the request, function argument, or scenario input.
- `expected_result`: string.
- `reason`: string.

Required RAG flow:

1. Clean `project_context`.
2. Split into chunks around 500 to 900 characters with about 100 characters of overlap.
3. Preserve source metadata, using `project_context` as the MVP source.
4. Create embeddings for chunks through a wrapper.
5. Store and retrieve chunks through a local vector store.
6. Build a retrieval query from target name, test framework, request intent, and extra instructions.
7. Retrieve top 4 to 8 chunks.
8. Pass retrieved context into the prompt builder.
9. Generate structured JSON.
10. Validate the response model.

## Invariants

- User-provided code is analyzed only as text.
- Generated code is returned only as text.
- Automated tests must mock LLM and embedding calls.
- Missing or invalid LLM JSON must not silently reach the frontend.
- Prompt instructions must tell the model not to invent unsupported behavior.
- Evidence snippets must be derived from provided or retrieved context.
- If authentication, status codes, or error behavior are missing, output should warn or mark assumptions instead of fabricating certainty.
- API keys must come from environment variables and never be hardcoded.
- Provider mode must not expose secrets or imply generated tests were executed.

## Risks

- Provider SDK behavior may differ from the eventual implementation assumptions.
- Vector store setup can overcomplicate the MVP if introduced before core schemas and services.
- Prompt output may be valid JSON but still weak or unsupported without evaluation checks.
- ChromaDB or FAISS may add dependency friction; the first sprint should keep interfaces clean.
- Request size limits must be defined before large pasted contexts are supported.

## Verification Strategy

- `pytest` backend tests for health endpoint and request validation.
- Schema validation tests for valid and invalid generated responses.
- Chunking tests for long text, small text, empty text, overlap, and metadata.
- Prompt builder tests for target name, framework, evidence, and extra instructions.
- Retrieval tests using fake embeddings or mocked vector store behavior.
- Evaluation tests using the debt API fixture from SPEC-002 and the letter.
- Error path tests for missing API key, invalid LLM JSON, vector store errors, no relevant chunks, and request too large.

## Sprint Plan

1. Backend foundation sprint: app shell, `/health`, schemas, mocked `/api/generate-tests`, initial tests.
2. Core services sprint: cleaning, chunking, prompt builder, LLM client interface, unit tests.
3. RAG sprint: embedding wrapper, local vector store interface, retrieval, evidence propagation, mocked retrieval tests.
4. Generation sprint: real LLM adapter behind configuration, structured JSON validation, repair/error strategy, evaluation checks.

## Rollout / Sequencing Notes

Do not add real LLM calls until mocked response validation and API tests exist. Do not let vector store implementation details leak into route handlers.

## Completion Criteria

- Backend exposes `/health` and `/api/generate-tests`.
- Request validation rejects empty context and unsupported frameworks.
- Response validation enforces structured output.
- Service boundaries are modular and testable.
- Retrieval returns chunks with text and metadata.
- LLM calls are abstracted and mocked in automated tests.
- The debt API fixture can produce or validate the expected categories of tests.
- No user input is executed.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-003
- **Spec ID:** SPEC-003
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`

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

- The exact LLM and embedding models should be selected during implementation using current official provider documentation.

### Final QA Summary

- **What was checked:** Backend API contract, RAG flow, service boundaries, safety rules, and test expectations were checked against SPEC-002 and `docs/references/letter.md`.
- **What was fixed:** The spec avoids hardcoding provider-specific model claims beyond environment-based configuration, and `Related Sprints` was updated after SPRINT-002 through SPRINT-005 were planned.
- **Residual risks:** Dependency choices need implementation-time verification.
- **Recommendation:** Ready.

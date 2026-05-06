# Spec: TestPilot AI MVP Product Scope

## Metadata

- **ID:** SPEC-002
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** None
- **Related Sprints:** SPRINT-002, SPRINT-003, SPRINT-004, SPRINT-005, SPRINT-006, SPRINT-007, SPRINT-009, SPRINT-010

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** TestPilot AI is foundational product work with product scope, architecture, safety, AI behavior, frontend, backend, and verification implications.

## Problem Statement

Developers often have API documentation, validation rules, function descriptions, or README notes but still need to manually turn that context into useful tests. TestPilot AI should reduce that manual work by generating reviewable test plans, edge cases, starter test code, and evidence-backed recommendations from user-provided context.

The MVP must prove the core product idea without drifting into a generic chatbot, CI/CD tool, enterprise testing platform, or code execution system.

## Goals

- Build a focused AI-powered test case generator named **TestPilot AI**.
- Let users paste backend API, function, validation, README-style, or small code-snippet context.
- Support Pytest and Jest/Supertest as target test frameworks, defaulting to Pytest.
- Let users choose supported test types before generation.
- Generate structured output with summary, test cases, starter code, evidence snippets, and warnings.
- Ground recommendations in user-provided context and avoid unsupported claims.
- Keep the first version professional, useful, and scoped to a polished MVP.

## Non-Goals

- User authentication, teams, accounts, or payments.
- Full GitHub integration, repository scanning, CI/CD integration, or production monitoring.
- Running user-submitted code, uploaded code, generated code, or generated tests.
- Selenium, Playwright browser automation, admin panels, dashboards, or complex persistence.
- A generic chatbot experience.
- Advanced future features unless a later spec explicitly governs them.

## Current State

Verified repository state on 2026-05-04:

- The repository contains workflow documentation, one prior workflow spec, and one completed workflow sprint.
- `docs/references/letter.md` contains the TestPilot AI project brief and was read fully for this spec.
- No `backend/`, `frontend/`, application source, package files, or test suites exist yet.
- `docs/references/letter.md` has visible mojibake/encoding damage in several display strings. The damaged encoding should not be copied into user-facing product text.

## Proposed Approach

1. Treat this spec as the umbrella product scope for TestPilot AI.
2. Use child specs for backend/RAG architecture and frontend UX so implementation sprints can stay bounded.
3. Implement in phases: backend foundation, core services, RAG layer, LLM generation, frontend, polish/documentation.
4. Start with mocked AI output before integrating real LLM calls.
5. Require strict structured response validation before the frontend renders generated content.
6. Preserve the safety boundary that all user code and generated code are text only.

## Architecture / Data / Flow Notes

- Product name: **TestPilot AI**.
- Subtitle: **AI-powered test case generation for backend APIs and software functions.**
- Primary workflow:
  1. User opens the app.
  2. User pastes project context.
  3. User selects Pytest or Jest/Supertest.
  4. User clicks `Generate Tests`.
  5. Backend validates, cleans, chunks, embeds, retrieves, prompts, and validates output.
  6. Frontend displays structured results.
- Preferred architecture:
  - `backend/` with FastAPI, Pydantic, Pytest, service modules, and tests.
  - `frontend/` with React or Next.js, TypeScript, and Tailwind CSS.
  - Local vector search through ChromaDB unless a later sprint verifies a better fit.
- Child specs:
  - `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`
  - `docs/specs/spec-004-testpilot-ai-frontend-ux.md`

## Invariants

- Build TestPilot AI, not a generic chatbot.
- Do not execute user-submitted code.
- Do not execute generated tests.
- Do not install dependencies, run shell commands, or access repositories based on user input.
- Do not invent fake features, fake integrations, fake links, or fake project status in docs.
- LLM output must be structured JSON and validated before use.
- Evidence snippets must come from user-provided context or retrieved chunks.
- Missing information should produce warnings, not fabricated certainty.
- Automated backend tests must mock LLM calls.

## Risks

- The app could drift into an overbuilt testing platform instead of a focused generator.
- LLM output could invent unsupported behavior if prompts and validation are weak.
- Evidence snippets could create false confidence if not tied to retrieved context.
- UI polish could displace core backend correctness if implementation starts with visual work.
- Encoding damage in `letter.md` could leak into product copy if copied directly.

## Verification Strategy

- Spec verification: confirm this spec reflects the letter and live repository state.
- Backend verification: run Pytest suites for validation, schemas, chunking, prompt builder, retrieval, API behavior, and evaluation.
- Frontend verification: run build/lint checks and browser checks for desktop and mobile layouts after frontend exists.
- Product verification: use the debt API fixture from the letter to confirm generated output includes expected positive, negative, validation, evidence, and warning behavior.
- Safety verification: confirm no code execution path exists for user input or generated tests.

## Sprint Plan

1. SPRINT-002: Backend foundation with FastAPI app, health endpoint, schemas, mocked `/api/generate-tests`, and validation tests.
2. SPRINT-003: Core backend services with text cleaning, chunking, prompt builder, LLM client abstraction, and unit tests.
3. SPRINT-004: RAG retrieval layer with embeddings wrapper, vector store interface, retrieval, evidence propagation, and mocked retrieval tests.
4. SPRINT-005: Structured LLM generation and evaluation with provider adapter, response validation, repair/error path, and mocked tests.
5. SPRINT-006: Frontend MVP with app-first UI, input form, framework selector, loading/error states, and structured result rendering.
6. SPRINT-007: Polish, documentation, sample fixture, responsive checks, and final verification.

## Rollout / Sequencing Notes

Backend foundation should come first because the frontend depends on stable request and response contracts. Real LLM integration should follow mocked output and schema validation, not precede them.

## Completion Criteria

- A user can paste API/function context and generate structured test recommendations.
- The app supports Pytest and Jest/Supertest, defaulting to Pytest.
- Output includes summary, test cases, generated code, evidence, and warnings.
- The backend validates request and response schemas.
- RAG retrieves context chunks for grounding generated output.
- The frontend renders results clearly with loading and error states.
- Backend tests pass without real LLM calls.
- README explains setup, usage, testing, limitations, and safety boundaries.
- No user or generated code is executed.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-002
- **Spec ID:** SPEC-002
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md`

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

- **What was checked:** The spec was checked against `docs/references/letter.md`, workflow rules, and the live repository file list.
- **What was fixed:** The spec avoids copying damaged encoded characters from the letter into product copy, and `Related Sprints` plus sprint sequencing were updated after SPRINT-002 through SPRINT-007 were planned.
- **Residual risks:** Future implementation still needs sprints and verification before any app behavior can be claimed complete.
- **Recommendation:** Ready.

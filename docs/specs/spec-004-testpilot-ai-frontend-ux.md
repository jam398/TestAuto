# Spec: TestPilot AI Frontend UX

## Metadata

- **ID:** SPEC-004
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** SPEC-002
- **Related Sprints:** SPRINT-006, SPRINT-009, SPRINT-010

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** The frontend defines the primary user workflow, visual presentation, state handling, and rendering contract for AI-generated output.

## Problem Statement

TestPilot AI needs a frontend that feels like a focused developer tool, not a marketing site or chatbot. The user must be able to paste context, select a framework, generate tests, and inspect structured output with evidence and warnings. The UI must make generated recommendations easy to review without hiding uncertainty or dumping one large text block.

## Goals

- Provide an app-first interface for the core test-generation workflow.
- Let users enter project context, optional target name, preferred test framework, and optional extra instructions.
- Display loading, error, empty, and success states clearly.
- Render structured result sections for summary, test cases, generated code, evidence, and warnings.
- Provide copy actions for generated code and useful result blocks.
- Keep the visual design professional, compact, and developer-oriented.

## Non-Goals

- A marketing-first landing page that delays access to the generator.
- Authentication, accounts, billing, dashboards, saved history, or project management.
- File upload unless a later spec or sprint adds it.
- In-browser execution of generated tests or user code.
- Large instructional content that distracts from the primary tool.

## Current State

Verified repository state on 2026-05-04:

- No frontend source tree exists.
- No frontend framework, package file, Tailwind setup, routes, or components exist yet.
- `docs/references/letter.md` defines the desired frontend responsibilities, visual direction, and result layout.
- SPEC-002 governs product scope and SPEC-003 governs the backend response contract.

## Proposed Approach

1. Build a single app-first page where the generator is immediately available.
2. Use React or Next.js with TypeScript and Tailwind CSS unless an implementation sprint verifies a simpler approach is better.
3. Keep layout compact: header, input panel, result panel, and secondary context below the main workflow if needed.
4. Render structured backend JSON into distinct sections instead of one free-form response.
5. Include copy buttons for generated code and key output sections.
6. Handle errors from validation, missing API key, LLM failure, invalid output, vector store failure, no relevant chunks, and request size limits.

## Architecture / Data / Flow Notes

Primary fields:

- `project_context`: large text area.
- `target_name`: optional text input.
- `test_framework`: selector with Pytest and Jest/Supertest.
- `selected_test_types`: first-class dropdown multi-select for supported test type categories.
- `extra_instructions`: optional text area.
- Scenario groups: superseded frontend preset controls from SPRINT-009; SPRINT-010 replaces them with selected test types.

Primary actions:

- `Generate Tests`
- Copy generated code.
- Copy result block when implemented cleanly.

Result sections:

- Summary.
- Test cases with type badge, name, expected result, and reason.
- Generated code in a code-style block.
- Evidence snippets with source labels.
- Warnings in a clear callout.

Expected states:

- Empty state before generation.
- Loading state while the request is in flight.
- Success state with structured results.
- Error state with readable backend error text.
- Validation state for missing or too-short context.

Visual direction:

- Dark professional developer-tool interface.
- Clean panels, compact cards, code-style blocks, badges, and strong spacing.
- Subtle accent color, avoiding overly decorative or neon styling.
- Responsive layout for desktop and mobile.

## Invariants

- The first screen should expose the usable generator, not only product explanation.
- Generated results must remain visibly reviewable and should not imply correctness beyond the provided evidence.
- Evidence and warnings must be first-class result sections.
- The frontend must not execute generated code.
- The frontend must not expose secrets.
- The frontend must not claim integrations or capabilities that are not implemented.
- UI copy should avoid carrying over damaged encoded characters from `docs/references/letter.md`.

## Risks

- A hero/landing-page structure could delay the core workflow and make the app feel less useful.
- Dense generated output could become hard to scan without clear grouping.
- Long code blocks or snippets could break mobile layouts if not constrained.
- The UI could imply generated tests are authoritative instead of reviewable recommendations.
- Copy actions could be added before output state is stable, creating edge-case bugs.

## Verification Strategy

- Frontend build and lint commands once the frontend package exists.
- Manual browser check on desktop and mobile viewports.
- Verify the form can submit a valid request to the backend.
- Verify validation and error states render cleanly.
- Verify result sections render from the structured `GenerateTestsResponse` schema.
- Verify long generated code and long evidence snippets do not overflow or overlap.
- Verify copy buttons copy the intended text and are disabled or hidden when content is absent.

## Sprint Plan

1. Frontend foundation sprint: create app shell, layout, form fields, framework selector, and local mock result rendering.
2. Frontend integration sprint: connect to `/api/generate-tests`, handle loading/errors, render real backend response.
3. Frontend polish sprint: responsive checks, copy actions, spacing, accessibility labels, and result readability.

## Rollout / Sequencing Notes

The frontend should follow the backend schema from SPEC-003. If the backend contract changes, update this spec or the governing sprint before implementation claims frontend completion.

## Completion Criteria

- User can enter context and select Pytest or Jest/Supertest.
- User can submit the form and see loading feedback.
- Successful responses render summary, test cases, generated code, evidence, and warnings.
- Errors are shown in a clean callout.
- Generated code can be copied.
- Mobile and desktop layouts are usable without overlapping text or broken blocks.
- The frontend does not execute user or generated code.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-004
- **Spec ID:** SPEC-004
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-004-testpilot-ai-frontend-ux.md`

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

- The final frontend framework choice should be confirmed in the first frontend implementation sprint after checking the repository state at that time.

### Final QA Summary

- **What was checked:** Frontend goals, non-goals, states, result rendering, visual direction, and verification strategy were checked against SPEC-002, SPEC-003, and `docs/references/letter.md`.
- **What was fixed:** The spec keeps the app-first generator workflow as the first screen while preserving the letter's requirement for a polished developer-tool feel, and `Related Sprints` was updated after SPRINT-006 was planned.
- **Residual risks:** Actual UI quality depends on implementation-time browser verification.
- **Recommendation:** Ready.

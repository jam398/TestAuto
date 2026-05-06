# Sprint: Frontend MVP

## Metadata

- **ID:** SPRINT-006
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** SPEC-004 defines the frontend UX, and this sprint is a bounded UI implementation slice dependent on the backend response contract.

## Goal

Build the app-first frontend MVP for entering context, selecting a framework, generating tests, and rendering structured results.

## Governing Spec

`docs/specs/spec-004-testpilot-ai-frontend-ux.md`

## Carry-Forward Context

SPEC-004 defines the app-first frontend workflow. SPEC-003 defines the response schema the frontend must render. SPRINT-005 completed the validated `/api/generate-tests` backend path before frontend implementation began.

## Scope

In scope:

- Frontend project setup.
- App-first page layout.
- Input form with context, optional target name, framework selector, and optional extra instructions.
- Generate button, loading state, validation state, error callout, and success state.
- Structured rendering for summary, test cases, generated code, evidence, and warnings.
- Copy action for generated code.
- Basic responsive layout checks.

Out of scope:

- User accounts, dashboards, saved history, or payments.
- File upload.
- Running generated tests in the browser.
- GitHub or CI integration.
- Marketing-only landing page.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Frontend spec | `docs/specs/spec-004-testpilot-ai-frontend-ux.md` | Governing spec | Verified present and read. |
| Backend spec | `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md` | API contract | Verified present and read. |
| Product spec | `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md` | Product scope | Verified present and read. |
| Project letter | `docs/references/letter.md` | Source brief | Verified present and read; damaged encoding must not be copied into UI text. |
| Repository root | `.` | Live app state | Verified no `frontend/` source tree exists. |

## Files Expected To Change

- `frontend/package.json`
- `frontend/README.md`
- `frontend/index.html`
- `frontend/src/main.tsx`
- `frontend/src/App.tsx`
- `frontend/src/components/TestGeneratorForm.tsx`
- `frontend/src/components/ResultsPanel.tsx`
- `frontend/src/components/CodeBlock.tsx`
- `frontend/src/components/StatusCallout.tsx`
- `frontend/src/lib/api.ts`
- `frontend/src/types.ts`
- `frontend/src/styles.css`
- `frontend/tailwind.config.*`
- `frontend/tsconfig.json`
- `frontend/vite.config.*` or equivalent framework config
- `backend/app/main.py`

## Ordered Tasks

### Task 1. Scaffold Frontend

- **Objective:** Create a TypeScript frontend application with styling setup.
- **Files:** `frontend/package.json`, `frontend/index.html`, `frontend/src/main.tsx`, config files
- **Changes:** Add React or equivalent verified setup, TypeScript, and Tailwind or equivalent styling pipeline.
- **Unchanged:** No backend changes unless required for CORS or documented API compatibility.
- **Verify After:** Run frontend install/build checks in the implementation environment.

### Task 2. Build App-First Layout And Form

- **Objective:** Expose the generator workflow immediately.
- **Files:** `frontend/src/App.tsx`, `frontend/src/components/TestGeneratorForm.tsx`, `frontend/src/styles.css`
- **Changes:** Add header, context textarea, optional target field, framework selector, extra instructions, and generate action.
- **Unchanged:** No file upload or auth.
- **Verify After:** Manual browser check confirms the generator is visible on first screen.

### Task 3. Add API Client And States

- **Objective:** Connect the form to `/api/generate-tests` with predictable state handling.
- **Files:** `frontend/src/lib/api.ts`, `frontend/src/types.ts`, `frontend/src/App.tsx`, `frontend/src/components/StatusCallout.tsx`
- **Changes:** Add request/response types, loading state, client-side validation, backend error display, and empty state.
- **Unchanged:** No real secrets in frontend code.
- **Verify After:** Test valid and invalid requests against the backend.

### Task 4. Render Structured Results

- **Objective:** Display generated output as reviewable sections.
- **Files:** `frontend/src/components/ResultsPanel.tsx`, `frontend/src/components/CodeBlock.tsx`
- **Changes:** Render summary, typed test cases, generated code, evidence snippets, warnings, and copy generated code.
- **Unchanged:** Do not execute generated code.
- **Verify After:** Browser check with long code and long evidence snippets.

### Task 5. Responsive And Copy Checks

- **Objective:** Confirm the MVP works on desktop and mobile.
- **Files:** Frontend components and styles as needed.
- **Changes:** Adjust layout, spacing, overflow, and disabled/empty states.
- **Unchanged:** No decorative overbuild or marketing-only layout.
- **Verify After:** Desktop and mobile viewport checks.

## Product Rules

- The generator is the primary first-screen experience.
- Evidence and warnings are first-class result sections.
- Generated tests are recommendations and must remain visibly reviewable.
- Do not execute generated code.
- Do not claim unsupported integrations.
- Do not copy damaged encoded characters from `letter.md`.

## Deliverables

- Frontend app shell.
- Test generation form.
- API client.
- Loading, error, empty, and success states.
- Structured results panel.
- Copy generated code action.
- Responsive MVP layout.

## Acceptance Criteria

- User can enter context and select Pytest or Jest/Supertest.
- User can submit the form and see loading feedback.
- Successful responses render summary, test cases, generated code, evidence, and warnings.
- Backend validation errors render in a clean callout.
- Generated code can be copied.
- Mobile and desktop layouts are usable without overlapping text or broken blocks.
- The frontend never executes generated code.

## Dependencies / Blockers

- SPRINT-005 should be completed before final backend integration is claimed complete.

## Risks / Watchouts

- Frontend setup should not introduce a large framework burden for the MVP.
- Long generated code can overflow if code blocks are not constrained.
- The UI must not imply the AI output is guaranteed correct.

## Sprint Boundary Check

This sprint builds the usable frontend MVP and integrates with the backend contract. It does not add future product features.

## Verification

- Automated verification 1: `npm.cmd --prefix frontend run build`
- Automated verification 2: `npm.cmd --prefix frontend run lint`
- Manual verification 1: Desktop browser check at 1440x900 for form, loading, error, and result states.
- Manual verification 2: Mobile browser check at 390x844 for no overlap, usable controls, and readable code/evidence sections.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-006
- **Sprint ID:** SPRINT-006
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-006-frontend-mvp.md`
- **Spec Path:** `docs/specs/spec-004-testpilot-ai-frontend-ux.md`

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
- **Manual:** Sprint document reviewed against frontend UX, backend contract, and product non-goals.

### Carry-Forward Updates

- PowerShell blocks `npm.ps1` in this environment, so frontend verification should use `npm.cmd`.

### Final QA Summary

- **What was checked:** Frontend scope, result sections, responsive checks, copy behavior, and non-goals.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Actual UI quality depends on browser verification during implementation.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** PowerShell blocks `npm.ps1`, so all npm verification used `npm.cmd`. Initial Playwright copy-state check needed clipboard permission in the browser context. Mobile viewport verification found horizontal overflow caused by grid item minimum widths; CSS was fixed with `min-width: 0` on the workspace, panels, and form controls.
- **Final Verification Results:** `npm.cmd --prefix frontend install` completed successfully. `npm.cmd --prefix frontend run build` passed. `npm.cmd --prefix frontend run lint` passed. `python -m pytest backend/app/tests` passed with 35 tests after adding frontend CORS support. Browser verification passed at 1440x900 and 390x844 against local backend/frontend dev servers, including form submit, loading/result flow, summary, test cases, starter code, evidence, warnings, copy button state, generate button dimensions, and no horizontal overflow. Backend-style error rendering was verified with a Playwright route mock returning HTTP 422. Frontend scans found no hardcoded secrets and no generated-code execution path.
- **Deviations From Plan:** Added `backend/app/main.py` CORS middleware for localhost frontend integration. Added `@playwright/test` as a frontend dev dependency so browser verification is reproducible. Used custom CSS with Tailwind configured and exercised instead of utility-first Tailwind styling.
- **Carry-Forward Updates For Next Sprint:** SPRINT-007 should add root documentation, `.gitignore`, environment examples, final fixture, and final verification. Local dev servers are available at `http://127.0.0.1:5173` and `http://127.0.0.1:8000` during this implementation session.

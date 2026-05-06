# Sprint: Test Scenario Presets

## Metadata

- **ID:** SPRINT-009
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** SPEC-006 defines the scenario preset UX and keeps the work bounded to frontend request guidance.

## Goal

Add selectable scenario groups to make common test-generation instructions easier to remember and reuse.

## Governing Spec

`docs/specs/spec-006-test-scenario-presets.md`

## Carry-Forward Context

The current form has a free-form `extra_instructions` field. Backend prompt construction already uses that field, so scenario presets can be composed into it without changing the backend API schema.

## Scope

In scope:

- Scenario group preset controls in the frontend form.
- Combining selected presets with user extra instructions during submit.
- Styling for desktop and mobile layouts.
- README note about scenario groups.

Out of scope:

- Backend request schema changes.
- Persisting custom presets.
- Running generated tests.
- User accounts, saved history, or analytics.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Frontend spec | `docs/specs/spec-004-testpilot-ai-frontend-ux.md` | Parent UX spec | Requires app-first form and structured output. |
| Scenario spec | `docs/specs/spec-006-test-scenario-presets.md` | Governing spec | Created and QA passed. |
| Form component | `frontend/src/components/TestGeneratorForm.tsx` | Main edit target | Currently has context, target, framework, extra instructions. |
| Styles | `frontend/src/styles.css` | UI styling | Current form uses compact dark panel styles. |

## Files Expected To Change

- `frontend/src/components/TestGeneratorForm.tsx`
- `frontend/src/styles.css`
- `README.md`
- `docs/specs/spec-004-testpilot-ai-frontend-ux.md`
- `docs/specs/spec-002-testpilot-ai-mvp-product-scope.md`
- `docs/sprints/completed/sprint-009-test-scenario-presets.md`

## Ordered Tasks

### Task 1. Add Preset Data And Request Composition

- **Objective:** Define scenario presets and include selected guidance in submitted extra instructions.
- **Files:** `frontend/src/components/TestGeneratorForm.tsx`
- **Changes:** Add preset definitions, selected state, toggle handling, and composed submit instructions.
- **Unchanged:** Keep `extra_instructions` field and backend request shape.
- **Verify After:** Run frontend type checking.

### Task 2. Add Preset UI Styling

- **Objective:** Render compact toggle controls that work on desktop and mobile.
- **Files:** `frontend/src/styles.css`
- **Changes:** Add chip grid, active state, and text wrapping rules.
- **Unchanged:** Do not redesign the full app.
- **Verify After:** Run frontend build and browser checks.

### Task 3. Update Durable Docs

- **Objective:** Record the current workflow and verification.
- **Files:** `README.md`, specs, this sprint
- **Changes:** Document that scenario groups supplement extra instructions.
- **Unchanged:** Do not claim persistence or execution.
- **Verify After:** Manual doc review.

## Product Rules

- Presets guide generation only.
- Presets must not imply generated tests are executed.
- Free-form instructions remain available.
- Multiple presets can be selected together.

## Deliverables

- Scenario preset toggles.
- Composed extra instructions submission.
- Updated docs and QA.

## Acceptance Criteria

- User can select and deselect multiple scenario groups.
- Selected scenario groups are included in `extra_instructions` when submitting.
- User-written extra instructions are preserved.
- Frontend build and lint pass.
- Browser check confirms the UI renders and submits.

## Dependencies / Blockers

- None.

## Risks / Watchouts

- Long preset labels must not overflow on mobile.
- Preset instructions must not overpromise unsupported behavior.

## Sprint Boundary Check

This sprint is a frontend guidance enhancement. It does not change backend generation, execute tests, or add persistence.

## Verification

- Automated verification 1: `npm.cmd --prefix frontend run build`
- Automated verification 2: `npm.cmd --prefix frontend run lint`
- Manual/browser verification 1: Desktop browser check for selecting presets and submitting.
- Manual/browser verification 2: Mobile viewport check for preset wrapping and no overlap.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-009
- **Sprint ID:** SPRINT-009
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-009-test-scenario-presets.md`
- **Spec Path:** `docs/specs/spec-006-test-scenario-presets.md`

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
- **Manual:** Sprint document and implementation reviewed against SPEC-006 and current frontend files.

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** Scope, task order, acceptance criteria, and verification commands.
- **What was fixed:** No sprint doc fixes were required.
- **Residual risks:** Preset wording may need tuning after user feedback.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** None.
- **Final Verification Results:** `npm.cmd --prefix frontend run build` passed. `npm.cmd --prefix frontend run lint` passed. Desktop browser automation confirmed seven scenario chips render, selected groups are included in the submitted `extra_instructions`, free-form extra instructions are preserved, and result rendering still works. Mobile browser automation at 390x844 confirmed seven chips render with no horizontal overflow and body scroll width equals viewport width.
- **Deviations From Plan:** None.
- **Carry-Forward Updates For Next Sprint:** Scenario preset wording can be tuned after more real generation examples, but no blocking gap remains.

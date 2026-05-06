# Spec: Test Scenario Presets

## Metadata

- **ID:** SPEC-006
- **Status:** Superseded by SPEC-007
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** SPEC-004
- **Related Sprints:** SPRINT-009

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** Scenario presets change the primary generation workflow, user controls, and prompt guidance while preserving the existing backend request contract.

## Problem Statement

Users know they want different categories of tests, but remembering how to phrase those categories in extra instructions creates friction. The app should expose common scenario groups as selectable controls while still allowing free-form extra instructions.

## Goals

- Add scenario-group controls to the generator form.
- Preserve the existing `extra_instructions` text area.
- Compose selected scenario groups into the submitted `extra_instructions`.
- Keep the backend API contract stable unless a later sprint needs first-class scenario fields.
- Make the controls compact and understandable without turning the app into a tutorial.

## Non-Goals

- Persisting user presets.
- Adding accounts, saved projects, or history.
- Executing generated tests.
- Replacing the free-form extra instructions field.
- Adding backend database or analytics.

## Current State

Verified after SPRINT-010 on 2026-05-04:

- SPRINT-009 implemented frontend-only scenario chips for this spec.
- SPRINT-010 replaced those chips with first-class selected test type controls governed by SPEC-007.
- `frontend/src/components/TestGeneratorForm.tsx` now has project context, target, framework, selected test type dropdown, and additional instructions.
- `GenerateTestsRequest` supports structured `selected_test_types` plus optional `extra_instructions`.
- Backend prompt builder includes selected test types and additional instructions.
- No scenario preset chip controls remain in the active UI.

## Proposed Approach

1. Add a small list of curated scenario groups in the frontend form.
2. Render them as toggleable chips with clear labels.
3. Combine selected preset instructions with free-form extra instructions during submit.
4. Keep the payload shape unchanged by sending the combined text through `extra_instructions`.
5. Verify the UI remains responsive and that generated requests include selected scenario guidance.

## Architecture / Data / Flow Notes

Initial scenario groups:

- Happy path.
- Required fields.
- Boundary values.
- Type validation.
- Combined invalid input.
- Error response shape.
- Framework fixture.

The submitted `extra_instructions` should contain both selected preset guidance and any user-written instructions.

## Invariants

- Presets must not imply generated tests are executed.
- Presets must not invent auth, persistence, or deployment behavior.
- Free-form extra instructions remain available.
- The backend request schema remains compatible.
- UI controls must not overflow on mobile.

## Risks

- Too many presets could clutter the form.
- Preset wording could over-constrain the model or cause unsupported assumptions.
- Users might confuse presets with guaranteed coverage unless warnings/evidence remain visible.

## Verification Strategy

- Frontend build and TypeScript lint.
- Browser check that presets can be toggled and submitted.
- Browser check that layout remains usable on desktop and mobile widths.
- Manual review that preset wording stays focused on generation guidance only.

## Sprint Plan

1. SPRINT-009: Implement scenario presets in the frontend form and verify the generation request flow.

## Rollout / Sequencing Notes

Keep this frontend-only unless future feedback shows the backend needs analytics, schema-level scenario fields, or output grouping.

## Supersession Note

SPEC-007 supersedes this frontend-only scenario preset direction with first-class selected test types in the backend request and response contract. SPRINT-010 replaced the scenario chips rather than keeping both controls.

## Completion Criteria

- Scenario groups render in the form.
- Multiple groups can be selected and deselected.
- Free-form extra instructions remain editable.
- Submitted request includes selected scenario guidance.
- Build, lint, and browser checks pass.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-006
- **Spec ID:** SPEC-006
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-006-test-scenario-presets.md`

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

- **What was checked:** Scope, UX behavior, backend contract preservation, and verification plan.
- **What was fixed:** The spec explicitly keeps presets frontend-only and preserves free-form instructions.
- **Residual risks:** Preset wording may need tuning after real generation examples.
- **Recommendation:** Ready.

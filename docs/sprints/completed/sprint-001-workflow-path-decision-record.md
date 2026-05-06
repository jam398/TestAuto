# Sprint: Workflow Path Decision Record

## Metadata

- **ID:** SPRINT-001
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04

## Workflow Path Decision

- **Chosen Path:** Full Spec
- **Reason:** This updates workflow reference templates and affects how future agents record artifact decisions.

## Goal

Add a concise path decision record to workflow templates and reference guidance.

## Governing Spec

`docs/specs/spec-001-workflow-path-decision-record.md`

## Carry-Forward Context

No prior specs or sprints existed in the repository before this sprint. The governing spec records that absence and the live reference files checked.

## Scope

In scope:

- Add workflow path decision guidance to workflow references.
- Add a workflow path decision section to spec, sprint, and change note templates.
- Record verification in this sprint artifact.

Out of scope:

- Changing the path selection criteria.
- Creating unrelated workflow categories.
- Reading or changing `docs/references/letter.md`.

## Available Assets / Current State

| Asset | Path | Role | Notes |
|-------|------|------|-------|
| Agent entry rules | `AGENTS.md` | Repository entry instructions | Verified present and read. |
| Workflow quickstart | `docs/references/WORKFLOW_QUICKSTART.md` | Path selection summary | Verified present and read. |
| Workflow agreement | `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md` | Durable workflow rules | Verified present and read. |
| Spec template | `docs/references/SPEC_TEMPLATE.md` | Spec scaffold | Verified present and read. |
| Sprint template | `docs/references/SPRINT_TEMPLATE.md` | Sprint scaffold | Verified present and read. |
| Change note template | `docs/references/CHANGE_NOTE_TEMPLATE.md` | Lightweight change scaffold | Verified present and read. |

## Files Expected To Change

- `docs/references/WORKFLOW_QUICKSTART.md`
- `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
- `docs/references/SPEC_TEMPLATE.md`
- `docs/references/SPRINT_TEMPLATE.md`
- `docs/references/CHANGE_NOTE_TEMPLATE.md`
- `docs/specs/spec-001-workflow-path-decision-record.md`
- `docs/sprints/active/sprint-001-workflow-path-decision-record.md`

## Ordered Tasks

### Task 1. Update Reference Guidance

- **Objective:** Make path decision recording part of the workflow guidance.
- **Files:** `docs/references/WORKFLOW_QUICKSTART.md`, `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
- **Changes:** Add concise guidance requiring artifacts to record chosen path and reason.
- **Unchanged:** Existing path criteria and required phases.
- **Verify After:** Search for `Workflow Path Decision` in both reference files.

### Task 2. Update Templates

- **Objective:** Give future artifacts a stable place to record path choice.
- **Files:** `docs/references/SPEC_TEMPLATE.md`, `docs/references/SPRINT_TEMPLATE.md`, `docs/references/CHANGE_NOTE_TEMPLATE.md`
- **Changes:** Add a `Workflow Path Decision` section with `Chosen Path` and `Reason`.
- **Unchanged:** Existing metadata, QA sections, and completion rules.
- **Verify After:** Search for `Workflow Path Decision` in all three templates.

### Task 3. Record Implementation QA

- **Objective:** Close this sprint with verified results.
- **Files:** `docs/sprints/active/sprint-001-workflow-path-decision-record.md`
- **Changes:** Replace pending QA values with verification results.
- **Unchanged:** Scope and non-goals.
- **Verify After:** Confirm the QA report no longer says pending.

## Product Rules

- Keep workflow records embedded in governing artifacts.
- Do not change the meaning of existing workflow paths.
- Do not read or modify `docs/references/letter.md`.

## Deliverables

- Updated workflow references.
- Updated spec, sprint, and change note templates.
- Completed sprint QA report.

## Acceptance Criteria

- `Workflow Path Decision` appears in the quickstart, workflow agreement, spec template, sprint template, and change note template.
- The new template section records a chosen path and a reason.
- The sprint records verification results.

## Dependencies / Blockers

- None.

## Risks / Watchouts

- Template wording must not imply that path choice is optional.
- The lightweight path must remain limited to narrow, low-risk, directly verifiable work.

## Sprint Boundary Check

This sprint is bounded to documentation and template updates for recording workflow path decisions.

## Verification

- Automated verification 1: `rg "Workflow Path Decision" docs/references docs/specs docs/sprints`
- Automated verification 2: `rg "letter.md" docs/sprints/active/sprint-001-workflow-path-decision-record.md docs/specs/spec-001-workflow-path-decision-record.md`
- Manual verification 1: Review changed reference docs for unchanged path criteria.
- Manual verification 2: Confirm `docs/references/letter.md` was not read or changed during this sprint.

## Completion Checklist

- [x] All in-scope tasks implemented
- [x] Non-goals preserved
- [x] Carry-forward constraints respected
- [x] Acceptance criteria met
- [x] Verification passed
- [x] No known blocking gaps remain

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-001
- **Sprint ID:** SPRINT-001
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifacts

- **Sprint Path:** `docs/sprints/completed/sprint-001-workflow-path-decision-record.md`
- **Spec Path:** `docs/specs/spec-001-workflow-path-decision-record.md`

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

- **Automated:** Not run yet
- **Manual:** Not run yet

### Carry-Forward Updates

- None.

### Final QA Summary

- **What was checked:** Sprint scope, task order, expected files, acceptance criteria, and verification commands.
- **What was fixed:** No sprint doc fixes were required before implementation.
- **Residual risks:** The update is documentation-only, but it affects future workflow behavior.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** One wording mismatch was found: the workflow agreement described the path decision concept but did not include the exact `Workflow Path Decision` section name. It was fixed before final verification.
- **Final Verification Results:** `rg "Workflow Path Decision" docs\references docs\specs docs\sprints` passed and found the new section/guidance in the expected reference files. `rg -n "Full Spec Path|Sprint-First Path|Lightweight Change Note Path|Do not use a change note|Required phases|Workflow Path Decision" docs\references\WORKFLOW_QUICKSTART.md docs\references\WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md` passed and confirmed existing path criteria remain present. Manual review confirmed `docs/references/letter.md` was not read or changed.
- **Deviations From Plan:** None.
- **Carry-Forward Updates For Next Sprint:** Future artifacts should include `Workflow Path Decision` when created from the updated templates.

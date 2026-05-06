# Spec: Workflow Path Decision Record

## Metadata

- **ID:** SPEC-001
- **Status:** Active
- **Owner:** Codex
- **Created:** 2026-05-04
- **Last Updated:** 2026-05-04
- **Parent Spec:** None
- **Related Sprints:** SPRINT-001

## Problem Statement

The repository requires agents to choose between the full spec path, sprint-first path, and lightweight change note path. The current workflow describes when to use each path, but the templates do not provide a consistent place to record why a path was chosen. This makes later review harder, especially when an agent chooses a lighter path.

## Goals

- Add a concise workflow path decision field to relevant durable artifact templates.
- Make path choice auditable without adding detached records.
- Keep the change limited to workflow documentation and templates.

## Non-Goals

- Redesign the workflow agreement.
- Change the criteria for full spec, sprint-first, or lightweight paths.
- Modify `docs/references/letter.md`.

## Current State

Verified repository state on 2026-05-04:

- `AGENTS.md` requires agents to choose the right path and use the heavier path when in doubt.
- `docs/references/WORKFLOW_QUICKSTART.md` describes the three paths but does not require a path decision field in templates.
- `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md` defines artifact roles and required phases but does not define where to record path choice.
- `docs/references/SPEC_TEMPLATE.md`, `docs/references/SPRINT_TEMPLATE.md`, and `docs/references/CHANGE_NOTE_TEMPLATE.md` do not include a dedicated workflow path decision section.

## Proposed Approach

1. Add a short `Workflow Path Decision` section to the spec, sprint, and change note templates.
2. Update the workflow quickstart and agreement so the new section is expected when creating or updating artifacts.
3. Keep wording narrow: the field records the chosen path and reason; it does not change path eligibility rules.

## Architecture / Data / Flow Notes

- Reference docs live under `docs/references/`.
- Specs live under `docs/specs/`.
- Sprint artifacts live under `docs/sprints/planned/`, `docs/sprints/active/`, and `docs/sprints/completed/`.
- QA remains embedded in the governing artifact.

## Invariants

- The durable artifact remains the source of truth.
- Path choice must not be used to bypass required phases.
- `docs/references/letter.md` remains unread and unchanged for this work.

## Risks

- Adding the field to too many places could create redundant boilerplate.
- Weak wording could imply agents may choose paths arbitrarily.

## Verification Strategy

- Confirm the expected reference files contain `Workflow Path Decision`.
- Confirm `docs/references/letter.md` was not read or changed.
- Confirm the sprint QA report records the verification result.

## Sprint Plan

1. SPRINT-001 updates the reference docs and records implementation QA.

## Rollout / Sequencing Notes

This documentation change takes effect immediately for future artifacts after the reference docs are updated.

## Completion Criteria

- Relevant templates include a `Workflow Path Decision` section.
- Workflow references explain that path decisions should be recorded.
- Implementation QA is recorded in SPRINT-001.

## Spec QA Record

### Metadata

- **QA ID:** SPEC-QA-001
- **Spec ID:** SPEC-001
- **Reviewer:** Codex
- **Date:** 2026-05-04
- **Verdict:** PASS

### Governing Artifact

- **Spec Path:** `docs/specs/spec-001-workflow-path-decision-record.md`

### QA Scope

This QA pass reviewed:

- problem statement quality
- goal and non-goal clarity
- current-state accuracy
- proposed approach coherence
- risk, invariant, and truth-rule coverage
- verification and sprint-plan completeness

### Checks Performed

- [x] Read the full spec
- [x] Compared claims against the live repository where applicable
- [x] Checked for ambiguity, contradictions, and missing requirements
- [x] Checked whether risks, invariants, and verification are concrete
- [x] Checked whether sprint plan is bounded and sequenced sensibly

### Findings

None.

### Open Questions

- None.

### Final QA Summary

- **What was checked:** The proposed workflow-template update was checked against the live reference files present on 2026-05-04.
- **What was fixed:** No spec fixes were required before implementation.
- **Residual risks:** The new field adds minor template overhead.
- **Recommendation:** Ready.

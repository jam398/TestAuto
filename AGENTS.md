# AGENTS

This file is the single entry document for any agent, LLM, or automation working in this repository.

## Purpose

This repository uses durable workflow artifacts as the system of record. Agents must follow the documented workflow instead of relying on chat memory or inferred context.

## Read Order

Before meaningful work, read in this order:

1. `AGENTS.md`
2. `docs/references/WORKFLOW_QUICKSTART.md`
3. `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
4. The relevant spec, sprint, or change note
5. Any prior embedded QA section or carry-forward notes for the same area
6. The live files the artifact claims to govern

## Non-Negotiable Rules

### 1. Use the right path

- Full path for foundational, architectural, ambiguous, or high-impact work
- Sprint-first path for bounded medium work that still needs planning and QA
- Lightweight path only for narrow, low-risk, directly verifiable work

When in doubt, use the heavier path.

### 2. Do not skip artifact phases

If the chosen path requires spec QA, sprint QA, implementation QA, or recorded verification, do not skip those phases. Record them inside the governing artifact rather than creating detached QA files.

### 3. Read before writing

Do not draft or edit from assumptions. Read the governing artifacts and verify the live repository state first.

### 4. Verify before claiming completion

Do not mark work complete because it looks done. Completion requires recorded verification and QA.

### 5. Preserve durable artifacts

Specs, sprints, change notes, and QA reports are part of the implementation system. Keep them accurate and up to date when verified state changes.

## Accuracy Rules

- Verify commands against the live repository before documenting or running them
- Verify file paths against the current workspace
- Verify implementation state before describing behavior in docs or QA
- Do not describe planned work as already implemented
- Remove stale future-state wording once the work becomes current state

## No False Authority

- Do not present polished but unverified claims as facts
- Do not treat AI-generated output as trustworthy without verification
- Do not use frameworks, names, or patterns as status markers without tying them to a concrete repository rule or behavior

## Scope Discipline

- No unrelated features or refactors
- No rewriting adjacent systems without approval
- No helpful expansion that changes the agreed scope
- Keep work bounded to the governing artifact

## Expected Agent Behavior

Agents working here should:

- read before writing
- verify before claiming completion
- preserve durable artifacts
- keep scope tight
- prefer explicit evidence over confidence
- update governing artifacts when verified state changes

## Workflow References

- `docs/references/WORKFLOW_QUICKSTART.md`
- `docs/references/WORKFLOW_AGREEMENT_SPEC_SPRINT_QA.md`
- `docs/references/SPEC_TEMPLATE.md`
- `docs/references/SPRINT_TEMPLATE.md`
- `docs/references/CHANGE_NOTE_TEMPLATE.md`
- `docs/references/SPEC_QA_TEMPLATE.md` (embedded section template)
- `docs/references/SPRINT_QA_TEMPLATE.md` (embedded section template)
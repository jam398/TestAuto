# Change Note: Browser E2E QA And Test Case Input Display

## Metadata

- **ID:** CHANGE-002
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-06
- **Last Updated:** 2026-05-06

## Workflow Path Decision

- **Chosen Path:** Lightweight Change Note
- **Reason:** This was a narrow browser QA pass and small result-card display improvement. It did not change backend contracts, deployment architecture, or generation behavior.

## Reason For Change

Browser QA confirmed that OpenAI generation returns useful structured output, evidence, warnings, and non-empty starter code for multiple API contexts. The QA also found one UI gap: `TestCase.input` was returned by the backend but not displayed in the result cards.

## Scope

In scope:

- Display each generated test case input/scenario in the result card.
- Add wrapping rules so long endpoints and generated text do not create horizontal overflow.
- Run real browser E2E checks with multiple API contexts.
- Run mocked layout stress checks for desktop and mobile result rendering.

Out of scope:

- Executing generated tests.
- Changing the backend generation schema.
- Adding Playwright back to the committed frontend package or CI workflow.

## Files Expected To Change

- `frontend/src/components/ResultsPanel.tsx`
- `frontend/src/styles.css`
- `docs/change-002-browser-e2e-qa-test-case-input.md`

## Change Summary

Completed. Result cards now show `Input`, `Expected`, and `Why`. Long test names, inputs, expected results, reasons, evidence, and warnings wrap safely.

## Risk Level

- **Risk:** Low
- **Reason:** The change renders an already-required response field and adds CSS wrapping only.

## Verification

- `npm.cmd --prefix frontend run lint`
- `npm.cmd --prefix frontend run build`
- Browser E2E real OpenAI pass through the running frontend/backend for:
  - `POST /api/debts` with Jest/Supertest
  - `PATCH /api/products/{id}` with Pytest
  - multi-endpoint RAG context targeting `GET /api/users/{id}`
- Browser mocked layout stress check at `1440x1100` and `390x844`

## QA Record

- **Reviewer:** Codex
- **Date:** 2026-05-06
- **Checks Performed:** Verified non-empty code, provider mode, selected types, summary, test cases, evidence, warnings, copy button state, target focus, desktop overflow, mobile overflow, and result-section usefulness.
- **Result:** PASS. Real OpenAI E2E produced non-empty starter code for all three API contexts. Evidence matched the relevant context, including RAG retrieval focusing on `GET /api/users/{id}` while ignoring unrelated payment/session chunks. Mocked layout checks confirmed no horizontal overflow on desktop or mobile after the wrapping fix.
- **Carry-Forward Notes:** The UI now serves the review workflow better by showing test inputs directly. Future QA should still review generated starter code manually before use because the app does not execute tests.

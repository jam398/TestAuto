# Sprint: Deployment Readiness For Render And GitHub Pages

## Metadata

- **ID:** SPRINT-012
- **Status:** Completed
- **Owner:** Codex
- **Created:** 2026-05-05
- **Last Updated:** 2026-05-05

## Workflow Path Decision

- **Chosen Path:** Sprint-First
- **Reason:** Deployment readiness is bounded but affects backend runtime config, frontend build config, GitHub Actions, Render Blueprint config, and verification.

## Goal

Make the Render backend Blueprint and GitHub Pages frontend workflow deployable from the current repository layout.

## Governing Specs

- `docs/specs/spec-003-testpilot-ai-backend-rag-architecture.md`
- `docs/specs/spec-004-testpilot-ai-frontend-ux.md`

## Scope

In scope:

- Validate and adjust `render.yaml` for the backend service layout.
- Fix frontend CI TypeScript errors around `process` in Vite config.
- Verify GitHub Pages build base for the `TestAuto` repository path.
- Remove Playwright from the frontend deploy workflow per current project preference.
- Add configurable backend CORS origins for deployed frontend URLs.
- Add root pytest configuration so backend tests work from the repository root with `app.*` imports.

Out of scope:

- Actually deploying to Render or GitHub Pages.
- Adding custom domains.
- Adding persistent storage.
- Changing app product behavior.

## Files Expected To Change

- `render.yaml`
- `.github/workflows/frontend-deploy.yml`
- `frontend/vite.config.ts`
- `frontend/package.json`
- `frontend/package-lock.json`
- `frontend/tsconfig.json`
- `backend/app/config.py`
- `backend/app/main.py`
- `backend/app/tests/test_config.py`
- `.gitignore`
- `pytest.ini`
- `README.md`
- `docs/sprints/completed/sprint-012-deployment-readiness-render-github-pages.md`

## Acceptance Criteria

- Frontend `npm run lint` passes.
- Frontend `npm run build` passes.
- Frontend GitHub Pages workflow does not install or run Playwright.
- Backend tests pass from the repository root.
- `render.yaml` matches the backend `app.main:app` import layout.
- Backend CORS can include a deployed GitHub Pages origin through environment configuration.
- README documents the Render/GitHub Pages deployment variables.

## Verification

- `python -m pytest backend/app/tests`
- `npm.cmd --prefix frontend run lint`
- `npm.cmd --prefix frontend run build`
- CI-style frontend build with `GITHUB_ACTIONS=true` and production `VITE_API_BASE_URL`

## Sprint Doc QA

### Metadata

- **QA ID:** SPRINT-QA-012
- **Sprint ID:** SPRINT-012
- **Reviewer:** Codex
- **Date:** 2026-05-05
- **Verdict:** PASS

### Checks Performed

- [x] Read governing workflow files
- [x] Read current deployment files
- [x] Compared Render config to backend import layout
- [x] Compared GitHub Pages workflow to frontend scripts
- [x] Checked official Render Blueprint, GitHub Pages workflow, and Vite GitHub Pages docs

### Findings

None.

### Final QA Summary

- **What was checked:** Scope, deployment targets, expected files, and concrete verification.
- **Recommendation:** Ready.

## QA Report

- **Verdict:** PASS
- **Reviewer:** Codex
- **Issues Found:** The original frontend workflow failed type checking because `process` was used in `vite.config.ts` without Node types in the frontend TypeScript config. Playwright was also removed from the workflow and package at the user's request.
- **Final Verification Results:** `python -m pytest backend/app/tests` passed with 56 tests. `python -c "from app.main import app; print(app.title)"` from `backend/` printed `TestPilot AI API`, matching the Render `rootDir: backend` and `uvicorn app.main:app` layout. `npm.cmd --prefix frontend run lint` passed. `npm.cmd --prefix frontend run build` passed. CI-style build with `GITHUB_ACTIONS=true` and `VITE_API_BASE_URL=https://testpilot-backend-q3wx.onrender.com` passed. Search confirmed no Playwright references remain in `frontend/package.json`, `frontend/package-lock.json`, `.github/workflows/frontend-deploy.yml`, or `frontend/tsconfig.json`.
- **Deviations From Plan:** Playwright preview testing was removed from scope after the user said it was not needed.
- **Carry-Forward Updates For Next Sprint:** After GitHub Pages deploys, verify the real Pages URL and set Render `ALLOWED_ORIGINS` to the exact origin. For a GitHub Pages project site, the CORS origin is `https://jam398.github.io`; the `/TestAuto/` path belongs in Vite `base`, not in CORS.

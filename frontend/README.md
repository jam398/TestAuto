# TestPilot AI Frontend

React and TypeScript frontend for TestPilot AI.

## Current Sprint State

This frontend implements the SPRINT-010 MVP:

- app-first test generation form
- Pytest and Jest/Supertest framework selector
- selected test type dropdown with supported coverage categories
- loading, validation, error, empty, and success states
- structured results for summary, test cases, generated code, evidence, and warnings
- copy action for generated code

The frontend does not execute generated tests or user-submitted code.

## Run Locally

From the repository root:

```bash
npm.cmd --prefix frontend install
npm.cmd --prefix frontend run dev
```

By default, the frontend calls same-origin `/api` routes, and Vite proxies them to `http://127.0.0.1:8000` during local development. Set `VITE_API_BASE_URL` only if the backend runs elsewhere or the frontend is deployed separately.

## Verify

```bash
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend run lint
```

# TestPilot AI

TestPilot AI is an AI-powered test case generator for backend APIs and software functions. Developers paste API documentation, validation rules, or function descriptions, and the app generates structured test plans, edge cases, starter test code, and evidence snippets from the provided context.

## What It Does

- Accepts pasted API, validation, README-style, or function context.
- Supports Pytest and Jest/Supertest output.
- Provides a selected test type dropdown for supported coverage categories while keeping free-form additional instructions.
- Generates a structured summary, test cases, starter code, evidence, and warnings.
- Rejects blank starter-code responses from the LLM instead of rendering an empty code block.
- Uses local chunking and deterministic retrieval to ground evidence in the provided context.
- Uses the OpenAI Responses API adapter when `OPENAI_API_KEY` is configured.
- Falls back to deterministic mock output when no API key is configured.
- Shows whether a result came from `mock` mode or `openai` mode.

The app treats user-submitted code and generated tests as text only. It does not execute either one.

## Tech Stack

- Backend: Python, FastAPI, Pydantic, Pytest
- Frontend: React, TypeScript, Vite, Tailwind-compatible CSS
- AI boundary: OpenAI Python SDK behind a mockable client abstraction
- Retrieval: local deterministic embeddings plus an in-memory vector store

## Architecture

```text
Frontend
  |
  | POST /api/generate-tests
  v
FastAPI Backend
  |
  | validate request
  | clean and chunk context
  | retrieve relevant chunks
  | build prompt with evidence
  | call LLM if configured, otherwise use deterministic mock output
  | validate structured response
  v
Frontend renders provider mode, selected test types, summary, tests, code, evidence, and warnings
```

## Setup

Install backend dependencies:

```bash
python -m pip install -r backend/requirements.txt
```

Install frontend dependencies:

```bash
npm.cmd --prefix frontend install
```

Configure environment values using `.env.example` or `backend/.env.example` as a reference:

```bash
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-5.4-mini
EMBEDDING_MODEL=text-embedding-3-small
ALLOWED_ORIGINS=http://localhost:5173,http://127.0.0.1:5173
VITE_API_BASE_URL=
```

For local frontend development, leaving `VITE_API_BASE_URL` empty makes Vite proxy `/api` requests to the local backend. For deployed frontend builds, set it to the deployed backend URL. For local backend development, put backend secrets in `backend/.env`. The backend loads that file automatically, and real process environment variables take precedence.

## Deploy

Backend deployment is configured with `render.yaml` for Render. The service uses `backend` as its root directory, installs `backend/requirements.txt`, and starts `uvicorn app.main:app`.

Set these Render environment variables:

```bash
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-5.4-mini
EMBEDDING_MODEL=text-embedding-3-small
ALLOWED_ORIGINS=https://jam398.github.io
```

The frontend deploy workflow is `.github/workflows/frontend-deploy.yml`. It builds the Vite app from `frontend`, sets `VITE_API_BASE_URL` to the Render backend URL, uploads `frontend/dist`, and deploys it to GitHub Pages. The Vite base path is `/TestAuto/` when running in GitHub Actions, matching the GitHub Pages repository path.

## Run

Start the backend:

```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Start the frontend:

```bash
npm.cmd --prefix frontend run dev
```

Open:

```text
http://127.0.0.1:5173
```

## Test

Backend:

```bash
python -m pytest backend/app/tests
```

Frontend:

```bash
npm.cmd --prefix frontend run build
npm.cmd --prefix frontend run lint
```

## Example Input

Target is optional. Leave it blank when the pasted context has one clear endpoint, function, or module. Fill it in when the context contains multiple APIs, or when you want one endpoint to be the principal focus. If target and additional instructions conflict, the target should remain primary and additional instructions should only add focus on top.

```text
POST /api/debts

Creates a new debt record for a user.

Required fields:
- name: string, required
- principal: number, must be greater than 0
- apr: number, must be between 0 and 100
- minimumPayment: number, must be greater than 0

Successful response:
- 201 Created
- returns id, name, principal, apr, minimumPayment, createdAt

Validation errors:
- 400 Bad Request
- returns a message describing invalid fields
```

Other API targets work the same way:

```text
Target:
PATCH /api/products/{id}

Project context:
PATCH /api/products/{id}

Updates product fields.

Request body:
- name: string, optional
- price: number, optional, must be greater than 0
- active: boolean, optional

Successful response:
- 200 OK
- returns id, name, price, active, updatedAt
```

```text
Target:
GET /api/users/{id}

Project context:
GET /api/users/{id}
- returns id, email, name, createdAt
- returns 404 Not Found if user does not exist

DELETE /api/sessions/{id}
- returns 204 No Content after deleting a session
```

In the second example, the target keeps generation focused on `GET /api/users/{id}` even though the pasted context also includes `DELETE /api/sessions/{id}`.

## Supported Test Types

| Test Type | What It Checks | Example |
| --- | --- | --- |
| API Endpoint | HTTP request/response behavior | POST creates a record |
| Validation | Required fields and input rules | Reject missing name |
| Negative | Bad or invalid input | Reject malformed body |
| Edge Case | Unusual but possible inputs | Empty string or zero |
| Boundary | Exact min/max limits | APR 0, 100, 100.01 |
| Contract / Schema | Response shape | Must include id and createdAt |
| Error Handling | Clean failure behavior | Invalid ID returns 404 |
| Smoke | Basic sanity checks | Health endpoint works |
| Unit | One function in isolation | calculateTotal returns correct value |
| Integration | Multiple parts working together | Create then fetch record |

## Example Output Shape

```json
{
  "provider_mode": "mock",
  "selected_test_types": [
    "api_endpoint",
    "validation",
    "negative",
    "edge_case",
    "contract_schema"
  ],
  "summary": "Generated mocked test plan for POST /api/debts.",
  "test_cases": [
    {
      "name": "Valid endpoint request returns success",
      "type": "api_endpoint",
      "description": "Checks that the documented endpoint accepts a valid request.",
      "input": "Valid request body using documented fields.",
      "expected_result": "Successful response matching the documented status code and body.",
      "reason": "API endpoint tests verify request and response behavior for the documented route."
    }
  ],
  "generated_code": "def test_generated_valid_request(client): ...",
  "evidence": [
    {
      "snippet": "principal: number, must be greater than 0",
      "source": "project_context"
    }
  ],
  "warnings": [
    "This is deterministic mocked output because OpenAI generation is not active for this request."
  ]
}
```

When `OPENAI_API_KEY` is configured, the backend uses the real LLM adapter and still validates the response against the same schema. The `generated_code` field must contain starter test code; blank or whitespace-only code is rejected and sent through the backend repair path.

## Limitations

- Generated tests must be reviewed before use.
- The app does not execute user code.
- The app does not execute generated tests.
- File upload is not implemented.
- GitHub import, CI integration, authentication, accounts, and saved history are not implemented.
- External embedding provider calls are not implemented; retrieval currently uses deterministic local embeddings.

## Future Improvements

- File upload for README or OpenAPI files.
- OpenAPI schema parser.
- More test frameworks.
- Downloadable test file.
- Saved generation history.
- Local model support.
- GitHub import and CI integration after separate specs approve that scope.

# TestPilot AI Backend

FastAPI backend for TestPilot AI.

## Current Sprint State

This backend currently implements the SPRINT-010 backend state:

- `GET /health`
- `POST /api/generate-tests`
- Pydantic request and response schemas
- deterministic mocked test generation
- text cleaning and chunking
- reusable prompt construction
- LLM client abstraction with fake test client
- deterministic local embeddings and in-memory retrieval
- OpenAI Responses API adapter behind a mockable LLM client boundary
- structured JSON parsing with one repair attempt
- non-empty `generated_code` validation so blank starter-code responses are rejected
- deterministic evaluation checks
- `.env.example` placeholders for provider configuration
- automatic local `backend/.env` loading
- provider mode in generated responses
- selected test type request and response fields
- backend tests

When `OPENAI_API_KEY` is configured, the generate endpoint uses the real LLM adapter. Without an API key, it returns deterministic mock output while using local retrieval to carry evidence from the provided context.

Real external embeddings are not implemented yet; retrieval currently uses deterministic local embeddings.

## Run Locally

From the repository root:

```bash
python -m pip install -r backend/requirements.txt
python -m uvicorn backend.app.main:app --reload
```

## Environment

Copy `backend/.env.example` to `backend/.env` for local development, or provide the same values as real environment variables:

```bash
OPENAI_API_KEY=your_api_key_here
LLM_MODEL=gpt-5.4-mini
EMBEDDING_MODEL=text-embedding-3-small
```

Values already set in the process environment take precedence over values from `.env` files. Never commit real API keys.

## Test

From the repository root:

```bash
python -m pytest backend/app/tests
```

## Safety Boundary

The backend treats submitted code and generated tests as text only. It does not execute user-submitted code or generated test code.

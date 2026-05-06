from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


VALID_CONTEXT = """
POST /api/debts

Creates a new debt record.

Required fields:
- name: string
- principal: number greater than 0
- apr: number between 0 and 100
- minimumPayment: number greater than 0
"""

PRODUCT_CONTEXT = """
PATCH /api/products/{id}

Updates product fields.

Request body:
- name: string, optional
- price: number, optional, must be greater than 0
- active: boolean, optional

Successful response:
- 200 OK
- returns id, name, price, active, updatedAt
"""

MULTI_API_CONTEXT = """
GET /api/users/{id}
- returns id, email, name, createdAt
- returns 404 Not Found if the user does not exist

DELETE /api/sessions/{id}
- deletes a session
- returns 204 No Content
- returns 404 Not Found if the session does not exist
"""


def setup_function():
    import os

    os.environ["OPENAI_API_KEY"] = ""


def test_health_returns_ok():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_generate_tests_valid_request_returns_response_shape():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "target_name": "/api/debts",
            "test_framework": "pytest",
            "extra_instructions": "Focus on validation.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["provider_mode"] == "mock"
    assert body["selected_test_types"] == [
        "api_endpoint",
        "validation",
        "negative",
        "edge_case",
        "contract_schema",
    ]
    assert body["summary"] == "Generated mocked test plan for /api/debts."
    assert body["test_cases"]
    assert {test_case["type"] for test_case in body["test_cases"]} == set(body["selected_test_types"])
    assert body["generated_code"].startswith("def test_generated_valid_request")
    assert body["evidence"]
    assert all(item["source"] == "project_context" for item in body["evidence"])
    assert body["warnings"]


def test_generate_tests_defaults_to_pytest():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "target_name": "/api/debts",
        },
    )

    assert response.status_code == 200
    assert "def test_generated_valid_request" in response.json()["generated_code"]


def test_generate_tests_accepts_blank_target_name():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "target_name": "   ",
            "extra_instructions": "Use the only endpoint in the context.",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "Generated mocked test plan for provided context."
    assert 'client.post("/api/example"' in body["generated_code"]


def test_generate_tests_supports_non_debt_api_target():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": PRODUCT_CONTEXT,
            "target_name": "PATCH /api/products/{id}",
            "selected_test_types": ["api_endpoint", "contract_schema"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "Generated mocked test plan for PATCH /api/products/{id}."
    assert 'client.patch("/api/products/{id}"' in body["generated_code"]
    assert body["selected_test_types"] == ["api_endpoint", "contract_schema"]


def test_generate_tests_keeps_target_primary_when_extra_instructions_mention_another_api():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": MULTI_API_CONTEXT,
            "target_name": "GET /api/users/{id}",
            "extra_instructions": "Also think about DELETE /api/sessions/{id}, but do not switch target.",
            "selected_test_types": ["api_endpoint"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["summary"] == "Generated mocked test plan for GET /api/users/{id}."
    assert 'client.get("/api/users/{id}"' in body["generated_code"]


def test_generate_tests_accepts_selected_test_types():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "target_name": "/api/debts",
            "selected_test_types": ["validation", "boundary", "contract_schema"],
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["selected_test_types"] == ["validation", "boundary", "contract_schema"]
    assert {test_case["type"] for test_case in body["test_cases"]} == {
        "validation",
        "boundary",
        "contract_schema",
    }


def test_generate_tests_empty_selected_test_types_uses_defaults():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "target_name": "/api/debts",
            "selected_test_types": [],
        },
    )

    assert response.status_code == 200
    assert response.json()["selected_test_types"] == [
        "api_endpoint",
        "validation",
        "negative",
        "edge_case",
        "contract_schema",
    ]


def test_generate_tests_supports_jest_supertest():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "target_name": "/api/debts",
            "test_framework": "jest_supertest",
        },
    )

    assert response.status_code == 200
    assert "request(app).post('/api/debts')" in response.json()["generated_code"]


def test_generate_tests_rejects_too_short_context():
    response = client.post(
        "/api/generate-tests",
        json={"project_context": "too short"},
    )

    assert response.status_code == 422


def test_generate_tests_rejects_unsupported_framework():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "test_framework": "unittest",
        },
    )

    assert response.status_code == 422


def test_generate_tests_rejects_invalid_selected_test_type():
    response = client.post(
        "/api/generate-tests",
        json={
            "project_context": VALID_CONTEXT,
            "selected_test_types": ["performance"],
        },
    )

    assert response.status_code == 422

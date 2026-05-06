import pytest

from app.services.llm_client import FakeLLMClient, LLMClientError, MissingAPIKeyError, OpenAILLMClient


def test_fake_llm_client_returns_configured_response_and_records_prompt():
    client = FakeLLMClient(response='{"summary": "ok"}')

    response = client.generate("prompt text")

    assert response == '{"summary": "ok"}'
    assert client.prompts == ["prompt text"]


def test_openai_llm_client_requires_api_key_without_injected_client():
    client = OpenAILLMClient(api_key=None, model="gpt-5.4-mini")

    with pytest.raises(MissingAPIKeyError):
        client.generate("prompt")


def test_openai_llm_client_uses_responses_api_with_json_schema():
    class StubResponses:
        def __init__(self) -> None:
            self.kwargs = None

        def create(self, **kwargs):
            self.kwargs = kwargs

            class Response:
                output_text = '{"provider_mode": "openai", "selected_test_types": ["api_endpoint"], "summary": "ok", "test_cases": [], "generated_code": "", "evidence": [], "warnings": []}'

            return Response()

    class StubClient:
        def __init__(self) -> None:
            self.responses = StubResponses()

    stub = StubClient()
    client = OpenAILLMClient(api_key="test-key", model="gpt-5.4-mini", client=stub)

    response = client.generate("prompt")

    assert '"summary": "ok"' in response
    assert stub.responses.kwargs["model"] == "gpt-5.4-mini"
    assert stub.responses.kwargs["input"] == "prompt"
    assert stub.responses.kwargs["text"]["format"]["type"] == "json_schema"
    assert stub.responses.kwargs["text"]["format"]["strict"] is True


def test_openai_llm_client_wraps_provider_errors():
    class StubResponses:
        def create(self, **kwargs):
            raise RuntimeError("provider failed")

    class StubClient:
        def __init__(self) -> None:
            self.responses = StubResponses()

    client = OpenAILLMClient(api_key="test-key", model="gpt-5.4-mini", client=StubClient())

    with pytest.raises(LLMClientError, match="OpenAI generation failed"):
        client.generate("prompt")


def test_openai_llm_client_reports_rejected_api_key_without_echoing_key():
    class StubResponses:
        def create(self, **kwargs):
            raise RuntimeError("Incorrect API key provided: sk-test-secret")

    class StubClient:
        def __init__(self) -> None:
            self.responses = StubResponses()

    client = OpenAILLMClient(api_key="test-key", model="gpt-5.4-mini", client=StubClient())

    with pytest.raises(LLMClientError) as exc_info:
        client.generate("prompt")

    message = str(exc_info.value)
    assert message == "OpenAI rejected the API key. Check backend/.env OPENAI_API_KEY."
    assert "sk-test-secret" not in message

from __future__ import annotations

from typing import Any, Protocol

from app.models.schemas import GenerateTestsResponse


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str:
        """Generate text from a prompt."""


class LLMClientError(RuntimeError):
    pass


class MissingAPIKeyError(LLMClientError):
    pass


def _provider_error_message(exc: Exception) -> str:
    message = str(exc)
    if "Incorrect API key provided" in message or exc.__class__.__name__ == "AuthenticationError":
        return "OpenAI rejected the API key. Check backend/.env OPENAI_API_KEY."
    if "model" in message.lower() and ("not found" in message.lower() or "does not exist" in message.lower()):
        return "OpenAI rejected the configured model. Check LLM_MODEL."
    return "OpenAI generation failed. Check the API key, model, and provider availability."


class FakeLLMClient:
    def __init__(self, response: str = "{}") -> None:
        self.response = response
        self.prompts: list[str] = []

    def generate(self, prompt: str) -> str:
        self.prompts.append(prompt)
        return self.response


class OpenAILLMClient:
    def __init__(self, *, api_key: str | None, model: str, client: Any | None = None) -> None:
        self.api_key = api_key
        self.model = model
        self._client = client

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client
        if not self.api_key:
            raise MissingAPIKeyError("OPENAI_API_KEY is required for real LLM generation.")

        try:
            from openai import OpenAI
        except ImportError as exc:
            raise LLMClientError("The openai package is required for real LLM generation.") from exc

        self._client = OpenAI(api_key=self.api_key)
        return self._client

    def generate(self, prompt: str) -> str:
        client = self._get_client()
        schema = GenerateTestsResponse.model_json_schema()
        try:
            response = client.responses.create(
                model=self.model,
                input=prompt,
                text={
                    "format": {
                        "type": "json_schema",
                        "name": "generate_tests_response",
                        "schema": schema,
                        "strict": True,
                    }
                },
            )
        except Exception as exc:
            raise LLMClientError(_provider_error_message(exc)) from exc
        return response.output_text

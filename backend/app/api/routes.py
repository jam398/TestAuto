from fastapi import APIRouter, HTTPException

from backend.app.config import get_settings
from backend.app.models.schemas import GenerateTestsRequest, GenerateTestsResponse
from backend.app.services.llm_client import LLMClientError, OpenAILLMClient
from backend.app.services.test_generator import GenerationError, generate_mock_tests, generate_tests_with_llm

router = APIRouter()


@router.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@router.post("/api/generate-tests", response_model=GenerateTestsResponse)
def generate_tests(request: GenerateTestsRequest) -> GenerateTestsResponse:
    settings = get_settings()
    if not settings.has_openai_api_key:
        return generate_mock_tests(request)

    client = OpenAILLMClient(api_key=settings.openai_api_key, model=settings.llm_model)
    try:
        return generate_tests_with_llm(request, client)
    except (GenerationError, LLMClientError) as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc

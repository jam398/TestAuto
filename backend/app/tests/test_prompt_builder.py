from backend.app.models.schemas import TestFramework, TestType
from backend.app.services.chunking import TextChunk
from backend.app.services.prompt_builder import build_generation_prompt, format_retrieved_context


def test_format_retrieved_context_includes_chunk_metadata():
    chunk = TextChunk(
        id="project_context:0",
        text="principal: number greater than 0",
        metadata={"source": "project_context", "chunk_index": 0},
    )

    formatted = format_retrieved_context([chunk])

    assert "[source=project_context chunk=0]" in formatted
    assert "principal: number greater than 0" in formatted


def test_format_retrieved_context_handles_empty_chunks():
    assert format_retrieved_context([]) == "No retrieved context was available."


def test_build_generation_prompt_includes_target_framework_evidence_and_instructions():
    chunk = TextChunk(
        id="project_context:0",
        text="apr: number between 0 and 100",
        metadata={"source": "project_context", "chunk_index": 0},
    )

    prompt = build_generation_prompt(
        target_name="POST /api/debts",
        test_framework=TestFramework.PYTEST,
        selected_test_types=[TestType.VALIDATION, TestType.BOUNDARY],
        extra_instructions="Focus on validation.",
        retrieved_chunks=[chunk],
    )

    assert "POST /api/debts" in prompt
    assert "pytest" in prompt
    assert "Focus on validation." in prompt
    assert "apr: number between 0 and 100" in prompt
    assert "validation" in prompt
    assert "boundary" in prompt
    assert "Validation Tests: test required fields" in prompt
    assert "Boundary Tests: test exact limits" in prompt
    assert "Target precedence:" in prompt
    assert "treat it as the principal API" in prompt
    assert "must not override or replace the specified target" in prompt


def test_build_generation_prompt_includes_anti_fabrication_rules():
    prompt = build_generation_prompt(
        target_name=None,
        test_framework=TestFramework.JEST_SUPERTEST,
        selected_test_types=[TestType.API_ENDPOINT],
        extra_instructions=None,
        retrieved_chunks=[],
    )

    assert "Do not invent behavior" in prompt
    assert "add a warning instead of making it up" in prompt
    assert "Return valid JSON" in prompt
    assert "jest_supertest" in prompt
    assert "Only generate test cases that match these selected types" in prompt
    assert "Do not generate test cases for unselected test types" in prompt
    assert "If the target is not specified" in prompt
    assert "generated_code field must contain non-empty starter test code" in prompt
    assert "Set generated_code to starter test code, not an empty string" in prompt

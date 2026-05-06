import pytest

from app.services.chunking import chunk_text, clean_text


def test_clean_text_normalizes_whitespace():
    text = "  POST /api/debts  \r\n\r\n\r\n  Creates a debt.  "

    assert clean_text(text) == "POST /api/debts\n\nCreates a debt."


def test_chunk_text_returns_empty_for_empty_text():
    assert chunk_text("   \n  ") == []


def test_chunk_text_returns_one_chunk_for_small_text():
    chunks = chunk_text("POST /api/debts creates a debt record.", chunk_size=100, overlap=10)

    assert len(chunks) == 1
    assert chunks[0].text == "POST /api/debts creates a debt record."
    assert chunks[0].metadata["source"] == "project_context"
    assert chunks[0].metadata["chunk_index"] == 0


def test_chunk_text_splits_long_text_with_overlap():
    text = "0123456789" * 30

    chunks = chunk_text(text, chunk_size=100, overlap=20)

    assert len(chunks) > 1
    assert chunks[0].text[-20:] == chunks[1].text[:20]
    assert chunks[1].metadata["start_char"] == 80


def test_chunk_text_preserves_custom_source_metadata():
    chunks = chunk_text("x" * 120, chunk_size=50, overlap=10, source="custom_source")

    assert chunks[0].id == "custom_source:0"
    assert chunks[0].metadata["source"] == "custom_source"


def test_chunk_text_rejects_invalid_settings():
    with pytest.raises(ValueError):
        chunk_text("content", chunk_size=10, overlap=10)

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class TextChunk:
    id: str
    text: str
    metadata: dict[str, Any]


def clean_text(text: str) -> str:
    normalized = text.replace("\r\n", "\n").replace("\r", "\n")
    lines = [line.strip() for line in normalized.split("\n")]

    cleaned_lines: list[str] = []
    previous_blank = False
    for line in lines:
        is_blank = line == ""
        if is_blank and previous_blank:
            continue
        cleaned_lines.append(line)
        previous_blank = is_blank

    return "\n".join(cleaned_lines).strip()


def chunk_text(
    text: str,
    *,
    chunk_size: int = 800,
    overlap: int = 100,
    source: str = "project_context",
) -> list[TextChunk]:
    if chunk_size <= 0:
        raise ValueError("chunk_size must be greater than 0")
    if overlap < 0:
        raise ValueError("overlap must be greater than or equal to 0")
    if overlap >= chunk_size:
        raise ValueError("overlap must be smaller than chunk_size")

    cleaned = clean_text(text)
    if not cleaned:
        return []

    if len(cleaned) <= chunk_size:
        return [
            TextChunk(
                id=f"{source}:0",
                text=cleaned,
                metadata={"source": source, "chunk_index": 0, "start_char": 0, "end_char": len(cleaned)},
            )
        ]

    chunks: list[TextChunk] = []
    start = 0
    while start < len(cleaned):
        end = min(start + chunk_size, len(cleaned))
        chunk_value = cleaned[start:end]
        chunks.append(
            TextChunk(
                id=f"{source}:{len(chunks)}",
                text=chunk_value,
                metadata={
                    "source": source,
                    "chunk_index": len(chunks),
                    "start_char": start,
                    "end_char": end,
                },
            )
        )
        if end == len(cleaned):
            break
        start = end - overlap

    return chunks

from __future__ import annotations

import math
from dataclasses import dataclass

from backend.app.services.chunking import TextChunk
from backend.app.services.embeddings import DeterministicEmbeddingClient, EmbeddingClient


@dataclass(frozen=True)
class RetrievedChunk:
    chunk: TextChunk
    score: float


def cosine_similarity(left: list[float], right: list[float]) -> float:
    if len(left) != len(right):
        raise ValueError("vectors must have the same dimensions")
    left_mag = math.sqrt(sum(value * value for value in left))
    right_mag = math.sqrt(sum(value * value for value in right))
    if left_mag == 0 or right_mag == 0:
        return 0.0
    return sum(a * b for a, b in zip(left, right, strict=True)) / (left_mag * right_mag)


class InMemoryVectorStore:
    def __init__(self) -> None:
        self._items: list[tuple[TextChunk, list[float]]] = []

    def add(self, chunk: TextChunk, embedding: list[float]) -> None:
        self._items.append((chunk, embedding))

    def search(self, query_embedding: list[float], *, top_k: int = 6) -> list[RetrievedChunk]:
        if top_k <= 0 or not self._items:
            return []

        scored = [
            RetrievedChunk(chunk=chunk, score=cosine_similarity(query_embedding, embedding))
            for chunk, embedding in self._items
        ]
        scored.sort(key=lambda item: item.score, reverse=True)
        return [item for item in scored[:top_k] if item.score > 0]


def build_retrieval_query(*, target_name: str | None, test_framework: str, extra_instructions: str | None) -> str:
    parts = ["Generate backend API or function tests", test_framework]
    if target_name:
        parts.extend(["primary target", target_name, target_name])
    if extra_instructions:
        parts.extend(["additional instructions", extra_instructions])
    return " ".join(parts)


def retrieve_relevant_chunks(
    chunks: list[TextChunk],
    *,
    query: str,
    embedding_client: EmbeddingClient | None = None,
    top_k: int = 6,
) -> list[RetrievedChunk]:
    if not chunks:
        return []

    client = embedding_client or DeterministicEmbeddingClient()
    store = InMemoryVectorStore()
    for chunk in chunks:
        store.add(chunk, client.embed(chunk.text))

    return store.search(client.embed(query), top_k=top_k)

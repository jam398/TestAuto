from app.services.chunking import TextChunk, chunk_text
from app.services.embeddings import DeterministicEmbeddingClient
from app.services.vector_store import (
    InMemoryVectorStore,
    build_retrieval_query,
    retrieve_relevant_chunks,
)


def test_deterministic_embedding_client_returns_stable_vectors():
    client = DeterministicEmbeddingClient(dimensions=16)

    assert client.embed("principal greater than 0") == client.embed("principal greater than 0")
    assert len(client.embed("principal greater than 0")) == 16


def test_retrieve_relevant_chunks_returns_matching_context_with_metadata():
    chunks = [
        TextChunk(
            id="project_context:0",
            text="principal must be greater than 0",
            metadata={"source": "project_context", "chunk_index": 0},
        ),
        TextChunk(
            id="project_context:1",
            text="createdAt is returned after creation",
            metadata={"source": "project_context", "chunk_index": 1},
        ),
    ]

    retrieved = retrieve_relevant_chunks(
        chunks,
        query="principal validation negative value",
        embedding_client=DeterministicEmbeddingClient(dimensions=32),
        top_k=1,
    )

    assert len(retrieved) == 1
    assert retrieved[0].chunk.text == "principal must be greater than 0"
    assert retrieved[0].chunk.metadata["source"] == "project_context"
    assert retrieved[0].score > 0


def test_retrieve_relevant_chunks_handles_empty_chunks():
    assert retrieve_relevant_chunks([], query="anything") == []


def test_vector_store_returns_empty_when_no_scores_match():
    client = DeterministicEmbeddingClient(dimensions=32)
    store = InMemoryVectorStore()
    chunk = TextChunk(id="project_context:0", text="apr validation", metadata={"source": "project_context"})
    store.add(chunk, client.embed(chunk.text))

    assert store.search(client.embed("zzzz yyyy xxxx"), top_k=3) == []


def test_build_retrieval_query_includes_target_framework_and_instructions():
    query = build_retrieval_query(
        target_name="POST /api/debts",
        test_framework="pytest",
        extra_instructions="Focus on validation.",
    )

    assert "POST /api/debts" in query
    assert "pytest" in query
    assert "Focus on validation." in query
    assert query.count("POST /api/debts") == 2
    assert query.index("POST /api/debts") < query.index("Focus on validation.")


def test_build_retrieval_query_weights_target_before_conflicting_extra_instructions():
    query = build_retrieval_query(
        target_name="PATCH /api/products/{id}",
        test_framework="pytest",
        extra_instructions="Generate tests for DELETE /api/sessions/{id}.",
    )

    assert query.count("PATCH /api/products/{id}") == 2
    assert "DELETE /api/sessions/{id}" in query
    assert query.index("PATCH /api/products/{id}") < query.index("DELETE /api/sessions/{id}")


def test_chunked_context_can_be_retrieved():
    context = """
    POST /api/debts

    Required fields:
    principal must be greater than 0.
    apr must be between 0 and 100.

    Successful response returns createdAt.
    """
    chunks = chunk_text(context, chunk_size=70, overlap=10)

    retrieved = retrieve_relevant_chunks(chunks, query="apr validation above 100", top_k=2)

    assert retrieved
    assert any("apr" in item.chunk.text for item in retrieved)

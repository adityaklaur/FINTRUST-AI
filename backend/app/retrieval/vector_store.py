"""ChromaDB wrapper.

Embedding backend selection (in priority order):
  1. sentence-transformers, IF it is installed AND EMBEDDING_MODEL names an ST
     model — highest quality, but pulls in torch.
  2. ChromaDB's built-in ONNX ``all-MiniLM-L6-v2`` (DefaultEmbeddingFunction) —
     the same model family, no torch, ~80MB one-time model download.

We default to (2): robust, light, and identical model to what the plan asked
for. Set EMBEDDING_MODEL + `pip install sentence-transformers` to opt into (1).

The collection is (re)acquired via ``get_or_create_collection`` on EVERY call
rather than cached, so a ``reset()`` in one place never leaves another
VectorStore holding a stale (deleted) collection handle.
"""

from __future__ import annotations

from app.core.config import Settings, get_settings
from app.core.logging import get_logger

log = get_logger("vector_store")


class VectorStore:
    def __init__(self, config: Settings | None = None) -> None:
        import chromadb
        from chromadb.config import Settings as ChromaSettings

        self.config = config or get_settings()
        self.client = chromadb.PersistentClient(
            path=str(self.config.chroma_dir),
            settings=ChromaSettings(anonymized_telemetry=False, allow_reset=True),
        )
        self._embedding_fn = self._build_embedding_fn()
        self._collection()  # ensure it exists so count() works immediately

    def _build_embedding_fn(self):
        from chromadb.utils import embedding_functions as ef

        model = self.config.embedding_model
        try:
            import sentence_transformers  # noqa: F401

            log.info("embeddings: sentence-transformers (%s)", model)
            return ef.SentenceTransformerEmbeddingFunction(model_name=model)
        except Exception:
            log.info("embeddings: ChromaDB default ONNX all-MiniLM-L6-v2")
            return ef.DefaultEmbeddingFunction()

    def _collection(self):
        return self.client.get_or_create_collection(
            name=self.config.collection_name,
            embedding_function=self._embedding_fn,
            metadata={"hnsw:space": "cosine"},
        )

    def upsert_chunks(self, chunks) -> int:
        if not chunks:
            return 0
        self._collection().upsert(
            ids=[c.chunk_id for c in chunks],
            documents=[c.text for c in chunks],
            metadatas=[c.metadata for c in chunks],
        )
        return len(chunks)

    def query(self, query_text: str, n_results: int, where: dict | None = None) -> dict:
        return self._collection().query(
            query_texts=[query_text],
            n_results=n_results,
            where=where,
            include=["documents", "metadatas", "distances"],
        )

    def count(self) -> int:
        return self._collection().count()

    def reset(self) -> None:
        """Dev only: drop and recreate the collection."""
        try:
            self.client.delete_collection(self.config.collection_name)
        except Exception:  # noqa: BLE001
            pass
        self._collection()

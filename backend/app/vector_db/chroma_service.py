import chromadb
from app.core.config import settings
import os
        return [[0.0] * 384 for _ in inputs]


class ChromaService:
    def __init__(self):
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        os.makedirs(self.persist_directory, exist_ok=True)
        # Lazy initialization — loaded on first use to save memory at startup
        self._client = None
        self._memories_collection = None
        self._summaries_collection = None

    def _ensure_initialized(self):
        """Initialize ChromaDB only when first needed. Uses ChromaDB's built-in
        default embedding function (ONNX all-MiniLM-L6-v2) — no PyTorch needed."""
        if self._client is not None:
            return
        self._client = chromadb.PersistentClient(path=self.persist_directory)
        # Using default embedding function (ONNX-based, ~50MB vs ~400MB for PyTorch)
        self._memories_collection = self._client.get_or_create_collection(
            name="memories"
        )
        self._summaries_collection = self._client.get_or_create_collection(
            name="summaries"
        )

    @property
    def memories_collection(self):
        self._ensure_initialized()
        return self._memories_collection

    @property
    def summaries_collection(self):
        self._ensure_initialized()
        return self._summaries_collection

    def add_memory(self, memory_id: str, content: str, metadata: dict):
        self.memories_collection.add(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata]
        )

    def query_memories(self, query_text: str, workspace_id: int, n_results: int = 5):
        results = self.memories_collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where={"workspace_id": workspace_id}
        )
        return results

    def delete_memory(self, memory_id: str):
        self.memories_collection.delete(ids=[memory_id])

    def update_memory(self, memory_id: str, content: str, metadata: dict):
        self.memories_collection.update(
            ids=[memory_id],
            documents=[content],
            metadatas=[metadata]
        )

chroma_service = ChromaService()

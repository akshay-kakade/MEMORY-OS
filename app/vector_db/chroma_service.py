import chromadb
from chromadb.utils import embedding_functions
from app.core.config import settings
import os

class ChromaService:
    def __init__(self):
        self.persist_directory = settings.CHROMA_PERSIST_DIRECTORY
        os.makedirs(self.persist_directory, exist_ok=True)
        
        self.client = chromadb.PersistentClient(path=self.persist_directory)
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )
        
        self.memories_collection = self.client.get_or_create_collection(
            name="memories",
            embedding_function=self.embedding_function
        )
        self.summaries_collection = self.client.get_or_create_collection(
            name="summaries",
            embedding_function=self.embedding_function
        )

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

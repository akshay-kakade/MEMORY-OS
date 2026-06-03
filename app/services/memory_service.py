import json
from groq import Groq
from app.core.config import settings
from app.vector_db.chroma_service import chroma_service
from app.models import models
from app.schemas import schemas
from sqlalchemy.orm import Session
from datetime import datetime

class MemoryService:
    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def extract_memories(self, text: str):
        prompt = f"""
        You are a memory extraction engine. Your task is to identify and extract key information (facts, preferences, goals, projects, skills, experiences, or relationships) from the user message that should be remembered for long-term context.
        
        User Message: "{text}"
        
        Rules:
        1. Extract only meaningful information.
        2. Categorize each into one of: Preference, Goal, Project, Skill, Fact, Experience, Relationship.
        3. Assign an importance score (1-10) based on how critical this info is for a personal assistant.
        
        Return a JSON object with a "memories" key containing a list of objects.
        Example:
        {{
            "memories": [
                {{"content": "User prefers Python for backend development", "category": "Preference", "importance": 7}},
                {{"content": "User is working on a project called MemoryOS", "category": "Project", "importance": 9}}
            ]
        }}
        """
        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model,
                response_format={"type": "json_object"}
            )
            content = json.loads(response.choices[0].message.content)
            # The LLM might return {"memories": [...]} or just the list
            if isinstance(content, dict) and "memories" in content:
                return content["memories"]
            return content
        except Exception as e:
            print(f"Error parsing memories: {e}")
            return []

    def save_memory(self, db: Session, workspace_id: int, content: str, category_name: str, importance: int):
        # 1. Get category ID
        category = db.query(models.MemoryCategory).filter(models.MemoryCategory.name == category_name).first()
        if not category:
            category = db.query(models.MemoryCategory).filter(models.MemoryCategory.name == "Fact").first()
        if not category:
            category = models.MemoryCategory(name="Fact")
            db.add(category)
            db.commit()
            db.refresh(category)

        # 2. Save to PostgreSQL
        db_memory = models.Memory(
            content=content,
            workspace_id=workspace_id,
            category_id=category.id,
            importance=importance
        )
        db.add(db_memory)
        db.commit()
        db.refresh(db_memory)

        # 3. Save to ChromaDB
        try:
            chroma_service.add_memory(
                memory_id=str(db_memory.id),
                content=content,
                metadata={
                    "workspace_id": workspace_id,
                    "category": category.name,
                    "importance": importance
                }
            )
        except Exception as e:
            print(f"Error saving memory embedding: {e}")
        return db_memory

    def retrieve_relevant_memories(self, query: str, workspace_id: int, n_results: int = 5):
        try:
            chroma_results = chroma_service.query_memories(query, workspace_id, n_results)
        except Exception as e:
            print(f"Error retrieving memories: {e}")
            return []
        # Format results for prompt context
        memories = []
        if chroma_results["documents"]:
            for i in range(len(chroma_results["documents"][0])):
                memories.append({
                    "content": chroma_results["documents"][0][i],
                    "metadata": chroma_results["metadatas"][0][i],
                    "score": chroma_results["distances"][0][i] if "distances" in chroma_results else 0
                })
        return memories

memory_service = MemoryService()

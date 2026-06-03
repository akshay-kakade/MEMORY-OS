from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.core.database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    workspaces = relationship("Workspace", back_populates="owner")

class UserCredential(Base):
    __tablename__ = "user_credentials"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, index=True)
    password_hash = Column(String)
    salt = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Workspace(Base):
    __tablename__ = "workspaces"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(Text)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    owner = relationship("User", back_populates="workspaces")
    chats = relationship("Chat", back_populates="workspace")
    memories = relationship("Memory", back_populates="workspace")

class Chat(Base):
    __tablename__ = "chats"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    is_archived = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    workspace = relationship("Workspace", back_populates="chats")
    messages = relationship("Message", back_populates="chat")
    branches = relationship("ChatBranch", back_populates="parent_chat")

class ChatBranch(Base):
    __tablename__ = "chat_branches"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    parent_chat_id = Column(Integer, ForeignKey("chats.id"))
    fork_point_message_id = Column(Integer, ForeignKey("messages.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    parent_chat = relationship("Chat", back_populates="branches")

class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    chat_id = Column(Integer, ForeignKey("chats.id"))
    role = Column(String) # user or assistant
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    chat = relationship("Chat", back_populates="messages")

class MemoryCategory(Base):
    __tablename__ = "memory_categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True) # Preference, Goal, Project, Skill, Fact, Experience, Relationship

class Memory(Base):
    __tablename__ = "memories"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    category_id = Column(Integer, ForeignKey("memory_categories.id"))
    importance = Column(Integer, default=1) # 1-10
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    last_retrieved = Column(DateTime(timezone=True))
    is_pinned = Column(Boolean, default=False)
    
    workspace = relationship("Workspace", back_populates="memories")
    category = relationship("MemoryCategory")
    relationships = relationship("MemoryRelationship", foreign_keys="[MemoryRelationship.source_id]")

class MemoryRelationship(Base):
    __tablename__ = "memory_relationships"
    id = Column(Integer, primary_key=True, index=True)
    source_id = Column(Integer, ForeignKey("memories.id"))
    target_id = Column(Integer, ForeignKey("memories.id"))
    relation_type = Column(String) # e.g., "Skill", "Project", "Goal"
    
class MemorySummary(Base):
    __tablename__ = "memory_summaries"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    content = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UploadedFile(Base):
    __tablename__ = "uploaded_files"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String)
    url = Column(String) # Cloudinary URL
    file_type = Column(String) # PNG, JPG, etc.
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    uploaded_at = Column(DateTime(timezone=True), server_default=func.now())

class ImageMemory(Base):
    __tablename__ = "image_memories"
    id = Column(Integer, primary_key=True, index=True)
    uploaded_file_id = Column(Integer, ForeignKey("uploaded_files.id"))
    extracted_text = Column(Text)
    memory_id = Column(Integer, ForeignKey("memories.id"))

class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"
    id = Column(Integer, primary_key=True, index=True)
    memory_id = Column(Integer, ForeignKey("memories.id"))
    chat_id = Column(Integer, ForeignKey("chats.id"))
    query = Column(String)
    score = Column(Float)
    retrieved_at = Column(DateTime(timezone=True), server_default=func.now())

class Analytics(Base):
    __tablename__ = "analytics"
    id = Column(Integer, primary_key=True, index=True)
    workspace_id = Column(Integer, ForeignKey("workspaces.id"))
    metric_name = Column(String)
    metric_value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())

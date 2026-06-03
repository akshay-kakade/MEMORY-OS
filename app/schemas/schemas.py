from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

# User/Auth
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class UserLogin(BaseModel):
    username_or_email: str
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

class AuthResponse(BaseModel):
    user: User
    message: str

# Workspace
class WorkspaceBase(BaseModel):
    name: str
    description: Optional[str] = None
    owner_id: int

class WorkspaceCreate(WorkspaceBase):
    pass

class Workspace(WorkspaceBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Chat
class ChatBase(BaseModel):
    title: str
    workspace_id: int

class ChatCreate(ChatBase):
    pass

class Chat(ChatBase):
    id: int
    is_archived: bool
    created_at: datetime

    class Config:
        from_attributes = True

# Message
class MessageBase(BaseModel):
    chat_id: int
    role: str
    content: str

class MessageCreate(MessageBase):
    pass

class Message(MessageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True

# Memory
class MemoryBase(BaseModel):
    content: str
    workspace_id: int
    category_id: int
    importance: int = 1

class MemoryCreate(MemoryBase):
    pass

class Memory(MemoryBase):
    id: int
    created_at: datetime
    last_retrieved: Optional[datetime]
    is_pinned: bool

    class Config:
        from_attributes = True

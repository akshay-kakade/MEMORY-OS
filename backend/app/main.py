from fastapi import FastAPI, Depends, HTTPException
# Force non-GUI matplotlib backend early to avoid Tkinter imports in workers
try:
    import matplotlib
    matplotlib.use('Agg')
except Exception:
    pass
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from app.core.database import get_db, engine, Base
from app.core.config import settings
from app.models import models
from app.schemas import schemas # Need to create this
from typing import List
import hashlib
import secrets

app = FastAPI(title=settings.PROJECT_NAME)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup():
    from app.init_db import init_db
    init_db()

@app.get("/")
def read_root():
    return {"message": "Welcome to MemoryOS API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}

def hash_password(password: str, salt: str) -> str:
    return hashlib.sha256(f"{salt}{password}".encode("utf-8")).hexdigest()

def public_user(user: models.User):
    return {"id": user.id, "username": user.username, "email": user.email}

# Auth endpoints
@app.post("/auth/signup", response_model=schemas.AuthResponse)
def signup(payload: schemas.UserCreate, db: Session = Depends(get_db)):
    username = payload.username.strip()
    email = payload.email.strip().lower()
    if not username or not email or len(payload.password) < 6:
        raise HTTPException(status_code=400, detail="Username, email, and a 6+ character password are required")

    existing = db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Username or email already exists")

    user = models.User(username=username, email=email)
    db.add(user)
    db.commit()
    db.refresh(user)

    salt = secrets.token_hex(16)
    credential = models.UserCredential(
        user_id=user.id,
        salt=salt,
        password_hash=hash_password(payload.password, salt),
    )
    db.add(credential)
    db.commit()
    return {"user": public_user(user), "message": "Account created"}

@app.post("/auth/signin", response_model=schemas.AuthResponse)
def signin(payload: schemas.UserLogin, db: Session = Depends(get_db)):
    identifier = payload.username_or_email.strip()
    user = db.query(models.User).filter(
        (models.User.username == identifier) | (models.User.email == identifier.lower())
    ).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid username/email or password")

    credential = db.query(models.UserCredential).filter(
        models.UserCredential.user_id == user.id
    ).first()
    if not credential or credential.password_hash != hash_password(payload.password, credential.salt):
        raise HTTPException(status_code=401, detail="Invalid username/email or password")

    return {"user": public_user(user), "message": "Signed in"}

# Workspace endpoints
@app.post("/workspaces/", response_model=schemas.Workspace)
def create_workspace(workspace: schemas.WorkspaceCreate, db: Session = Depends(get_db)):
    db_workspace = models.Workspace(**workspace.dict())
    db.add(db_workspace)
    db.commit()
    db.refresh(db_workspace)
    return db_workspace

@app.get("/workspaces/", response_model=List[schemas.Workspace])
def read_workspaces(user_id: int | None = None, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    query = db.query(models.Workspace)
    if user_id is not None:
        query = query.filter(models.Workspace.owner_id == user_id)
    workspaces = query.offset(skip).limit(limit).all()
    return workspaces

# Chat endpoints
@app.post("/chats/", response_model=schemas.Chat)
def create_chat(chat: schemas.ChatCreate, db: Session = Depends(get_db)):
    db_chat = models.Chat(**chat.dict())
    db.add(db_chat)
    db.commit()
    db.refresh(db_chat)
    return db_chat

@app.delete("/chats/{chat_id}")
def delete_chat(chat_id: int, db: Session = Depends(get_db)):
    db_chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not db_chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    # Delete messages first
    db.query(models.Message).filter(models.Message.chat_id == chat_id).delete()
    db.delete(db_chat)
    db.commit()
    return {"message": "Chat deleted"}

@app.post("/chats/{chat_id}/generate-title")
def generate_chat_title(chat_id: int, db: Session = Depends(get_db)):
    from app.services.chat_service import chat_service
    title = chat_service.generate_title(db, chat_id)
    return {"title": title}

# Message endpoints
@app.post("/chats/{chat_id}/messages/", response_model=schemas.Message)
def send_message(chat_id: int, message: schemas.MessageCreate, db: Session = Depends(get_db)):
    from app.services.chat_service import chat_service
    db_assist_msg = chat_service.get_response(db, chat_id, message.content)
    return db_assist_msg

@app.get("/chats/", response_model=List[schemas.Chat])
def read_chats(workspace_id: int, db: Session = Depends(get_db)):
    chats = db.query(models.Chat).filter(models.Chat.workspace_id == workspace_id).all()
    return chats

# Memory endpoints
@app.get("/memories/{workspace_id}", response_model=List[schemas.Memory])
def read_memories(workspace_id: int, db: Session = Depends(get_db)):
    memories = db.query(models.Memory).filter(models.Memory.workspace_id == workspace_id).all()
    return memories

@app.post("/memories/", response_model=schemas.Memory)
def create_memory(memory: schemas.MemoryCreate, db: Session = Depends(get_db)):
    from app.services.memory_service import memory_service
    # We need to map category_id to name for the service
    cat = db.query(models.MemoryCategory).filter(models.MemoryCategory.id == memory.category_id).first()
    return memory_service.save_memory(db, memory.workspace_id, memory.content, cat.name if cat else "Fact", memory.importance)

@app.get("/chats/{chat_id}/messages/", response_model=List[schemas.Message])
def read_messages(chat_id: int, db: Session = Depends(get_db)):
    messages = db.query(models.Message).filter(models.Message.chat_id == chat_id).all()
    return messages

from fastapi.responses import Response

@app.get("/chats/{chat_id}/export/{format}")
def export_chat(chat_id: int, format: str, db: Session = Depends(get_db)):
    from app.services.export_service import export_service
    
    chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
        
    messages = db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.created_at).all()
    msg_data = [{"role": m.role, "content": m.content, "timestamp": str(m.created_at)} for m in messages]
    
    if format == "pdf":
        content = export_service.export_as_pdf(chat.title, msg_data)
        return Response(content=content, media_type="application/pdf", headers={"Content-Disposition": f"attachment; filename=chat_{chat_id}.pdf"})
    elif format == "docx":
        content = export_service.export_as_docx(chat.title, msg_data)
        return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": f"attachment; filename=chat_{chat_id}.docx"})
    elif format == "excel":
        content = export_service.export_as_excel(msg_data)
        return Response(content=content, media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", headers={"Content-Disposition": f"attachment; filename=chat_{chat_id}.xlsx"})
    elif format == "csv":
        content = export_service.export_as_csv(msg_data)
        return Response(content=content, media_type="text/csv", headers={"Content-Disposition": f"attachment; filename=chat_{chat_id}.csv"})
    else:
        raise HTTPException(status_code=400, detail="Invalid format")

# OCR endpoint
from fastapi import UploadFile, File, Form
@app.post("/ocr/")
async def process_ocr(workspace_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    from app.services.ocr_service import ocr_service
    from app.services.memory_service import memory_service
    
    content = await file.read()
    text = ocr_service.process_image(content)
    url = ocr_service.upload_to_cloudinary(content, file.filename)
    
    # Save file record
    db_file = models.UploadedFile(filename=file.filename, url=url, file_type=file.content_type, workspace_id=workspace_id)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    
    # Save as memory
    db_memory = memory_service.save_memory(db, workspace_id, text, "Fact", 5)
    
    # Link image memory
    db_image_mem = models.ImageMemory(uploaded_file_id=db_file.id, extracted_text=text, memory_id=db_memory.id)
    db.add(db_image_mem)
    db.commit()
    
    return {"extracted_text": text, "url": url}

# PDF endpoint
@app.post("/pdf/")
async def process_pdf(workspace_id: int = Form(...), file: UploadFile = File(...), db: Session = Depends(get_db)):
    from app.services.tools_service import tools_service
    from app.services.memory_service import memory_service
    
    content = await file.read()
    text = tools_service.extract_text_from_pdf(content)
    
    # Save as memory (summarize if too long)
    db_memory = memory_service.save_memory(db, workspace_id, text[:2000], "Fact", 7)
    
    return {"extracted_text": text[:1000] + "...", "memory_id": db_memory.id}

# Graph endpoint
@app.get("/graph/{workspace_id}")
def get_graph(workspace_id: int, db: Session = Depends(get_db)):
    from app.graph.graph_service import graph_service
    memories = db.query(models.Memory).filter(models.Memory.workspace_id == workspace_id).all()
    
    for mem in memories:
        cat = db.query(models.MemoryCategory).filter(models.MemoryCategory.id == mem.category_id).first()
        graph_service.add_memory_node(mem.id, mem.content[:30], cat.name if cat else "Fact")
        
    img_str = graph_service.visualize_graph()
    return {"image": img_str}


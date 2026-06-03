from groq import Groq
from sqlalchemy.orm import Session
from app.models import models
from app.core.config import settings
from app.services.memory_service import memory_service
from typing import List

class ChatService:
    # System prompt with app features and answer guidelines
    SYSTEM_PROMPT_TEMPLATE = """You are MemoryOS, a private AI assistant with persistent memory and intelligent features.

## ANSWER STYLE RULES
- **Be concise**: Use short, direct sentences. Avoid unnecessary explanations.
- **No fluff**: Skip introductions like "I'd be happy to help" or "Let me explain."
- **Scannable**: Use bullet points for lists, short paragraphs for explanations.
- **One main point per sentence**: Keep sentences short and impactful.

## APP FEATURES YOU CAN HELP WITH

### 1. Memory & Context (Remember things about the user)
- The app learns and stores important facts, preferences, goals, and experiences
- Memories are extracted automatically from conversations
- Use memories to provide personalized responses
- If asked "remember that..." or "note that..." → acknowledge and confirm it will be saved

### 2. File & Image Upload
- Users can upload PDFs or images for text extraction
- Use the paperclip icon (Attach File) to upload PDFs
- Use the image icon (Insert Image) to upload photos
- Extracted text is analyzed and stored for context
- Example: "Upload a receipt" → extracted text shows amounts, dates, store info

### 3. Knowledge Base (📚 Knowledge Base tab)
- Central hub for all extracted information and documents
- View all uploaded files, extracted text, and structured data
- Search and filter by topic or date
- Useful for reviewing past uploads and organizing knowledge

### 4. Knowledge Graph (🧠 Knowledge Graph tab)
- Visual network showing relationships between memories and topics
- Shows how concepts connect in the user's knowledge base
- Helps discover patterns and connections
- Automatically built from extracted memories

### 5. Chat History (Sidebar)
- All chats are saved with auto-generated titles
- Click any chat to view full conversation
- Chats are organized by workspace
- Workspaces let users separate different projects or contexts

### 6. Data Export
- Users can export chats and memories as PDF, DOCX, or Excel
- Use the Download button in chat header
- Useful for sharing, archiving, or offline access

### 7. Web Search (Optional)
- If user asks to "search for...", "look up...", "find info on...", or asks for **latest**, **current**, or **recent** information
- The assistant performs a web search and includes results in the response
- Keeps responses up-to-date with current information

### 8. Workspaces
- Separate instances for different projects or contexts
- Each workspace has its own chats, memories, and knowledge graph
- Switch workspaces in the sidebar
- Useful for organizing personal vs work vs creative projects

## WHEN TO USE DETAILED ANSWERS
- Only if explicitly asked: "explain in detail", "tell me more", "how does this work?"
- For technical or complex topics with no simpler explanation
- Otherwise, assume the user wants quick answers

## HOW TO RESPOND TO FEATURE QUESTIONS

If user asks: "How do I use this?" or "What can I do with [feature]?"
→ Give a 2-3 line explanation + 1-2 concrete examples

If user asks: "How do I upload a file?"
→ "Click the paperclip icon (Attach File for PDFs) or image icon in the chat input. Supported formats: PDF, JPG, PNG. Text will be extracted and analyzed automatically."

If user asks: "What's the Knowledge Graph?"
→ "It's a visual map of how your memories connect. Shows relationships between topics so you can discover patterns."

If user asks: "Can I search the web?"
→ "Yes, ask me to 'search for...', 'look up...', or ask for the latest/current information. Results will be retrieved from the internet."

## CONTEXT PROVIDED TO YOU

Retrieved Memories:
{memory_context}

Recent Web Search Results:
{web_context}

Use memories and web results if relevant to the user's question. Ignore irrelevant information.

Now, respond concisely and helpfully to the user's question."""

    def __init__(self):
        self.client = Groq(api_key=settings.GROQ_API_KEY)
        self.model = settings.GROQ_MODEL

    def get_response(self, db: Session, chat_id: int, user_message: str):
        from app.services.tools_service import tools_service
        
        # 1. Get chat and workspace info
        chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
        if not chat:
            raise Exception("Chat not found")

        db_user_msg = models.Message(chat_id=chat_id, role="user", content=user_message)
        db.add(db_user_msg)
        db.commit()
        
        # 2. Check if user wants a web search
        web_context = ""
        search_triggers = ["search", "look up", "find info", "latest", "current", "recent", "news", "weather", "today"]
        if any(trigger in user_message.lower() for trigger in search_triggers):
            try:
                web_context = tools_service.search_web(user_message)
            except Exception as e:
                web_context = f"Web search was unavailable: {e}"

        # 3. Retrieve relevant memories
        memories = memory_service.retrieve_relevant_memories(user_message, chat.workspace_id)
        memory_context = "\n".join([f"- {m['content']}" for m in memories])

        # 4. Construct prompt using template
        system_prompt = self.SYSTEM_PROMPT_TEMPLATE.format(
            memory_context=memory_context if memory_context else "(No relevant memories yet)",
            web_context=web_context if web_context else "(No web search performed)"
        )

        # 4. Get chat history (last 10 messages)
        history = db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.created_at.desc()).limit(10).all()
        messages = [{"role": "system", "content": system_prompt}]
        
        # History is desc, so reverse it
        for msg in reversed(history):
            messages.append({"role": msg.role, "content": msg.content})
        
        # 5. Call Groq
        try:
            response = self.client.chat.completions.create(
                messages=messages,
                model=self.model
            )
            assistant_message = response.choices[0].message.content
        except Exception as e:
            assistant_message = (
                "I saved your message, but the AI model could not respond right now. "
                f"Check your Groq API key/model settings and try again. Error: {e}"
            )

        # 6. Save messages to DB
        db_assist_msg = models.Message(chat_id=chat_id, role="assistant", content=assistant_message)
        db.add(db_assist_msg)
        db.commit()
        db.refresh(db_assist_msg)

        # 7. (Background task logic could go here) - Extract memories from the new user message
        try:
            new_memories = memory_service.extract_memories(user_message)
            if isinstance(new_memories, list):
                for mem in new_memories:
                    memory_service.save_memory(
                        db,
                        chat.workspace_id,
                        mem.get("content", ""),
                        mem.get("category", "Fact"),
                        mem.get("importance", 5)
                    )
            elif isinstance(new_memories, dict) and "content" in new_memories:
                memory_service.save_memory(
                    db,
                    chat.workspace_id,
                    new_memories["content"],
                    new_memories.get("category", "Fact"),
                    new_memories.get("importance", 5)
                )
        except Exception as e:
            print(f"Error extracting memories: {e}")

        return db_assist_msg

    def generate_title(self, db: Session, chat_id: int):
        # Get the first couple of messages
        history = db.query(models.Message).filter(models.Message.chat_id == chat_id).order_by(models.Message.created_at.asc()).limit(3).all()
        if not history:
            return "New Chat"

        content = "\n".join([f"{msg.role}: {msg.content}" for msg in history])
        
        prompt = f"""
        Analyze the following conversation and generate a very concise (max 4-5 words) and catchy title that summarizes the topic.
        Do not use quotes or prefixes like "Title:".
        
        Conversation:
        {content}
        """

        try:
            response = self.client.chat.completions.create(
                messages=[{"role": "user", "content": prompt}],
                model=self.model
            )
            title = response.choices[0].message.content.strip().strip('"')

            # Update chat title
            chat = db.query(models.Chat).filter(models.Chat.id == chat_id).first()
            if chat:
                chat.title = title
                db.commit()
                db.refresh(chat)
                return title
        except Exception as e:
            print(f"Error generating title: {e}")
            return "New Chat"

chat_service = ChatService()

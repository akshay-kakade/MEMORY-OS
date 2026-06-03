# MemoryOS

**Persistent Memory • RAG • LangGraph • LangChain • ChromaDB • Semantic Search • Knowledge Graphs • FastAPI • React • Docker • Render**

MemoryOS is a production-grade AI memory platform designed to extend the capabilities of Large Language Models through persistent memory, semantic retrieval, knowledge graphs, and Retrieval-Augmented Generation (RAG).

Unlike traditional AI chatbots that lose context between conversations, MemoryOS enables long-term memory retention, contextual retrieval, personalized interactions, and workspace-based knowledge organization. The platform acts as a dedicated memory operating system for AI assistants, allowing them to remember, retrieve, organize, and reason over information across multiple conversations and sessions.

---

# Project Overview

Large Language Models are limited by context windows and cannot naturally remember information between conversations. MemoryOS solves this problem by introducing a persistent memory layer built on vector search, semantic retrieval, structured memory storage, and intelligent memory management.

The system automatically extracts important information from conversations, stores it as structured memories, retrieves relevant context when needed, and injects those memories into future prompts to improve personalization and response quality.

MemoryOS is built to demonstrate practical GenAI engineering, RAG architectures, memory systems, vector databases, knowledge graphs, agent workflows, and production AI deployment.

---

# Core GenAI Concepts Demonstrated

* Retrieval-Augmented Generation (RAG)
* Long-Term Memory Systems
* Context Engineering
* Prompt Engineering
* LLM Orchestration
* Semantic Search
* Vector Databases
* Embedding-Based Retrieval
* Knowledge Graph Generation
* Memory Extraction Pipelines
* Agentic Workflows
* LangGraph State Management
* LangChain Retrieval Pipelines
* Memory Ranking & Prioritization
* Memory Compression
* Multimodal AI Processing
* Persistent AI Memory
* Conversational AI Systems

---
# Screenshots


![alt text](<Screenshot 2026-06-03 120053.png>) ,
![alt text](<Screenshot 2026-06-03 120213.png>) ,
![alt text](<Screenshot 2026-06-03 120228.png>),
![alt text](<Screenshot 2026-06-03 120255.png>) ,
![alt text](<Screenshot 2026-06-03 120319.png>) ,


---



# Key Features

## AI Assistant

* Multi-session conversational assistant
* Personalized responses using memory retrieval
* Workspace-aware conversations
* Long-term context retention
* Context-aware response generation
* Groq-powered LLM inference
* **Real-time Web Search**: Automatically conducts web searches to answer queries requesting latest news, current facts, weather, or explicit search tasks.

---

## Chat Management

* Create chats
* Continue conversations
* Chat history sidebar
* Rename chats
* Delete chats
* Archive chats
* Search chat history
* Conversation summaries

---

## Chat Branching

Fork conversations into separate branches.

Example:

AI Engineering
├── Machine Learning
├── XGBoost
└── Deep Learning

Users can explore multiple discussion paths without losing previous context.

---

## Workspace System

Organize information into isolated workspaces.

Examples:

* AI Engineering
* Research
* Projects
* Interview Preparation
* Learning

Each workspace maintains:

* Chats
* Memories
* Summaries
* Knowledge Graph
* Analytics

---

## Long-Term Memory Engine

The memory engine automatically extracts and stores important information from conversations.

Examples:

* User Preferences
* Skills
* Goals
* Projects
* Experiences
* Relationships
* Facts

Example Memory:

* User is learning Machine Learning
* User built AI Data Quality Copilot
* User wants an AI Engineer role

---

## Memory Classification

Memories are automatically categorized:

* Preference
* Goal
* Project
* Skill
* Fact
* Experience
* Relationship

---

## Memory Retrieval System

Relevant memories are retrieved before every response.

Retrieval methods include:

* Semantic Search
* Vector Similarity Search
* Importance Ranking
* Recency Ranking
* Workspace Filtering
* Category Filtering

---

## Memory Updating

The system detects newer information and updates existing memories.

Example:

Old Memory:

Favorite Language = Python

New Memory:

Favorite Language = Rust

The memory engine can:

* Replace
* Version
* Merge

existing information.

---

## Memory Forgetting

Users can:

* Delete memories
* Delete categories
* Remove workspace memories
* Manage stored information

---

## Memory Compression

Older conversation histories are compressed into summaries.

Example:

100 Memories
↓
Structured Summary

This reduces retrieval costs while preserving important information.

---

## Knowledge Base

Browse and search all stored memories.

Features:

* Memory Search
* Category Filters
* Workspace Filters
* Edit Memory
* Delete Memory
* Pin Memory
* Memory Inspector

---

## Semantic Search Engine

Natural language search over memories.

Examples:

* Show everything related to Machine Learning
* Find memories about XGBoost
* Show all project-related memories

Powered by embeddings and vector similarity search.

---

## Knowledge Graph

Visual representation of relationships between memories.

Example:

Akshay
├── Skill → Python
├── Skill → Machine Learning
├── Project → MemoryOS
├── Project → AI Data Quality Copilot
└── Goal → AI Engineer

The graph helps visualize how information is connected throughout the memory system.

---

## Multimodal Intelligence

MemoryOS supports knowledge extraction from files and images.

Supported formats:

### Images

* PNG
* JPG
* JPEG
* WEBP

Capabilities:

* OCR Text Extraction
* Memory Creation from Images

### Documents

* PDF
* DOCX
* XLSX
* CSV

Capabilities:

* Content Extraction
* Knowledge Parsing
* Memory Generation

---

## Export System

Export conversations and knowledge in multiple formats.

Supported exports:

* PDF
* DOCX
* CSV
* Excel

---

## Analytics Dashboard

### Chat Analytics

* Total Chats
* Active Chats
* Archived Chats
* Branch Count
* Message Count

### Memory Analytics

* Total Memories
* Memory Growth
* Category Distribution
* Retrieval Statistics

### Search Analytics

* Search Frequency
* Most Retrieved Memories
* Retrieval Hit Rate

### Workspace Analytics

* Workspace Activity
* Memory Distribution
* Conversation Trends

---

# AI Architecture

User Query
↓
Chat History
↓
Memory Retrieval (RAG)
↓
Semantic Search
↓
Relevant Memories
↓
Context Assembly
↓
Prompt Engineering Layer
↓
Groq LLM
↓
Response Generation
↓
Memory Extraction
↓
Embedding Generation
↓
ChromaDB + PostgreSQL

---

# System Architecture

Frontend
↓
FastAPI Backend
↓
LangGraph Workflow
↓
Memory Engine
↓
ChromaDB + PostgreSQL
↓
Groq LLM

---

# Database Architecture

## PostgreSQL (Neon)

Stores:

* Users
* Workspaces
* Chats
* Chat Branches
* Messages
* Memories
* Memory Categories
* Relationships
* Analytics
* Retrieval Logs

---

## ChromaDB

Stores:

* Memory Embeddings
* Chat Summaries
* Vector Indexes
* Semantic Search Data
* Compressed Memories

---

# Tech Stack

## Frontend

* React
* TypeScript
* Vite
* Tailwind CSS
* Zustand
* Framer Motion
* Lucide React

---

## Backend

* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* Python

---

## AI & GenAI

* Groq
* LangChain
* LangGraph
* ChromaDB
* Sentence Transformers
* Tavily API (Real-time web search)
* Retrieval-Augmented Generation (RAG)
* Semantic Search
* Prompt Engineering
* Context Management
* Memory Systems
* Knowledge Graphs
* MatplotLib

---

## Memory & Retrieval

* Vector Search
* Embedding Generation
* Similarity Matching
* Memory Ranking
* Memory Compression
* Context Injection

---

## File Processing

* EasyOCR
* PyMuPDF
* Pandas
* OpenPyXL
* Python-Docx
* ReportLab

---

## Storage

* Neon PostgreSQL
* ChromaDB
* Cloudinary

---

## Deployment

* Docker (Local containerization)
* Render (Backend API hosting)
* Vercel (Frontend static hosting)

---



# Local Development

This project is organized as a monorepo with separate `backend` (FastAPI) and `frontend` (React + Vite) directories.

## Clone Repository

## Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

## Frontend Setup

```bash
cd frontend
npm install
```

## Environment Variables

### Backend Configuration
Create a `.env` file in the `backend/` directory (or use a root `.env` file for Docker Compose):

```env
DATABASE_URL=your_neon_database_url
GROQ_API_KEY=your_groq_api_key
CLOUDINARY_CLOUD_NAME=your_cloudinary_name
CLOUDINARY_API_KEY=your_cloudinary_api_key
CLOUDINARY_API_SECRET=your_cloudinary_api_secret
TAVILY_API_KEY=optional
```

### Frontend Configuration
Create a `.env` file in the `frontend/` directory:

```env
VITE_API_URL=http://localhost:8001
```

## Start Application

### Option 1: Docker Compose (Recommended)
Run both backend and frontend services using Docker Compose:

```bash
docker-compose up --build
```
This will start:
- Backend on [http://localhost:8001](http://localhost:8001)
- Frontend on [http://localhost:3000](http://localhost:3000)

### Option 2: Run Separately
Start Backend:
```bash
cd backend
python start.py
```

Start Frontend:
```bash
cd frontend
npm run dev
```

---

# Production Deployment

## Backend Deployment (Render)
1. Create a new **Web Service** on Render and connect your repository.
2. In the configuration settings, set the **Root Directory** to `backend`.
3. Set the **Build Command** to `pip install -r requirements.txt`.
4. Set the **Start Command** to `python start.py` (or `uvicorn app.main:app --host 0.0.0.0 --port $PORT`).
5. Add your environment variables (`DATABASE_URL`, `GROQ_API_KEY`, etc.) in the Render dashboard.

## Frontend Deployment (Vercel)
1. Create a new project on Vercel and connect your repository.
2. Under project settings, set the **Root Directory** to `frontend`.
3. Vercel will automatically detect Vite settings (Build command: `npm run build`, Output directory: `dist`).
4. Under Environment Variables, add `VITE_API_URL` pointing to your deployed Render URL: `https://memory-os-80fm.onrender.com`.
5. Deploy!

---

# Live Demo

**Demo URL**

```text
ADD_DEPLOYMENT_URL_HERE
```

---

# What This Project Demonstrates

* Production-Grade RAG Systems
* Long-Term Memory Architectures
* Vector Database Engineering
* LangGraph Agent Workflows
* LangChain Retrieval Pipelines
* Embedding-Based Search Systems
* Context Engineering
* Knowledge Graph Construction
* Multimodal AI Processing
* Full-Stack AI Development
* Dockerized Applications
* Cloud Deployment
* LLM Engineering Best Practices
* Retrieval Infrastructure
* Persistent AI Memory Systems

---

# Future Improvements

* Multi-Agent Collaboration
* Shared Team Memory
* Memory Reflection Loops
* Advanced Memory Compression
* Hybrid Search (Vector + Keyword)
* Real-Time Collaboration
* Memory Versioning
* Reinforcement-Based Memory Ranking

---

# License

MIT License

---

Built as a production-grade GenAI engineering project focused on persistent memory systems, retrieval architectures, and real-world LLM application development.
#

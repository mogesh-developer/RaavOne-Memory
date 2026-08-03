<div align="center">

# 🧠 RaavOne Memory Engine

[![Python Version](https://img.shields.io/badge/Python-3.10%2B-3776AB.svg?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100%2B-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-red.svg?style=for-the-badge&logo=sqlalchemy&logoColor=white)](https://www.sqlalchemy.org/)
[![Pydantic v2](https://img.shields.io/badge/Pydantic-v2-E92063.svg?style=for-the-badge&logo=pydantic&logoColor=white)](https://docs.pydantic.dev/)
[![Status](https://img.shields.io/badge/Status-Active%20Development-success.svg?style=for-the-badge)](#)

**An intelligent, local-first long-term memory & user profiling engine built for autonomous AI agents and chat assistants.**

[Why Use This?](#-why-raavone-memory-use-case) •
[Core Capabilities](#-core-capabilities--functions) •
[Data Flow](#-how-it-works-data-flow) •
[API Reference](#-detailed-api-reference) •
[Getting Started](#-getting-started)

---

</div>

## 🎯 Why RaavOne Memory? (Use Case)

Standard LLM chat applications suffer from **context amnesia**—once a session ends, the AI forgets everything about the user.

**RaavOne Memory** acts as a long-term memory backend for AI assistants:
- 💾 **Session History**: Persists every chat message per session.
- 🔍 **Automated Fact Extraction**: Automatically analyzes user messages to identify key skills, tech stack, interests, and projects.
- 📈 **Importance Weighting**: Increments importance scores when user facts (e.g. `Python`, `FastAPI`, `AI`) are repeatedly mentioned across sessions.
- ⚡ **Zero Cloud Dependency**: Lightweight, local SQLite database backend for maximum user privacy.

---

## 🔥 Core Capabilities & Functions

### 1. 💬 Chat & Session Tracking (`/session`)
- Starts isolated user sessions with start timestamps (`/session/start`).
- Fetches all historical messages associated with a specific `session_id` (`/session/{session_id}`).

### 2. 📝 Message Logging & Querying (`/memory`)
- Logs raw incoming user/assistant messages (`/memory/save`).
- Retrieves complete raw message history for a user across all sessions (`/memory/history/{user_id}`).
- Returns all structured long-term memory facts stored for a user (`/memory/all/{user_id}`).

### 3. 🧠 Smart Fact Extraction (`/memory/extract`)
- Scans chat sessions to extract categories such as `skill`, `interest`, or `project`.
- Deduplicates memory entries and updates importance scores (`importance + 1`) automatically when repeated.

---

## 🔄 How It Works (Data Flow)

```mermaid
sequenceDiagram
    autonumber
    actor User as User / Frontend Agent
    participant SessionRoute as Session API
    participant MemoryRoute as Memory API
    participant ExtractService as Extraction Engine
    participant DB as SQLite DB

    User->>SessionRoute: POST /session/start { user_id }
    SessionRoute->>DB: Create & return session_id
    
    User->>MemoryRoute: POST /memory/save { user_id, session_id, role, text }
    MemoryRoute->>DB: Save raw chat message
    
    User->>ExtractService: POST /memory/extract/{session_id}
    ExtractService->>DB: Query session messages
    ExtractService->>ExtractService: Detect key entities (skills, interests, projects)
    ExtractService->>DB: Upsert memories & update importance score
    ExtractService-->>User: Return structured memories
```

---

## 📡 Detailed API Reference

| Section | Method | Endpoint | Description |
| :--- | :---: | :--- | :--- |
| **System** | `GET` | `/` | Service health status check |
| **Session** | `POST` | `/session/start` | Create a new user session ID |
| **Session** | `GET` | `/session/{session_id}` | Retrieve all chat messages in a session |
| **Memory** | `POST` | `/memory/save` | Store a new raw conversation message |
| **Memory** | `GET` | `/memory/history/{user_id}` | Fetch full message history for a user |
| **Memory** | `GET` | `/memory/all/{user_id}` | Fetch all extracted long-term memory facts |
| **Extraction**| `POST` | `/memory/extract/{session_id}` | Parse session & extract skills/projects/interests |

---

## 🗄️ Database Schema Overview

```mermaid
erDiagram
    USERS ||--o{ SESSIONS : has
    USERS ||--o{ MESSAGES : sends
    USERS ||--o{ MEMORIES : owns
    SESSIONS ||--o{ MESSAGES : contains

    USERS {
        string id PK
        string username
    }
    SESSIONS {
        string session_id PK
        string user_id FK
        datetime started_at
    }
    MESSAGES {
        int id PK
        string session_id FK
        string user_id FK
        string role
        string text
    }
    MEMORIES {
        int id PK
        string user_id FK
        string category
        string content
        int importance
        string source_session
    }
```

---

## 🚀 Getting Started

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/mogesh-developer/RaavOne-Memory.git
cd RaavOne-Memory
poetry install
```

### 2. Run Application Server
```bash
poetry run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Interactive Documentation
Access auto-generated interactive OpenAPI docs:
- **Swagger UI**: [http://localhost:8000/docs](http://localhost:8000/docs)
- **ReDoc**: [http://localhost:8000/redoc](http://localhost:8000/redoc)

---

<div align="center">

Built with ❤️ by [mogesh-developer](https://github.com/mogesh-developer)

</div>

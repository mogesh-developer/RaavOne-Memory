# 📡 RaavOne Memory API Specifications Documentation
*(Swagger & Endpoints Complete Specifications)*

Welcome to the API specifications document for **RaavOne Memory Engine**. 

FastAPI provides an automatic, interactive API explorer:
*   **Swagger UI**: `http://localhost:8000/docs`
*   **ReDoc**: `http://localhost:8000/redoc`

---

## 🔑 Base Configurations
*   **Default Base URL**: `http://localhost:8000`
*   **Prefix**: All memory routes use the `/memory` path prefix.

---

## 🌐 Endpoint Details

### 1. Start User Chat Session
*   **Route**: `POST /session/start`
*   **Description**: Creates a new chat session for a user or returns the current active one.
*   **Request Body**:
    ```json
    {
      "user_id": "string"
    }
    ```
*   **Response**:
    ```json
    {
      "session_id": "3c90a182-82bf-41bc-a8f8-b570e608034d",
      "user_id": "mogesh"
    }
    ```

---

### 2. Fetch Session Chat Log
*   **Route**: `GET /session/{session_id}`
*   **Description**: Returns the chronological chat messages of a specific session.
*   **Response**:
    ```json
    [
      {
        "id": 1,
        "session_id": "3c90a182-82bf-41bc-a8f8-b570e608034d",
        "role": "user",
        "text": "Hi, I am learning FastAPI.",
        "created_at": "2026-08-04T12:00:00"
      }
    ]
    ```

---

### 3. Log a Message
*   **Route**: `POST /memory/save`
*   **Description**: Logs a raw interaction between user and assistant.
*   **Request Body**:
    ```json
    {
      "user_id": "string",
      "role": "string",
      "text": "string",
      "session_id": "string"
    }
    ```
*   **Response**:
    ```json
    {
      "status": "success",
      "id": 4
    }
    ```

---

### 4. Fetch User Memory History
*   **Route**: `GET /memory/history/{user_id}`
*   **Description**: Fetches all raw logs of user messages across all sessions.
*   **Response**:
    ```json
    [
      {
        "role": "user",
        "text": "Suggest a backend stack"
      }
    ]
    ```

---

### 5. Semantic Memory Search
*   **Route**: `POST /memory/search`
*   **Description**: Searches user memories using vector similarity.
*   **Request Body**:
    ```json
    {
      "user_id": "string",
      "query": "string"
    }
    ```
*   **Response**:
    ```json
    {
      "documents": [
        ["Learns FastAPI", "Codes in Python"]
      ]
    }
    ```

---

### 6. User Profile Summary
*   **Route**: `GET /memory/profile/{user_id}`
*   **Description**: Gathers all memories and calls the LLM to output a Markdown formatted user profile.
*   **Response**:
    ```json
    {
      "user_id": "mogesh",
      "profile_summary": "* **Key Skills:**\n  - Python\n  - FastAPI"
    }
    ```

---

### 7. Chronological Timeline
*   **Route**: `GET /memory/timeline/{user_id}`
*   **Description**: Builds a visual milestone progress graph of the user's chronological path.
*   **Response**:
    ```json
    {
      "user_id": "mogesh",
      "timeline": "2026\n↓\n2026-08-04\n  • Started Python FastAPI development"
    }
    ```

---

### 8. Memory Metrics Analytics
*   **Route**: `GET /memory/analytics/{user_id}`
*   **Description**: Returns statistics regarding total counts, category breakdowns, and average importance.
*   **Response**:
    ```json
    {
      "user_id": "mogesh",
      "analytics": {
        "total_memories": 12,
        "category_breakdown": {
          "Skills": 8,
          "Preferences": 4
        },
        "average_importance": 4.25,
        "last_active": "2026-08-04T13:25:27"
      }
    }
    ```

---

### 9. Garbage Collection Forgetting Engine
*   **Route**: `POST /memory/cleanup`
*   **Description**: Runs cutoff cleanup. Removes memories older than `days` threshold that are below `importance_limit`.
*   **Query Parameters**:
    *   `days` (default `30`): Cutoff threshold.
    *   `importance_limit` (default `3`): Maximum importance score eligible for removal.
*   **Response**:
    ```json
    {
      "status": "success",
      "forgotten_memories_count": 2
    }
    ```

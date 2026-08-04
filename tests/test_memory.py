import pytest
from app.models.memory import Memory

def test_save_memory_endpoint(client):
    response = client.post(
        "/memory/save",
        json={
            "user_id": "test_user",
            "role": "user",
            "text": "Python is my favorite coding language.",
            "session_id": "session_1"
        }
    )
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert "id" in data

def test_get_history_endpoint(client):
    # First save a memory
    client.post(
        "/memory/save",
        json={
            "user_id": "test_user",
            "role": "user",
            "text": "FastAPI is fast.",
            "session_id": "session_1"
        }
    )
    response = client.get("/memory/history/test_user")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 1
    assert data[0]["text"] == "FastAPI is fast."

def test_all_memories_endpoint(client, db_session):
    # Seed database directly
    m = Memory(user_id="test_user", category="Skill", content="FastAPI")
    db_session.add(m)
    db_session.commit()

    response = client.get("/memory/all/test_user")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["content"] == "FastAPI"

def test_cleanup_expired_memories_endpoint(client, db_session):
    # Seed an old record
    from datetime import datetime, timedelta
    old_time = datetime.utcnow() - timedelta(days=40)
    m = Memory(
        user_id="test_user",
        category="Skill",
        content="Old React Memory",
        importance=1,
        updated_at=old_time,
        created_at=old_time
    )
    db_session.add(m)
    db_session.commit()

    response = client.post("/memory/cleanup?days=30&importance_limit=2")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "success"
    assert data["forgotten_memories_count"] == 1

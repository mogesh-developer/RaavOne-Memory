import pytest
from app.models.memory import Memory

def test_search_endpoint(client, db_session):
    # Seed memories in SQLite
    m1 = Memory(id=1, user_id="test_user", category="Skill", content="Python coding", importance=1)
    m2 = Memory(id=2, user_id="test_user", category="Skill", content="FastAPI backend", importance=2)
    db_session.add(m1)
    db_session.add(m2)
    db_session.commit()

    response = client.post(
        "/memory/search",
        json={"user_id": "test_user", "query": "backend development"}
    )
    assert response.status_code == 200
    data = response.json()
    # It should return ranked memories based on mock query
    assert "documents" in data
    assert len(data["documents"][0]) > 0

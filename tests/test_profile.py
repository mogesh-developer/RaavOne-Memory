import pytest
from app.models.memory import Memory

def test_profile_summary_endpoint(client, db_session):
    # Seed a memory
    m = Memory(user_id="test_user", category="Skill", content="Python coding")
    db_session.add(m)
    db_session.commit()

    response = client.get("/memory/profile/test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert "profile_summary" in data
    assert "Mocked" in data["profile_summary"] or "Failed" not in data["profile_summary"]

def test_timeline_endpoint(client, db_session):
    # Seed a memory
    m = Memory(user_id="test_user", category="Project", content="Started RaavOne Memory")
    db_session.add(m)
    db_session.commit()

    response = client.get("/memory/timeline/test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert "timeline" in data

def test_analytics_endpoint(client, db_session):
    # Seed memories
    m1 = Memory(user_id="test_user", category="Skill", content="Python")
    m2 = Memory(user_id="test_user", category="Preference", content="Likes Coffee")
    db_session.add_all([m1, m2])
    db_session.commit()

    response = client.get("/memory/analytics/test_user")
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["analytics"]["total_memories"] == 2
    assert "Skill" in data["analytics"]["category_breakdown"]
    assert "Preference" in data["analytics"]["category_breakdown"]

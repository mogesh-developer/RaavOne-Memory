import pytest
from app.models.session import Session as ChatSession

def test_chat_endpoint(client):
    response = client.post(
        "/chat",
        json={"user_id": "test_user", "message": "Hi, suggest a backend framework."}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == "test_user"
    assert data["message"] == "Hi, suggest a backend framework."
    assert "response" in data
    assert data["response"] == "Mocked personalized assistant response text."

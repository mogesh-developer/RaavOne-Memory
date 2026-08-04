import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool
from app.database import Base, get_db
from app.main import app
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# 1. Setup in-memory SQLite database engine
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)
    app.dependency_overrides.clear()

@pytest.fixture(autouse=True)
def mock_embedding_and_llm():
    """Automatically mock external SDK embedding & Groq chat calls during test runtime."""
    # Create the mock chat instance and class
    mock_chat_inst = MagicMock()
    mock_chat_inst.generate.return_value = "Mocked personalized assistant response text."
    mock_chat_inst.generate_json.return_value = MagicMock(updates_id=None, merged_content=None)
    
    mock_chat_class = MagicMock(return_value=mock_chat_inst)
    
    # Overwrite on all target service modules directly to bypass import bindings
    import app.services.chat_service
    import app.services.profile_service
    import app.services.timeline_service
    import app.services.extraction_service
    
    orig_chat = app.services.chat_service.ChatModel
    orig_profile = app.services.profile_service.ChatModel
    orig_timeline = app.services.timeline_service.ChatModel
    
    app.services.chat_service.ChatModel = mock_chat_class
    app.services.profile_service.ChatModel = mock_chat_class
    app.services.timeline_service.ChatModel = mock_chat_class
    app.services.extraction_service.ChatModel = mock_chat_class
    
    with patch("app.services.embedding_service.create_embedding") as mock_embed, \
         patch("app.services.extraction_service.create_embedding") as mock_embed2, \
         patch("app.services.extraction_service.extract_memory") as mock_extract, \
         patch("app.services.vector_service.add_memory") as mock_add_vector, \
         patch("app.services.search_service.semantic_search") as mock_search_service:
        
        # Setup default mock values
        mock_embed.return_value = [0.1] * 128
        mock_embed2.return_value = [0.1] * 128
        
        mock_extract.return_value = MagicMock(memories=[])
        mock_search_service.return_value = {
            "documents": [["Mock memory 1", "Mock memory 2"]],
            "ids": [["1", "2"]],
            "distances": [[0.1, 0.2]]
        }
        
        yield {
            "embed": mock_embed,
            "chat": mock_chat_inst,
            "search": mock_search_service,
            "extract": mock_extract
        }
        
        # Restore original classes after test
        app.services.chat_service.ChatModel = orig_chat
        app.services.profile_service.ChatModel = orig_profile
        app.services.timeline_service.ChatModel = orig_timeline
        if hasattr(app.services.extraction_service, "ChatModel"):
            delattr(app.services.extraction_service, "ChatModel")

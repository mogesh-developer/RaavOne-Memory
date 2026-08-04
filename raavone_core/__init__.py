from raavone import AIService as ChatModel
from raavone import EmbeddingService

class EmbeddingModel:
    def embed(self, text: str):
        import numpy as np
        res = EmbeddingService.generate_embeddings([text])
        if isinstance(res, np.ndarray):
            return res[0].tolist()
        return res[0]


class Memory:
    @staticmethod
    def chat(user_id: str, message: str) -> str:
        """Sends a message to the agent, retrieves context, and returns response."""
        from app.database import SessionLocal
        from app.services.chat_service import chat as chat_func
        
        db = SessionLocal()
        try:
            return chat_func(db, user_id, message)
        finally:
            db.close()

    @staticmethod
    def get_profile(user_id: str) -> str:
        """Retrieves summarized user profile persona."""
        from app.database import SessionLocal
        from app.services.profile_service import generate_user_profile
        
        db = SessionLocal()
        try:
            return generate_user_profile(db, user_id)
        finally:
            db.close()

    @staticmethod
    def get_timeline(user_id: str) -> str:
        """Retrieves chronological timeline milestone summary."""
        from app.database import SessionLocal
        from app.services.timeline_service import generate_user_timeline
        
        db = SessionLocal()
        try:
            return generate_user_timeline(db, user_id)
        finally:
            db.close()

    @staticmethod
    def get_analytics(user_id: str) -> dict:
        """Retrieves database counts and category breakdowns."""
        from app.database import SessionLocal
        from app.services.analytics_service import get_user_analytics
        
        db = SessionLocal()
        try:
            return get_user_analytics(db, user_id)
        finally:
            db.close()

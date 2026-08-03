from fastapi import FastAPI
from app.routes.memory import router as memory_router
from app.routes.session import router as session_router
from app.routes.extraction import router as extraction_router
from app.database import Base, engine

# Import models before create_all()
from app.models.user import User
from app.models.message import Message
from app.models.session import Session
from app.models.memory import Memory


Base.metadata.create_all(bind=engine)

app = FastAPI(title="RaavOne Memory")
app.include_router(memory_router)
app.include_router(session_router)
app.include_router(extraction_router)

@app.get("/")
def home():
    return {
        "project": "RaavOne Memory",
        "status": "Running"
    }
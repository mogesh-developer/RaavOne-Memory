from app.models.message import Message
from app.models.memory import Memory


def extract_memories(messages: list[Message]):

    memories = []

    for message in messages:

        text = message.text.lower()

        if "python" in text:

            memories.append({
                "category": "skill",
                "content": "Python"
            })

        if "fastapi" in text:

            memories.append({
                "category": "skill",
                "content": "FastAPI"
            })

        if "rag" in text:

            memories.append({
                "category": "project",
                "content": "RAG"
            })

        if "ai" in text:

            memories.append({
                "category": "interest",
                "content": "AI"
            })

    return memories

def save_memories(
    db,
    user_id: str,
    session_id: str,
    memories: list,
):

    saved_memories = []

    for memory in memories:

        item = Memory(
            user_id=user_id,
            category=memory["category"],
            content=memory["content"],
            source_session=session_id,
        )

        existing = (
    db.query(Memory)
    .filter(
        Memory.user_id == user_id,
        Memory.category == memory["category"],
        Memory.content == memory["content"],
    )
    .first()
)

    if existing:

        existing.importance += 1

        saved_memories.append(existing)

    else:

        item = Memory(
            user_id=user_id,
            category=memory["category"],
            content=memory["content"],
            source_session=session_id,
        )

        db.add(item)

        saved_memories.append(item)

    db.commit()

    return saved_memories
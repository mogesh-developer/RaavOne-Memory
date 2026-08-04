import json
from app.models.message import Message
from app.models.memory import Memory
from app.services.llm_service import extract_memory
from app.services.embedding_service import create_embedding


def build_conversation(messages):

    lines = []

    for message in messages:

        lines.append(
            f"{message.role}: {message.text}"
        )

    return "\n".join(lines)


def extract_memories(messages: list[Message]):

    conversation = build_conversation(messages)

    response = extract_memory(conversation)

    for memory in response.memories:
        print(memory.category, memory.content)

    return [{"category": m.category, "content": m.content} for m in response.memories]



def save_memories(
    db,
    user_id: str,
    session_id: str,
    memories: list,
):

    saved_memories = []

    for memory in memories:

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
            existing.updated_at = func.now()
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

    from app.services.vector_service import add_memory

    for item in saved_memories:
        db.refresh(item)
        
        # Add to ChromaDB vector store
        try:
            vector = create_embedding(item.content)
            print(vector[:5])
            add_memory(
                memory_id=str(item.id),
                content=item.content,
                embedding=vector,
                metadata={
                    "user_id": item.user_id,
                    "category": item.category,
                    "importance": item.importance,
                }
            )
        except Exception as e:
            print(f"Failed to index memory {item.id} to ChromaDB: {e}")

    return [
        {
            "id": m.id,
            "user_id": m.user_id,
            "category": m.category,
            "content": m.content,
            "importance": m.importance,
            "source_session": m.source_session,
            "created_at": m.created_at,
        }
        for m in saved_memories
    ]




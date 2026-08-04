import json
from sqlalchemy.sql import func
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
    from app.services.vector_service import add_memory
    from app.vector.chroma import collection
    from raavone_core import ChatModel
    from app.prompts.conflict_prompt import CONFLICT_RESOLUTION_PROMPT
    from raavone.schemas.memory_extraction import MemoryConflictCheck

    saved_memories = []

    for memory in memories:
        # A. Check for exact duplicate
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
            db.commit()
            db.refresh(existing)
            
            # Sync updated importance to Chroma
            try:
                vector = create_embedding(existing.content)
                collection.update(
                    ids=[str(existing.id)],
                    documents=[existing.content],
                    embeddings=[vector],
                    metadatas=[{
                        "user_id": user_id,
                        "category": existing.category,
                        "importance": existing.importance,
                    }]
                )
            except Exception as e:
                print(f"Failed to update Chroma metadata for {existing.id}: {e}")
                
            saved_memories.append(existing)
            continue

        # B. Check for semantic conflict/update in the same category
        existing_in_cat = (
            db.query(Memory)
            .filter(
                Memory.user_id == user_id,
                Memory.category == memory["category"],
            )
            .all()
        )

        updates_id = None
        merged_content = None

        if existing_in_cat:
            existing_str = "\n".join([f"ID: {m.id} - {m.content}" for m in existing_in_cat])
            prompt = CONFLICT_RESOLUTION_PROMPT.format(
                new_memory=memory["content"],
                existing_memories=existing_str
            )
            model = ChatModel()
            try:
                conflict_res = model.generate_json(prompt, MemoryConflictCheck)
                updates_id = conflict_res.updates_id
                merged_content = conflict_res.merged_content
            except Exception as e:
                print(f"Error checking conflict: {e}")

        if updates_id:
            # Conflict found: update existing SQLite record
            # Audited: Ensure we only update records belonging to the active user
            existing_record = (
                db.query(Memory)
                .filter(Memory.id == updates_id)
                .filter(Memory.user_id == user_id)
                .first()
            )
            if existing_record:
                existing_record.content = merged_content
                existing_record.updated_at = func.now()
                existing_record.importance += 1
                db.commit()
                db.refresh(existing_record)
                
                # Update ChromaDB vector
                try:
                    vector = create_embedding(merged_content)
                    collection.update(
                        ids=[str(existing_record.id)],
                        documents=[merged_content],
                        embeddings=[vector],
                        metadatas=[{
                            "user_id": user_id,
                            "category": existing_record.category,
                            "importance": existing_record.importance,
                        }]
                    )
                except Exception as e:
                    print(f"Failed to update Chroma vector: {e}")
                    
                saved_memories.append(existing_record)
                continue

        # C. Save as new memory
        item = Memory(
            user_id=user_id,
            category=memory["category"],
            content=memory["content"],
            source_session=session_id,
        )
        db.add(item)
        db.commit()
        db.refresh(item)

        # Add to ChromaDB vector store
        try:
            vector = create_embedding(item.content)
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
            print(f"Failed to add new memory {item.id} to ChromaDB: {e}")
            
        saved_memories.append(item)

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

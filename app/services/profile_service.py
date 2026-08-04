from sqlalchemy.orm import Session
from app.models.memory import Memory
from raavone_core import ChatModel
from app.prompts.profile_prompt import USER_PROFILE_PROMPT

def generate_user_profile(db: Session, user_id: str) -> str:
    # 1. Fetch memories
    memories = db.query(Memory).filter(Memory.user_id == user_id).all()
    if not memories:
        return "No memories recorded for this user yet."

    # 2. Format memory details
    memory_lines = []
    for m in memories:
        memory_lines.append(f"- [{m.category}] {m.content} (importance: {m.importance})")
    
    formatted_memories = "\n".join(memory_lines)

    # 3. Assemble prompt
    full_prompt = f"{USER_PROFILE_PROMPT}\n\nRetrieved User Memories:\n{formatted_memories}\n"

    # 4. Generate profile via LLM
    model = ChatModel()
    try:
        response = model.generate(full_prompt)
        return response
    except Exception as e:
        print(f"Error generating user profile: {e}")
        return "Failed to generate profile summary."

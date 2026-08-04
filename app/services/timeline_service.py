from sqlalchemy.orm import Session
from app.models.memory import Memory
from raavone_core import ChatModel


def generate_user_timeline(db: Session, user_id: str) -> str:
    # 1. Fetch memories sorted chronologically
    memories = (
        db.query(Memory)
        .filter(Memory.user_id == user_id)
        .order_by(Memory.created_at.asc())
        .all()
    )

    if not memories:
        return "No memory milestones recorded for this user yet."

    # 2. Format memories with their creation dates
    memory_lines = []
    for m in memories:
        date_str = m.created_at.strftime("%Y-%m-%d") if m.created_at else "Unknown Date"
        memory_lines.append(f"- [{date_str}] [{m.category}] {m.content}")

    formatted_memories = "\n".join(memory_lines)

    # 3. Ask LLM to format a visually appealing progress timeline
    prompt = f"""
You are an AI Timeline Engine.

Based on the chronological user memories below, build a clean progress timeline mapping out their journey.
Use years, dates, and vertical arrows (↓) or emojis to display progression clearly. Keep it concise.

Chronological Memories:
{formatted_memories}
"""

    model = ChatModel()
    try:
        response = model.generate(prompt)
        return response
    except Exception as e:
        print(f"Error generating timeline: {e}")
        return formatted_memories

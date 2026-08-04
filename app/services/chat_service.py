from sqlalchemy.orm import Session
from app.models.session import Session as ChatSession
from app.models.message import Message
from app.services.search_service import semantic_search
from app.services.context_service import build_context
from app.prompts.context_prompt import CONTEXT_PROMPT
from raavone_core import ChatModel


def chat(db: Session, user_id: str, message: str) -> str:
    """Orchestrates the personalized chat loop by loading user context and querying the LLM.

    Args:
        db (Session): SQLite database session.
        user_id (str): The identifier of the target user.
        message (str): The incoming chat query text from the user.

    Returns:
        str: Personalized assistant chat response.
    """
    # 1. Find or create an active chat session for the user
    session = (
        db.query(ChatSession)
        .filter(ChatSession.user_id == user_id)
        .order_by(ChatSession.started_at.desc())
        .first()
    )
    if not session:
        session = ChatSession(user_id=user_id)
        db.add(session)
        db.commit()
        db.refresh(session)
    
    session_id = session.session_id

    # 2. Save the user's message to SQLite
    user_msg = Message(
        session_id=session_id,
        user_id=user_id,
        role="user",
        text=message
    )
    db.add(user_msg)
    db.commit()

    # 3. Search top memories using our compound scoring ranker
    search_res = semantic_search(message, user_id=user_id)
    memories = search_res.get("documents", [[]])[0]

    # 4. Build context and assemble system prompt
    context_str = build_context(memories, message)
    full_prompt = f"{CONTEXT_PROMPT}\n\n{context_str}"

    # 5. Call LLM model to generate response
    model = ChatModel()
    try:
        response_text = model.generate(full_prompt)
    except Exception as e:
        print(f"Error calling LLM: {e}")
        response_text = "I'm having trouble connecting to my service right now."

    # 6. Save the assistant's response to SQLite
    assistant_msg = Message(
        session_id=session_id,
        user_id=user_id,
        role="assistant",
        text=response_text
    )
    db.add(assistant_msg)
    db.commit()

    return response_text
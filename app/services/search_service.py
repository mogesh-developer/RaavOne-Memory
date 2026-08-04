from datetime import datetime
from app.services.embedding_service import create_embedding
from app.vector.chroma import collection
from app.database import SessionLocal
from app.models.memory import Memory


def semantic_search(query: str, user_id: str = None) -> dict:
    """Executes a compound-ranked semantic search query on ChromaDB and SQLite candidates.

    Args:
        query (str): The natural language search term.
        user_id (str): The identifier of the querying user.

    Returns:
        dict: A dictionary containing ranked memory document strings inside 'documents'.
    """
    # 1. Generate Query Embedding
    embedding = create_embedding(query)

    # 2. Filter by User ID
    where_filter = {"user_id": user_id} if user_id else None

    # 3. Query ChromaDB for top 10 candidates
    results = collection.query(
        query_embeddings=[embedding],
        n_results=10,
        where=where_filter
    )

    if not results or "ids" not in results or not results["ids"] or not results["ids"][0]:
        return {"documents": [[]]}

    ids = results["ids"][0]
    distances = results["distances"][0]
    documents = results["documents"][0]

    # Map distance by memory ID
    distance_map = {ids[idx]: distances[idx] for idx in range(len(ids))}
    document_map = {ids[idx]: documents[idx] for idx in range(len(ids))}

    # Convert string IDs back to integer for SQLite lookup
    int_ids = []
    for item_id in ids:
        try:
            int_ids.append(int(item_id))
        except ValueError:
            pass

    # 4. Fetch candidate details from SQLite
    db = SessionLocal()
    try:
        # Audited: Enforce user_id isolation in SQLite fetch
        memories = (
            db.query(Memory)
            .filter(Memory.id.in_(int_ids))
            .filter(Memory.user_id == user_id)
            .all()
        )

    finally:
        db.close()

    # 5. Compute Compound Ranking Score for each Candidate
    ranked_memories = []
    now = datetime.utcnow()

    for memory in memories:
        str_id = str(memory.id)
        distance = distance_map.get(str_id, 1.0)
        content = document_map.get(str_id, memory.content)

        # A. Similarity Score: Convert distance (0 to 2) to similarity out of 10
        similarity_score = max(0.0, (1.0 - distance) * 10.0)

        # B. Recency Score: (Current Time - Memory.updated_at).days
        m_time = memory.updated_at or memory.created_at
        if m_time:
            m_time = m_time.replace(tzinfo=None)
            days_diff = (now - m_time).days
            recency_score = max(0.0, 10.0 - days_diff)
        else:
            recency_score = 5.0

        # C. Frequency Score: Min of 10.0 or importance * 1.5
        frequency_score = min(10.0, (memory.importance or 1) * 1.5)

        # D. Final Composite Score
        final_score = similarity_score + recency_score + frequency_score

        ranked_memories.append({
            "content": content,
            "score": final_score
        })

    # Sort candidates by final score in descending order
    ranked_memories.sort(key=lambda x: x["score"], reverse=True)

    # Slice the top 5 documents
    top_docs = [item["content"] for item in ranked_memories[:5]]

    return {
        "documents": [top_docs]
    }

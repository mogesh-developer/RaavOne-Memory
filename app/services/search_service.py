from app.services.embedding_service import create_embedding
from app.vector.chroma import collection


def semantic_search(query: str, user_id: str = None):

    embedding = create_embedding(query)

    where_filter = {"user_id": user_id} if user_id else None

    results = collection.query(
        query_embeddings=[embedding],
        n_results=5,
        where=where_filter
    )

    return results

from app.vector.chroma import collection

def add_memory(
    memory_id: str,
    content: str,
    embedding: list,
    metadata: dict,
):
    collection.add(
        ids=[str(memory_id)],
        documents=[content],
        embeddings=[embedding],
        metadatas=[metadata],
    )

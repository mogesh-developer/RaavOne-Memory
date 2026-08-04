import chromadb

client = chromadb.PersistentClient(
    path="./storage/chroma"
)

collection = client.get_or_create_collection(
    name="raavone_memory"
)

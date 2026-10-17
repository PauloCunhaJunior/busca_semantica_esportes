from chromadb import PersistentClient
from chromadb.utils.embedding_functions import SentenceTransformerEmbeddingFunction


embedding_fn = SentenceTransformerEmbeddingFunction(
    model_name="all-MiniLM-L6-v2"
)

client = PersistentClient(path="chroma_db")

collection = client.get_collection(
    name="esportes",
    embedding_function=embedding_fn
)

dados = collection.get(
    include=["embeddings"]
)

print(dados["embeddings"])
print("Dimensões de um embedding:", len(dados["embeddings"][0]))

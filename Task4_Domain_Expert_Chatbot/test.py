from src.data_loader import load_data
from src.embedding import create_embeddings
from retriever import Retriever
from src.chatbot import  get_query_embedding

print("Loading papers...")
df = load_data()

print("Creating embeddings...")
embeddings = create_embeddings(
    df["summary"].tolist()
)

retriever = Retriever(
    embeddings
)

query = "machine learning"

query_embedding = get_query_embedding(
    query
)

indices = retriever.search(
    query_embedding
)

print("\nTop Results:\n")

for idx in indices:
    print(df.iloc[idx]["title"])
    print("-" * 50)
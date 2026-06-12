import json

from src.embeddings import create_embeddings
from src.vector_store import VectorStore

with open("data/articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

texts = [article["summary"] for article in articles]

embeddings = create_embeddings(texts)

vector_db = VectorStore(embeddings)

query = "data science"

query_embedding = create_embeddings([query])[0]

indices = vector_db.search(query_embedding)

print("\nTop Results:\n")

for idx in indices:
    print(articles[idx]["title"])
    print("-" * 50)
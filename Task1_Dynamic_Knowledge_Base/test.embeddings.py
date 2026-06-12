import json
from src.embeddings import create_embeddings

with open("data/articles.json", "r", encoding="utf-8") as f:
    articles = json.load(f)

texts = [article["summary"] for article in articles]

embeddings = create_embeddings(texts)

print("Number of articles:", len(texts))
print("Embedding shape:", embeddings.shape)
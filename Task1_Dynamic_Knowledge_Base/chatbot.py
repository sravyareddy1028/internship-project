from src.embeddings import create_embeddings

def get_query_embedding(query):
    embedding = create_embeddings([query])
    return embedding[0]
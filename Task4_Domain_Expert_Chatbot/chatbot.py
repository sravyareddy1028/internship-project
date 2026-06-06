from sentence_transformers import SentenceTransformer

model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

def get_query_embedding(query):
    return model.encode(
        [query],
        convert_to_numpy=True
    )[0]
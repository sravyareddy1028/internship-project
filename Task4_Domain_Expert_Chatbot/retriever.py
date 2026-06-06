import numpy as np

class Retriever:

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def search(self, query_embedding, top_k=5):

        query_embedding = query_embedding / np.linalg.norm(query_embedding)

        embeddings_norm = self.embeddings / np.linalg.norm(
            self.embeddings,
            axis=1,
            keepdims=True
        )

        similarities = np.dot(
            embeddings_norm,
            query_embedding
        )

        return similarities.argsort()[-top_k:][::-1]
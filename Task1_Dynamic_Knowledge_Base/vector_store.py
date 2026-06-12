import faiss
import numpy as np

class VectorStore:
    def __init__(self, embeddings):
        self.dimension = embeddings.shape[1]

        self.index = faiss.IndexFlatL2(self.dimension)

        self.index.add(
            np.array(embeddings).astype("float32")
        )

    def search(self, query_embedding, top_k=5):
        distances, indices = self.index.search(
            np.array([query_embedding]).astype("float32"),
            top_k
        )

        return indices[0]
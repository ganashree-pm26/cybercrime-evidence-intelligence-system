import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.embedding_model import EmbeddingModel
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class SimilarityFinder:
    def __init__(self):
        self.embedding_model = EmbeddingModel()

    def find_similar_cases(self, query_text: str, stored_embeddings: dict, top_k: int = 5) -> list:
        query_embedding = np.array(self.embedding_model.encode(query_text)).reshape(1, -1)

        similarities = {}
        for case_id, embedding in stored_embeddings.items():
            emb_array = np.array(embedding).reshape(1, -1)
            sim = cosine_similarity(query_embedding, emb_array)[0][0]
            similarities[case_id] = sim

        # Sort by similarity descending
        sorted_cases = sorted(similarities.items(), key=lambda x: x[1], reverse=True)
        return sorted_cases[:top_k]
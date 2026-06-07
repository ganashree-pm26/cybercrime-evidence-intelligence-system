import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from models.embedding_model import EmbeddingModel

class EmbeddingService:
    def __init__(self):
        self.model = EmbeddingModel()

    def generate_embedding(self, text: str) -> list:
        return self.model.encode(text)
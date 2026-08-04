from raavone import AIService as ChatModel
from raavone import EmbeddingService

class EmbeddingModel:
    def embed(self, text: str):
        import numpy as np
        res = EmbeddingService.generate_embeddings([text])
        if isinstance(res, np.ndarray):
            return res[0].tolist()
        return res[0]

from raavone_core import EmbeddingModel

model = EmbeddingModel()


def create_embedding(text: str):

    return model.embed(text)

from sentence_transformers import SentenceTransformer


class EmbeddingModel:

    def __init__(self, model_name="all-MiniLM-L6-v2"):

        self.model = SentenceTransformer(model_name)

    def generate_embeddings(self, texts):

        embeddings = self.model.encode(
            texts,
            convert_to_numpy=True
        )

        return embeddings.tolist()

    def generate_query_embedding(self, query):

        embedding = self.model.encode(
            query,
            convert_to_numpy=True
        )

        return embedding.tolist()
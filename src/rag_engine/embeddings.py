from sentence_transformers import SentenceTransformer

class EmbeddingModel:
    def __init__(self, model_name="all-MiniLM-L6-v2"):
        """
        Initializes the embedding model.
        Using 'all-MiniLM-L6-v2' which is the standard for fast, local, free embeddings.
        It maps sentences to a 384 dimensional dense vector space.
        """
        print(f"⏳ Loading Embedding Model ({model_name})...")
        self.model = SentenceTransformer(model_name)
        print("✅ Embedding Model Loaded.")

    def get_embedding(self, text: str):
        """Generates a vector embedding for the given text."""
        # Convert text to vector
        embedding = self.model.encode(text)
        return embedding.tolist()
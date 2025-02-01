from sentence_transformers import SentenceTransformer

class DocumentEmbedder:
    def __init__(self):
        self.model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1", truncate_dim=512, trust_remote_code=True)

    def embed_documents(self, documents):
        if not isinstance(documents, list):
            raise ValueError("Documents should be provided as a list of strings.")
        embeddings = self.model.encode(documents)
        return [embedding for embedding in embeddings]
    
    def embed_query(self, query):
        if not isinstance(query, str):
            raise ValueError("Query should be provided as a string.")
        return self.model.encode(query)
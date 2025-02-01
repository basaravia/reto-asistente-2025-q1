from utils.DocumentEmbedder import DocumentEmbedder
import os
import chromadb
from langchain_chroma import Chroma

COLLECTION_NAME = os.getenv("COLLECTION_NAME")

class RagService():
    def __init__(self):
        self.embedder = DocumentEmbedder()
        self.retriever = self._get_retriever()

    def _get_retriever(self):
        persistent_client = chromadb.HttpClient()
        vector_store_client = Chroma(
            client=persistent_client,
            collection_name=COLLECTION_NAME,
            embedding_function=self.embedder,
        )
        return vector_store_client.as_retriever(search_type="similarity", search_kwargs={"k": 5})

    def execute_rag(self, query):
        return self.retriever.invoke(query)
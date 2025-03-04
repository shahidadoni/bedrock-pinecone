from pinecone import Pinecone, ServerlessSpec
from typing import List, Dict, Any
from src.config import PINECONE_API_KEY, PINECONE_ENVIRONMENT, PINECONE_INDEX_NAME, VECTOR_DIMENSION

class PineconeManager:
    def __init__(self):
        self.pc = Pinecone(api_key=PINECONE_API_KEY)
        self.index = self._get_or_create_index()

    def _get_or_create_index(self):
        """Get existing index or create a new one if it doesn't exist."""
        if PINECONE_INDEX_NAME not in self.pc.list_indexes().names():
            self.pc.create_index(
                name=PINECONE_INDEX_NAME,
                dimension=VECTOR_DIMENSION,
                metric='cosine',
                spec=ServerlessSpec(
                    cloud='aws',
                    region=PINECONE_ENVIRONMENT
                )
            )
        return self.pc.Index(PINECONE_INDEX_NAME)

    def upsert_vectors(self, vectors: List[Dict[str, Any]]):
        """Upsert vectors to Pinecone index."""
        self.index.upsert(vectors=vectors)

    def query_vectors(self, query_vector: List[float], top_k: int = 3) -> List[Dict[str, Any]]:
        """Query the index for similar vectors."""
        results = self.index.query(
            vector=query_vector,
            top_k=top_k,
            include_metadata=True
        )
        return results.matches

    def delete_index(self):
        """Delete the Pinecone index."""
        self.pc.delete_index(PINECONE_INDEX_NAME) 
import chromadb
import uuid
import time
from typing import List, Dict, Any

class VectorStore:
    def __init__(self, persist_directory="data/chroma_db"):
        self.client = chromadb.PersistentClient(path=persist_directory)
        self.collection = self.client.get_or_create_collection(name="discord_memory")

    def add_memory(self, text: str, metadata: Dict[str, Any]):
        """
        Stores a text chunk with metadata into ChromaDB.
        """
        # Ensure metadata values are strings or numbers (Chroma requirement)
        clean_metadata = {k: str(v) for k, v in metadata.items()}
        
        self.collection.add(
            documents=[text],
            metadatas=[clean_metadata],
            ids=[str(uuid.uuid4())]  # Generate unique ID for every memory
        )

    def search(self, query_text: str, n_results=3):
        """
        Semantic search returning results AND their relevance scores.
        """
        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            # We explicitly ask for distances
            include=['documents', 'distances']
        )
        
        # Return a list of tuples: (document_text, distance_score)
        # Lower distance = Higher relevance
        if results and results['documents']:
            return list(zip(results['documents'][0], results['distances'][0]))
        return []
        
    def count(self):
        """Returns the total number of memories stored."""
        return self.collection.count()
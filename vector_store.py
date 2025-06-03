import os
from typing import List, Dict, Any, Optional
import chromadb
from chromadb.config import Settings
from langchain_community.vectorstores import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from config import config

class VectorStore:
    def __init__(self):
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=config.OPENAI_API_KEY,
            model=config.EMBEDDING_MODEL
        )
        self.vector_db = None
        self.initialize_db()

    def initialize_db(self):
        """Initialize ChromaDB vector store."""
        try:
            # Ensure directory exists
            os.makedirs(config.VECTOR_DB_PATH, exist_ok=True)

            # Initialize Chroma
            self.vector_db = Chroma(
                persist_directory=config.VECTOR_DB_PATH,
                embedding_function=self.embeddings,
                collection_name="ciroh_documents"
            )
            print("Vector database initialized successfully")
        except Exception as e:
            print(f"Error initializing vector database: {str(e)}")
            raise

    def add_documents(self, documents: List[Document]) -> None:
        """Add documents to the vector store."""
        if not documents:
            print("No documents to add")
            return

        try:
            self.vector_db.add_documents(documents)
            print(f"Added {len(documents)} documents to vector store")
        except Exception as e:
            print(f"Error adding documents to vector store: {str(e)}")
            raise

    def similarity_search(self, query: str, k: int = 5) -> List[Document]:
        """Perform similarity search."""
        try:
            results = self.vector_db.similarity_search(query, k=k)
            return results
        except Exception as e:
            print(f"Error performing similarity search: {str(e)}")
            return []

    def similarity_search_with_score(self, query: str, k: int = 5) -> List[tuple]:
        """Perform similarity search with scores."""
        try:
            results = self.vector_db.similarity_search_with_score(query, k=k)
            return results
        except Exception as e:
            print(f"Error performing similarity search with scores: {str(e)}")
            return []

    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the vector store collection."""
        try:
            collection = self.vector_db._collection
            count = collection.count()
            return {
                "total_documents": count,
                "collection_name": collection.name
            }
        except Exception as e:
            print(f"Error getting collection stats: {str(e)}")
            return {}
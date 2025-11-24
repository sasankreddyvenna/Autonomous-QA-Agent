import chromadb
import uuid
import os
from typing import List, Dict, Any, cast

PERSIST_DIR = os.path.join(
    os.path.dirname(os.path.dirname(__file__)),
    "..",
    "storage",
    "chroma_db"
)

class ChromaVectorDB:
    def __init__(self, collection_name: str = "qa_collection"):
        # Use a persistent Chroma client
        self.client = chromadb.PersistentClient(path=PERSIST_DIR)
        self.collection = self.client.get_or_create_collection(
            name=collection_name,
            metadata={"hnsw:space": "cosine"}
        )

    def add_documents(self, chunks: List[Dict[str, Any]], embeddings: List[List[float]]):
        # Assign IDs if missing
        ids = [chunk.get("id", str(uuid.uuid4())) for chunk in chunks]
        for i, chunk in enumerate(chunks):
            chunk["id"] = ids[i]

        # Extract document text
        contents = [chunk["text"] for chunk in chunks]

        # ✅ Metadata fix
        metadatas: List[Dict[str, str]] = [
            {"source": str(chunk.get("source", ""))}
            for chunk in chunks
        ]

        # ✅ Cast embeddings to satisfy type checker
        embeddings_cast = cast(List[List[float]], embeddings)

        self.collection.add(
            ids=ids,
            embeddings=embeddings,  # type: ignore[arg-type]
            metadatas=metadatas,          # type: ignore[arg-type]
            documents=contents
        )

    def query(self, text: str, n_results: int = 5):
        return self.collection.query(
            query_texts=[text],
            n_results=n_results
        )

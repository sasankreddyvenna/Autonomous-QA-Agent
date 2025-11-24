# backend/services/embeddings/embedder.py

from .model_loader import get_sentence_transformer
from typing import List, Dict
import numpy as np

MODEL_NAME = "all-MiniLM-L6-v2"

# Load model only once (important!)
MODEL = get_sentence_transformer(MODEL_NAME)

def _normalize(vec: np.ndarray) -> np.ndarray:
    """L2-normalize embeddings for consistent cosine similarity scoring."""
    norm = np.linalg.norm(vec)
    return vec / norm if norm > 0 else vec


def embed_chunks(chunks: List[Dict], batch_size: int = 16) -> List[List[float]]:
    """
    Convert document chunks into embeddings.
    - Uses batching
    - Normalizes vectors (improves Chroma performance)
    - Skips empty chunks
    """
    texts = [c.get("text", "") for c in chunks]

    # Handle empty dataset (fail-safe)
    if not texts:
        return []

    embeddings = []
    total = len(texts)

    for i in range(0, total, batch_size):
        batch = texts[i : i + batch_size]

        # Replace empty strings with a placeholder
        safe_batch = [" " if not txt.strip() else txt for txt in batch]

        try:
            vecs = MODEL.encode(safe_batch, show_progress_bar=False)
        except Exception as e:
            print(f"[Embedding Error] batch {i}: {e}")
            vecs = [np.zeros((384,))] * len(safe_batch)

        # Normalize each embedding
        norm_vecs = [_normalize(v) for v in vecs]

        for v in norm_vecs:
            if hasattr(v, "tolist"):
                embeddings.append(v.tolist())
            else:
                embeddings.append(list(v))

    return embeddings

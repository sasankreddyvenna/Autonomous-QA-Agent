# backend/services/embeddings/model_loader.py
from sentence_transformers import SentenceTransformer

# Lazily load model to avoid import cost at module import time
_MODEL = None

def get_sentence_transformer(model_name: str = "all-MiniLM-L6-v2"):
    global _MODEL
    if _MODEL is None:
        _MODEL = SentenceTransformer(model_name)
    return _MODEL

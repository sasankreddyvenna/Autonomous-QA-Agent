# backend/tests/test_embeddings.py
def test_embed_simple():
    from services.embeddings.embedder import embed_chunks
    chunks = [{"text": "hello world", "source": "test"}]
    vecs = embed_chunks(chunks)
    assert isinstance(vecs, list) and len(vecs) == 1

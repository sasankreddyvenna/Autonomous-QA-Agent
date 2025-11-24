# backend/services/document_ingestion/chunker.py
import uuid
import re

def _split_into_sentences(text: str):
    """
    Split into sentences using regex — much better than naive word splitting.
    """
    # Normalize whitespace
    text = re.sub(r"\s+", " ", text).strip()

    # Basic sentence split (LLM-friendly, simple & effective)
    sentences = re.split(r'(?<=[.!?])\s+', text)
    return [s.strip() for s in sentences if s.strip()]


def chunk_text(text: str, source: str = "unknown", chunk_size: int = 600, overlap: int = 150):
    """
    Semantic-aware chunker.
    - Break text into sentences
    - Merge sentences until reaching chunk_size (approx sentences length)
    - Add overlapping last N sentences to next chunk
    - Maintain metadata: id, text, source
    """
    sentences = _split_into_sentences(text)
    if not sentences:
        return []

    chunks = []
    current_chunk = []
    current_len = 0

    for sentence in sentences:
        words = sentence.split()
        sentence_len = len(words)

        # If adding this sentence exceeds chunk size → finalize chunk
        if current_len + sentence_len > chunk_size:
            # Finalize this chunk
            chunk_text = " ".join(current_chunk).strip()
            chunks.append({
                "id": str(uuid.uuid4()),
                "text": chunk_text,
                "source": source
            })

            # Start new chunk with overlap
            overlap_sentences = current_chunk[-(overlap // 10):]  # dynamic overlap
            current_chunk = overlap_sentences + [sentence]
            current_len = sum(len(s.split()) for s in current_chunk)
        else:
            current_chunk.append(sentence)
            current_len += sentence_len

    # Add final chunk
    if current_chunk:
        chunk_text = " ".join(current_chunk).strip()
        chunks.append({
            "id": str(uuid.uuid4()),
            "text": chunk_text,
            "source": source
        })

    return chunks

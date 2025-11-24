# backend/services/document_ingestion/pdf_parser.py
import fitz  # PyMuPDF

def parse_pdf_bytes(data: bytes) -> str:
    """
    Enhanced PDF text extraction.
    - Extracts page text
    - Extracts headings / layout blocks
    - Extracts tables (as best-effort)
    - Extracts metadata
    - Cleans whitespace
    Returns rich text suitable for chunking & vector search.
    """
    try:
        doc = fitz.open(stream=data, filetype="pdf")
    except Exception as e:
        print(f"PDF parse error: {e}")
        return ""

    output_parts = []

    # -------------------------
    # 1. Extract metadata
    # -------------------------
    try:
        metadata = doc.metadata or {}
        meta_lines = [f"{k}: {v}" for k, v in metadata.items() if v]
        if meta_lines:
            output_parts.append("=== PDF METADATA ===")
            output_parts.append("\n".join(meta_lines))
            output_parts.append("\n")
    except:
        pass

    # -------------------------
    # 2. Extract text page by page
    # -------------------------
    for page_num, page in enumerate(doc, start=1):
        output_parts.append(f"=== PAGE {page_num} ===")

        try:
            page_text = page.get_text("text")
            if page_text.strip():
                output_parts.append(page_text)
        except:
            pass

        # -------------------------
        # 3. Extract structured blocks (improved embeddings)
        # -------------------------
        try:
            blocks = page.get_text("blocks")
            if blocks:
                output_parts.append("\n=== TEXT BLOCKS ===")
                for block in blocks:
                    text = block[4].strip()
                    if text:
                        output_parts.append(text)
        except:
            pass

        # -------------------------
        # 4. Attempt table extraction
        # -------------------------
        try:
            tables = page.find_tables()
            if tables:
                output_parts.append("\n=== TABLES FOUND ===")
                for t in tables:
                    try:
                        output_parts.append(str(t.to_pandas()))
                    except:
                        output_parts.append("[Table extracted but formatting failed]")
        except:
            pass

        output_parts.append("\n")

    # Join everything
    final_text = "\n".join(part for part in output_parts if part.strip())

    # Clean whitespace
    cleaned = "\n".join(
        [line.strip() for line in final_text.split("\n") if line.strip()]
    )

    return cleaned

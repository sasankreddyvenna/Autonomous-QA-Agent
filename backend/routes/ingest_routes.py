# backend/routes/ingest_routes.py
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import List
import os, uuid, json

from backend.services.document_ingestion.dom_parser import parse_dom_structure
from backend.services.document_ingestion.pdf_parser import parse_pdf_bytes
from backend.services.document_ingestion.html_parser import parse_html_bytes
from backend.services.document_ingestion.text_parser import parse_text_bytes
from backend.services.document_ingestion.json_parser import parse_json_bytes
from backend.services.document_ingestion.chunker import chunk_text
from backend.services.embeddings.embedder import embed_chunks
from backend.services.knowledge_base.chroma_client import ChromaVectorDB

router = APIRouter(prefix="", tags=["Ingestion"])
db = ChromaVectorDB()

BASE_DIR = os.path.dirname(os.path.dirname(__file__))  # backend/
UPLOAD_DIR = os.path.join(BASE_DIR, "storage", "uploads")
PROCESSED_DIR = os.path.join(BASE_DIR, "storage", "processed")
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

@router.post("/upload")
async def upload_files(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files uploaded.")

    all_chunks = []
    stored_files = []

    for file in files:
        try:
            contents = await file.read()
            filename = file.filename or f"file_{uuid.uuid4().hex}"
            lower = filename.lower()

            save_path = os.path.join(UPLOAD_DIR, filename)
            with open(save_path, "wb") as f:
                f.write(contents)
            stored_files.append(save_path)

            # parse by type
            if lower.endswith(".pdf"):
                text = parse_pdf_bytes(contents)
                dom_text = ""
            elif lower.endswith(".html") or lower.endswith(".htm"):
                text = parse_html_bytes(contents)
                dom_text = parse_dom_structure(contents)
            elif lower.endswith(".txt") or lower.endswith(".md"):
                text = parse_text_bytes(contents)
                dom_text = ""
            elif lower.endswith(".json"):
                text = parse_json_bytes(contents)
                dom_text = ""
            else:
                try:
                    text = contents.decode("utf-8")
                except:
                    text = ""
                dom_text = ""

            if not text:
                continue

            combined = text
            if dom_text:
                combined = text + "\n\n" + dom_text

                # save a processed dom file for debugging
                dom_json_path = os.path.join(PROCESSED_DIR, f"{filename}_dom.txt")
                with open(dom_json_path, "w", encoding="utf-8") as fh:
                    fh.write(dom_text)

            # chunk and attach minimal metadata
            chunks = chunk_text(combined, source=filename)
            all_chunks.extend(chunks)

        except Exception as e:
            print(f"[ingest] error processing {file.filename}: {e}")
            continue

    if not all_chunks:
        raise HTTPException(status_code=400, detail="No parsable content found in uploaded files.")

    # create embeddings and add to DB
    embeddings = embed_chunks(all_chunks)
    db.add_documents(all_chunks, embeddings)

    return {"status": "Knowledge Base Built", "chunks_added": len(all_chunks), "files_stored": stored_files}

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.knowledge_base.chroma_client import ChromaVectorDB
from backend.services.groq_client.generator import generate_with_context

router = APIRouter(tags=["Testcase Generation"])
db = ChromaVectorDB()

class QueryRequest(BaseModel):
    query: str
    top_k: int = 8

@router.post("/generate")
async def generate_testcases(req: QueryRequest):
    if not (req.query or "").strip():
        raise HTTPException(status_code=400, detail="Query is required")

    # Retrieve relevant text from vector DB
    chroma_docs = db.query(req.query, n_results=req.top_k)

    # ✅ Safe extraction
    documents = (chroma_docs or {}).get("documents") or [[]]
    first_list = documents[0] if isinstance(documents, list) and documents else []
    context = "\n\n".join(first_list)

    docs_result = {"context": context}

    # Generate grounded test cases
    result = generate_with_context(
        query=req.query,
        docs_result=docs_result,
        prompt_filename="testcase_prompt.txt"
    )

    return {"testcases": result}

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.routes.ingest_routes import router as ingest_router
from backend.routes.testcase_routes import router as testcase_router
from backend.routes.script_routes import router as script_router

app = FastAPI(title="Autonomous QA Agent - Backend")

# Allow CORS for Streamlit UI or remote access
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Attach routers with prefixes
app.include_router(ingest_router, prefix="/ingest")        # /ingest/...
app.include_router(testcase_router, prefix="/testcases")  # /testcases/...
app.include_router(script_router, prefix="/script")        # /script/...

@app.get("/")
def root():
    return {"status": "ok", "service": "autonomous-qa-agent backend"}

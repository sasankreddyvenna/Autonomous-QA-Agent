# backend/routes/script_routes.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from backend.services.selenium.script_generator import SeleniumScriptGenerator

router = APIRouter(tags=["script"])

class ScriptRequest(BaseModel):
    test_id: str
    scenario: str | None = None
    steps: str | None = None
    expected_result: str | None = None

@router.post("/generate")
async def generate_script(payload: dict):
    test_id = payload.get("test_id", "")
    scenario = payload.get("scenario", "")
    steps = payload.get("steps", "")
    expected_result = payload.get("expected_result", "")

    if not steps:
        raise HTTPException(status_code=400, detail="Steps are required")

    script = SeleniumScriptGenerator.generate_script(test_id, scenario, steps, expected_result)

    return {"selenium_script": script}

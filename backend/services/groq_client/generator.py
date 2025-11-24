import os
from typing import Dict, Union, List
from groq import Groq

MODEL_NAME = "llama-3.3-70b-versatile"


PROMPTS_DIR = os.path.join(os.path.dirname(__file__), "prompts")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))


def _load_prompt(name: str) -> str:
    path = os.path.join(PROMPTS_DIR, name)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def _extract_context_text(docs_result: Union[Dict, str]) -> str:
    if isinstance(docs_result, dict) and "context" in docs_result:
        return docs_result["context"]

    if isinstance(docs_result, str):
        return docs_result

    if isinstance(docs_result, dict) and "documents" in docs_result:
        docs = docs_result["documents"]
        if isinstance(docs, list) and len(docs) > 0:
            flat_list: List[str] = []
            for block in docs:
                if isinstance(block, list):
                    flat_list.extend(txt for txt in block if isinstance(txt, str))
                elif isinstance(block, str):
                    flat_list.append(block)
            return "\n\n".join(flat_list)

    return ""


def generate_with_context(query: str, docs_result: Dict, prompt_filename: str) -> str:
    template = _load_prompt(prompt_filename)
    context = _extract_context_text(docs_result)

    final_prompt = (
        template.replace("{{query}}", query)
                .replace("{{context}}", context)
    )

    try:
        response = client.chat.completions.create(
            model=MODEL_NAME,
            messages=[
                {"role": "system", "content": "You are an expert QA analyst. Ground all outputs strictly in the provided context. Do NOT invent features."},
                {"role": "user", "content": final_prompt}
            ],
            temperature=0.0,
            max_tokens=1500
        )

        content = response.choices[0].message.content or ""
        return content.strip()

    except Exception as e:
        return f"[Groq Exception] {str(e)}"

# backend/services/document_ingestion/dom_parser.py
from bs4 import BeautifulSoup

def parse_dom_structure(html_bytes: bytes) -> str:
    try:
        soup = BeautifulSoup(html_bytes, "html.parser")
    except Exception:
        return ""

    lines = []
    lines.append("=== DOM STRUCTURE BEGIN ===")
    for element in soup.find_all(True):
        tag = element.name
        elem_id = element.get("id")
        elem_class = element.get("class")
        attrs = " ".join([f"{k}='{v}'" for k, v in element.attrs.items() if k not in ("id","class")])
        text = (element.get_text(strip=True) or "")[:120].replace("\n"," ")
        line = f"ELEMENT: <{tag}>"
        if elem_id:
            line += f" | id={elem_id}"
        if elem_class:
            line += f" | class={' '.join(elem_class)}"
        if attrs:
            line += f" | attrs={attrs}"
        if text:
            line += f" | text='{text}'"
        lines.append(line)
    lines.append("=== DOM STRUCTURE END ===")
    return "\n".join(lines)

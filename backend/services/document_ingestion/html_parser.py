from bs4 import BeautifulSoup
import json

def parse_html_bytes(data: bytes) -> str:
    """
    Extract BOTH visible text and DOM structure from HTML.
    Returns a long combined string that contains:
    - visible text
    - DOM element inventory (ids, classes, inputs, buttons, forms, labels, etc.)
    """

    try:
        soup = BeautifulSoup(data, "lxml")

        # Remove script/style/noscript
        for s in soup(["script", "style", "noscript"]):
            s.decompose()

        # -------------------------------
        # 1. Extract visible text
        # -------------------------------
        text = soup.get_text(separator="\n")
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        visible_text = "\n".join(lines)

        # -------------------------------
        # 2. Extract DOM STRUCTURE
        # -------------------------------
        dom_info = {
            "inputs": [],
            "buttons": [],
            "forms": [],
            "labels": [],
            "sections": [],
            "links": [],
            "radio_buttons": [],
            "divs": []
        }

        # INPUT FIELDS
        for inp in soup.find_all("input"):
            dom_info["inputs"].append({
                "id": inp.get("id"),
                "name": inp.get("name"),
                "type": inp.get("type"),
                "placeholder": inp.get("placeholder")
            })

        # BUTTONS
        for btn in soup.find_all(["button", "a"]):
            dom_info["buttons"].append({
                "id": btn.get("id"),
                "class": btn.get("class"),
                "text": btn.get_text(strip=True)
            })

        # FORMS
        for f in soup.find_all("form"):
            dom_info["forms"].append({
                "id": f.get("id"),
                "method": f.get("method"),
                "action": f.get("action")
            })

        # LABELS
        for lbl in soup.find_all("label"):
            dom_info["labels"].append({
                "for": lbl.get("for"),
                "text": lbl.get_text(strip=True)
            })

        # RADIO BUTTONS
        for r in soup.find_all("input", {"type": "radio"}):
            dom_info["radio_buttons"].append({
                "id": r.get("id"),
                "name": r.get("name"),
                "value": r.get("value")
            })

        # MAIN SECTIONS + DIVS
        for section in soup.find_all(["section", "div"]):
            dom_info["sections"].append({
                "id": section.get("id"),
                "class": section.get("class"),
                "text": section.get_text(strip=True)[:200]  # limit preview
            })

        # LINKS
        for a in soup.find_all("a"):
            dom_info["links"].append({
                "href": a.get("href"),
                "text": a.get_text(strip=True)
            })

        # serialized DOM info
        dom_json = json.dumps(dom_info, indent=2)

        # -------------------------------
        # FINAL RETURN = TEXT + DOM
        # -------------------------------
        full_payload = (
            "=== VISIBLE TEXT ===\n"
            + visible_text +
            "\n\n=== DOM STRUCTURE ===\n"
            + dom_json
        )

        return full_payload

    except Exception as e:
        print(f"HTML parse error: {e}")
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return ""

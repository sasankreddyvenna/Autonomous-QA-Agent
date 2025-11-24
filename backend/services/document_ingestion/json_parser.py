import json

def parse_json_bytes(data: bytes) -> str:
    """
    Parse JSON bytes into a stable text format for embeddings.
    Includes:
    - Pretty JSON (human-friendly)
    - Flattened key/value text list (AI-friendly)
    """
    try:
        obj = json.loads(data)

        # ------------------------------------------
        # 1. Pretty JSON (for readability)
        # ------------------------------------------
        pretty_json = json.dumps(obj, indent=2)

        # ------------------------------------------
        # 2. Flatten key-value pairs for better retrieval
        # ------------------------------------------
        flat_lines = []

        def flatten(prefix, value):
            """Recursively flatten dictionaries and arrays."""
            if isinstance(value, dict):
                for k, v in value.items():
                    flatten(f"{prefix}.{k}" if prefix else k, v)
            elif isinstance(value, list):
                for i, v in enumerate(value):
                    flatten(f"{prefix}[{i}]", v)
            else:
                flat_lines.append(f"{prefix}: {value}")

        flatten("", obj)

        flattened_text = "\n".join(flat_lines)

        # ------------------------------------------
        # 3. Final combined payload
        # ------------------------------------------
        final_text = (
            "=== RAW JSON ===\n"
            + pretty_json +
            "\n\n=== FLATTENED VALUES ===\n"
            + flattened_text
        )

        return final_text

    except Exception as e:
        print(f"JSON parse error: {e}")
        try:
            return data.decode("utf-8", errors="ignore")
        except Exception:
            return ""

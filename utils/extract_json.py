import json
import re

def extract_json(text: str):
    """
    Attempt to extract the first JSON block from LLM output.
    """
    try:
        # Try direct JSON parse
        return json.loads(text)
    except json.JSONDecodeError:
        pass

    # Try extracting JSON block manually
    match = re.search(r'\[.*\]', text, re.DOTALL)
    if match:
        json_str = match.group(0)
        try:
            return json.loads(json_str)
        except json.JSONDecodeError as e:
            print("❌ Even after extraction, invalid JSON.")
            print(json_str)
            raise e
    else:
        raise ValueError("No JSON block found — looks like general natural language.")
# ------------------------------------------------------
# 4. llm_gateway.py (still uses Ollama for local inference)
# ------------------------------------------------------
import subprocess

def query_llm(prompt):
    process = subprocess.Popen(
        ["ollama", "run", "llama3"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,  # ensures encoding/decoding is done properly
        encoding='utf-8',  # force utf-8 to handle special characters
    )
    try:
        output, _ = process.communicate(input=prompt, timeout=30)
        return output.strip()
    except subprocess.TimeoutExpired:
        process.kill()
        return "LLM timed out. Please try again."


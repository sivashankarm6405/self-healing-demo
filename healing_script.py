import requests
import os

OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL = "qwen2.5-coder:3b"

def read_error_log(path="build.log"):
    if not os.path.exists(path):
        return "No build.log found."
    with open(path, "r", errors="ignore") as f:
        content = f.read()
    return content[-4000:]  # keep it within a reasonable context size

def ask_llm_for_fix(error_log):
    prompt = (
        "You are a CI/CD auto-fix assistant. A Maven build failed. "
        "Given the following build log, identify the root cause and propose "
        "the exact code fix needed.\n\n"
        f"BUILD LOG:\n{error_log}\n\n"
        "Respond with: 1) Root cause (one line) 2) The corrected code snippet."
    )
    resp = requests.post(OLLAMA_URL, json={
        "model": MODEL,
        "prompt": prompt,
        "stream": False
    })
    resp.raise_for_status()
    return resp.json()["response"]

if __name__ == "__main__":
    print("=== Healing Script Started ===")
    log = read_error_log()
    print("=== Captured Build Log (last 4000 chars) ===")
    print(log)
    print("=== Asking Ollama for a fix ===")
    fix = ask_llm_for_fix(log)
    print("=== SUGGESTED FIX ===")
    print(fix)

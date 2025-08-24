import subprocess
from config import OLLAMA_PATH, MODEL_TIMEOUTS

def ask_ollama(model: str, query: str) -> str:
    timeout_sec = MODEL_TIMEOUTS.get(model, 120)
    try:
        result = subprocess.run(
            [OLLAMA_PATH, "run", model, query],
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout_sec
        )
        if result.returncode != 0:
            return f"[Error: {result.stderr.strip()}]"
        return result.stdout.strip() if result.stdout else "[No output]"
    except FileNotFoundError:
        return "[Error: Ollama executable not found]"
    except subprocess.TimeoutExpired:
        return f"[Error: Timeout after {timeout_sec}s]"
    except Exception as e:
        return f"[Error: Unexpected - {e}]"

from pathlib import Path
import os

# Paths
QUERIES_FILE = Path("C:/Users/aitoo/OneDrive/Desktop/Pak-Law/PakLawAI/data/queries_all.txt")
OUTPUT_JSON = Path("C:/Users/aitoo/OneDrive/Desktop/Pak-Law/PakLawAI/data/queries_all.txt/result.json")
OLLAMA_PATH = os.path.expanduser(r"~/AppData/Local/Programs/Ollama/ollama.exe")

# Models
OLLAMA_MODELS = [
    "llama3.1", "mistral", "gpt-oss",
    "smollm2:1.7b", "command-r7b", "granite3.3"
]

# Timeouts
MODEL_TIMEOUTS = {
    "llama3.1": 290,
    "mistral": 290,
    "gpt-oss": 480,
    "smollm2:1.7b": 290,
    "command-r7b": 290,
    "granite3.3": 290,
}

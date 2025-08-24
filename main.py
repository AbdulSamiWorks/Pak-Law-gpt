import json
from pathlib import Path
from tqdm import tqdm
from config import QUERIES_FILE, OUTPUT_JSON, OLLAMA_MODELS
from utils import ask_ollama
from metrics import bleu_score, semantic_score, jurisdiction_accuracy, length_penalty, composite_score
from rag.rag_query import ask_rag

def main():
    queries = Path(QUERIES_FILE).read_text(encoding="utf-8").splitlines()

    if Path(OUTPUT_JSON).exists():
        with open(OUTPUT_JSON, "r", encoding="utf-8") as f:
            results = json.load(f)
        processed_queries = {row["Query"] for row in results}
    else:
        results, processed_queries = [], set()

    for i, query in enumerate(tqdm(queries, desc="Processing queries"), start=1):
        if query in processed_queries:
            continue

        row = {"No": len(results) + 1, "Query": query}

        # PakLawAI
        paklawAI_answer = ask_rag(query)
        row["PakLawAI_Answer"] = paklawAI_answer
        ref = paklawAI_answer
        row["PakLawAI_BLEU"] = bleu_score(paklawAI_answer, ref)
        row["PakLawAI_Semantic"] = semantic_score(paklawAI_answer, ref)
        row["PakLawAI_Jurisdiction"] = jurisdiction_accuracy(paklawAI_answer)
        row["PakLawAI_LengthPenalty"] = length_penalty(paklawAI_answer, ref)
        row["PakLawAI_Composite"] = composite_score(
            row["PakLawAI_BLEU"], row["PakLawAI_Semantic"], row["PakLawAI_Jurisdiction"]
        ) * row["PakLawAI_LengthPenalty"]

        # Ollama models
        for model in OLLAMA_MODELS:
            answer = ask_ollama(model, query)
            row[f"{model}_Answer"] = answer
            row[f"{model}_BLEU"] = bleu_score(answer, ref)
            row[f"{model}_Semantic"] = semantic_score(answer, ref)
            row[f"{model}_Jurisdiction"] = jurisdiction_accuracy(answer)
            row[f"{model}_LengthPenalty"] = length_penalty(answer, ref)
            row[f"{model}_Composite"] = composite_score(
                row[f"{model}_BLEU"], row[f"{model}_Semantic"], row[f"{model}_Jurisdiction"]
            ) * row[f"{model}_LengthPenalty"]

        results.append(row)
        with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
            json.dump(results, f, indent=2, ensure_ascii=False)

    print(f"✅ Results saved to JSON: {OUTPUT_JSON}")

if __name__ == "__main__":
    main()

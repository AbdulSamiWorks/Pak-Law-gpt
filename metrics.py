import numpy as np
from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def cosine_similarity(vec1, vec2):
    return float(np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2)))

def semantic_score(pred, ref):
    try:
        v1 = embedding_model.encode(pred)
        v2 = embedding_model.encode(ref)
        return cosine_similarity(v1, v2)
    except Exception:
        return 0.0

def bleu_score(pred, ref):
    smoothie = SmoothingFunction().method4
    try:
        return sentence_bleu([ref.split()], pred.split(), smoothing_function=smoothie)
    except ZeroDivisionError:
        return 0.0

def jurisdiction_accuracy(answer: str) -> int:
    keywords = [
        "Pakistan", "Pakistani", "CPC", "Civil Procedure Code",
        "Ordinance", "Act", "Section", "Rent Restriction Ordinance",
        "Land Revenue Act", "Law", "Code"
    ]
    return int(any(kw.lower() in answer.lower() for kw in keywords))

def length_penalty(answer: str, ref: str) -> float:
    if not answer or not ref:
        return 0.0
    ratio = len(answer.split()) / max(1, len(ref.split()))
    return min(1.0, ratio)

def composite_score(bleu, semantic, jurisdiction, w_bleu=0.3, w_sem=0.4, w_jur=0.3):
    return (w_bleu * bleu) + (w_sem * semantic) + (w_jur * jurisdiction)

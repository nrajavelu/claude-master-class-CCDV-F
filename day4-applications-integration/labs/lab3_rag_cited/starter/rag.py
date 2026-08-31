"""
Day 4 · Lab 3 — tiny RAG with citations (STARTER). Fill every # TODO.

    cd aizentify-cdf-bootcamp
    python day4-applications-integration/labs/lab3_rag_cited/starter/rag.py "What is our refund window?"
"""
from __future__ import annotations

import math
import sys
from pathlib import Path

from dotenv import load_dotenv
import anthropic

load_dotenv()
CORPUS = Path(__file__).resolve().parent.parent / "corpus"
MODEL = "claude-haiku-4-5"

# TODO 5: write SYSTEM — answer ONLY from the provided <doc> blocks; cite the doc id(s) as
#   [id]; if the answer isn't present reply exactly "Not in the provided documents.";
#   keep it to one or two sentences.
SYSTEM = ""


def embed(texts: list[str]) -> list[list[float]]:
    # TODO 2: return an embedding vector per input text. Pick ONE:
    #   voyageai:  voyageai.Client().embed(texts, model="voyage-3", input_type="document").embeddings
    #   local:     SentenceTransformer("all-MiniLM-L6-v2").encode(texts, normalize_embeddings=True)  (-> .tolist())
    raise NotImplementedError("embed()")


def cos(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


DOCS = [(p.stem, p.read_text().strip()) for p in sorted(CORPUS.glob("*.md"))]
_VECS = None


def index():
    global _VECS
    if _VECS is None:
        # TODO 3: embed every doc's text ONCE
        _VECS = embed([t for _, t in DOCS])
    return _VECS


def retrieve(question: str, k: int = 3):
    # TODO 4: embed the question, cosine-similarity against index(), return the top-k (doc_id, text)
    raise NotImplementedError("retrieve()")


def answer(question: str) -> str:
    hits = retrieve(question)
    context = "\n\n".join(f'<doc id="{d}">\n{t}\n</doc>' for d, t in hits)
    client = anthropic.Anthropic()
    # TODO 6: one messages.create with SYSTEM + a user message containing `context` and the question
    r = None  # <-- replace
    return "".join(b.text for b in r.content if b.type == "text").strip()


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python rag.py "your question"')
        return 2
    q = " ".join(sys.argv[1:])
    print("retrieved:", [d for d, _ in retrieve(q)])
    print("Answer:", answer(q))
    return 0


if __name__ == "__main__":
    sys.exit(main())

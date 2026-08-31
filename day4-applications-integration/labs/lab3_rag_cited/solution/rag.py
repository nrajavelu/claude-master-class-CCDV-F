"""
Day 4 · Lab 3 — tiny RAG with citations (SOLUTION).

chunk -> embed -> cosine top-k -> grounded prompt (<doc id>) -> answer + cite.
Auto-detects the embedding path: voyageai (hosted) first, else sentence-transformers (local).

    cd aizentify-cdf-bootcamp
    python day4-applications-integration/labs/lab3_rag_cited/solution/rag.py "What is our refund window?"

Exports answer(question) -> str so evals/harness.py can grade it (Lab 4).
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

SYSTEM = (
    "Answer the question USING ONLY the provided <doc> blocks. "
    "Cite the doc id(s) you used in square brackets, e.g. [refunds]. "
    "If the answer is not in the provided documents, reply exactly: "
    "'Not in the provided documents.' Keep the answer to one or two sentences."
)

# --- embedding backend -----------------------------------------------------
_backend = None


def _embed_backend():
    global _backend
    if _backend:
        return _backend
    try:
        import voyageai  # type: ignore
        vc = voyageai.Client()
        _backend = ("voyage", lambda texts: vc.embed(texts, model="voyage-3", input_type="document").embeddings)
        return _backend
    except Exception:
        pass
    try:
        from sentence_transformers import SentenceTransformer  # type: ignore
        st = SentenceTransformer("all-MiniLM-L6-v2")
        _backend = ("local", lambda texts: [v.tolist() for v in st.encode(texts, normalize_embeddings=True)])
        return _backend
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            "No embedding library found. `pip install voyageai` (needs VOYAGE_API_KEY) "
            f"or `pip install sentence-transformers`. ({e})"
        )


def embed(texts: list[str]) -> list[list[float]]:
    return _embed_backend()[1](texts)


def _cos(a: list[float], b: list[float]) -> float:
    dot = sum(x * y for x, y in zip(a, b))
    na = math.sqrt(sum(x * x for x in a)) or 1.0
    nb = math.sqrt(sum(y * y for y in b)) or 1.0
    return dot / (na * nb)


# --- index (built once at import) ---------------------------------------
_DOCS = [(p.stem, p.read_text().strip()) for p in sorted(CORPUS.glob("*.md"))]
_VECS: list[list[float]] | None = None


def _index() -> list[list[float]]:
    global _VECS
    if _VECS is None:
        _VECS = embed([t for _, t in _DOCS])
    return _VECS


def retrieve(question: str, k: int = 3) -> list[tuple[str, str]]:
    qv = embed([question])[0]
    scored = sorted(zip(_DOCS, _index()), key=lambda z: _cos(qv, z[1]), reverse=True)
    return [doc for doc, _ in scored[:k]]


def answer(question: str) -> str:
    hits = retrieve(question)
    context = "\n\n".join(f'<doc id="{did}">\n{text}\n</doc>' for did, text in hits)
    client = anthropic.Anthropic()
    r = client.messages.create(
        model=MODEL, max_tokens=200, system=SYSTEM,
        messages=[{"role": "user", "content": f"{context}\n\nQuestion: {question}"}],
    )
    return "".join(b.text for b in r.content if b.type == "text").strip()


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python rag.py "your question"')
        return 2
    q = " ".join(sys.argv[1:])
    hits = retrieve(q)
    print("backend :", _embed_backend()[0])
    print("retrieved:", [did for did, _ in hits])
    print("Answer:", answer(q))
    return 0


if __name__ == "__main__":
    sys.exit(main())

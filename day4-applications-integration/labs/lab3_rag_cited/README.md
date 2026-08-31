# Lab 3 · Tiny RAG with citations

**Domain:** D2 · D6 (RAG) · **Time:** 50 min
**Practise:** chunking · embeddings (hosted **or** local) · cosine similarity · a grounded
prompt (`<doc id>` tags) · answering **only from the retrieved context** · **citing doc
ids** · saying "not in the provided documents" when it isn't.

---

## Goal

Answer questions about a 15-document corpus (`corpus/`), grounded and cited. One question
whose answer isn't in the corpus must return *"not in the provided documents"*.

```
cd aizentify-cdf-bootcamp

# pick ONE embedding path (see logistics/01-procurement-guide.md):
# A) hosted — needs a free VOYAGE_API_KEY in .env
pip install voyageai
# B) local  — no key, ~90 MB model download on first run
pip install sentence-transformers

python day4-applications-integration/labs/lab3_rag_cited/starter/rag.py "What is our refund window?"
python day4-applications-integration/labs/lab3_rag_cited/starter/rag.py "Do we ship to Antarctica?"   # not in corpus
```

The code auto-detects which path is installed (`voyageai` first, else
`sentence-transformers`).

---

## Steps

1. **Chunk** — `corpus/*.md` are already short (~1 paragraph each); treat one file = one
   chunk. (For real docs you'd split ~500 tokens with overlap.)
2. **Embed** — fill `embed(texts) -> list[list[float]]` for whichever library is present.
3. **Index** — embed every chunk once; keep `(doc_id, text, vector)`.
4. **Retrieve** — embed the question; cosine-similarity top-k (k=3); return the chunks.
5. **Ground** — build the prompt: a `system` that says *answer ONLY from the provided
   documents; cite the doc id(s) you used as `[id]`; if the answer isn't present, say "not
   in the provided documents"*; a `user` message with the k chunks wrapped as
   `<doc id="...">…</doc>`.
6. **Answer** — one `messages.create`; print the answer.

---

## Expected output (shape)

```
$ ... "What is our refund window?"
retrieved: [refunds, returns, shipping]
Answer: The refund window is 30 days from delivery. [refunds]

$ ... "Do we ship to Antarctica?"
retrieved: [shipping, international, returns]
Answer: Not in the provided documents.
```

## Checkpoints

- [ ] The answer **cites** at least one doc id for an in-corpus question.
- [ ] The out-of-corpus question returns "not in the provided documents" — it does **not**
      answer from the model's own knowledge.
- [ ] `embed()` is called **once per chunk at index time**, not per query.
- [ ] They can say when RAG beats long-context / fine-tuning (knowledge large / changing /
      must be cited).

## Common mistakes

| Symptom | Cause |
|---|---|
| model answers the Antarctica question anyway | grounding instruction too weak — make "if not present, say so" explicit and first |
| `ModuleNotFoundError` | neither embedding lib installed — `pip install` one (see above) |
| every retrieval returns the same 3 docs | you embedded the question with a different model than the chunks, or forgot to normalise |

## Going further (feeds Lab 4)

- Export `answer(question: str) -> str` so `evals/harness.py` can grade it.
- Add `citations: {enabled: true}` on the document blocks and read the structured `citations`
  array instead of parsing `[id]` out of the text.

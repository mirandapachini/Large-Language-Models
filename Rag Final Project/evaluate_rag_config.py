"""
RAG Configuration Sweep for the NP Tutor App
=====================================================

Purpose
-------
Runs your five verified questions against every combination of:
  - chunk_size:  100, 180, 240 words
  - overlap:     ~10% and ~20% of chunk_size
  - top_k:       3, 5, 7

...and scores retrieval relevance so you can compare configurations
side-by-side, without manually re-uploading documents 18 times in the UI.

HOW TO USE
----------
1. Copy this file into your MSBA_Statistics_Tutor_Student_Package folder
   (same folder as app.py, so it can import your rag_utils module).
2. Create a subfolder, e.g. "eval_docs", and put your 2-3 documents from
   a DIFFERENT course into it.
3. Fill in QUESTIONS below with your 5 questions and the answer keywords
   you expect to see in a *correctly retrieved* chunk (not the final
   generated answer -- we are scoring RETRIEVAL, not generation).
4. Make sure Ollama is running (same as when you launch the Streamlit app).
5. From Anaconda Prompt (with the stattutor environment activated), run:

       python evaluate_rag_config.py

6. Read the printed table and the saved eval_results.csv.

WHAT "RELEVANCE" MEANS HERE
----------------------------
For each question, you supply one or more keywords/phrases that MUST
appear in a chunk for that chunk to count as relevant (this is the
"answer you can verify manually" requirement from the assignment).
For each configuration, we check the top-k retrieved chunks and record:
  - hit_at_k        : was at least one relevant chunk retrieved? (1/0)
  - relevant_rank    : rank position of the first relevant chunk (or None)
  - avg_score_top_k  : average cosine similarity across the k results
This gives you a defensible, reproducible relevance score per configuration
instead of eyeballing it.
"""

from __future__ import annotations

import itertools
import time
from pathlib import Path

import pandas as pd

# Import directly from the module you were given.
# Adjust this import if your file is named differently (e.g. rag_utils).
# Importing DEFAULT_EMBEDDING_MODEL (instead of hardcoding a string here)
# guarantees this script always uses the exact same model name/tag as the
# real Streamlit app -- avoids "model not found" / "doesn't support
# embeddings" errors caused by a mismatched tag like all-minilm:latest
# vs all-minilm:l6-v2.
from rag_engine import build_knowledge_base, check_ollama, DEFAULT_EMBEDDING_MODEL

# ---------------------------------------------------------------------------
# 1. CONFIGURE THIS SECTION
# ---------------------------------------------------------------------------

DOCS_DIR = Path("docs")  # folder with your 2-3 documents from another course
OLLAMA_URL = "http://localhost:11434"
EMBEDDING_MODEL = DEFAULT_EMBEDDING_MODEL  # pulled straight from rag_utils.py

CHUNK_SIZES = [100, 180, 240]
OVERLAP_FRACTIONS = [0.10, 0.20]   # ~10% and ~20% of chunk_size
TOP_K_VALUES = [3, 5, 7]

# Fill in your 5 verified questions.
# `keywords` = short strings that MUST appear (case-insensitive) in a
# retrieved chunk for it to count as relevant. Use terms specific enough
# that they wouldn't appear by coincidence in an unrelated chunk.
QUESTIONS = [
    {
        "question": "How many PTO days do new hires get in their first year?",
        "keywords": ["PTO", "first", "year"],
    },
    {
        "question": "What is the deadline to enroll in benefits after starting?",
        "keywords": ["deadline", "enroll", "benefits", "after"],
    },
    {
        "question": "What password requirements do I need to set on Day 1?",
        "keywords": ["password", "requirements", "Day"],
    },
    {
        "question": "Does the company match 401(k) contributions?",
        "keywords": ["match", "401(k)"],
    },
    {
        "question": "Who do I contact if I have a workplace conflict?",
        "keywords": ["contact", "conflict"],
    },
]


# ---------------------------------------------------------------------------
# 2. EVALUATION LOGIC (no need to edit below this line)
# ---------------------------------------------------------------------------


def chunk_is_relevant(chunk_text: str, keywords: list[str]) -> bool:
    text_lower = chunk_text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


def evaluate_configuration(chunk_size: int, overlap: int, top_k: int) -> list[dict]:
    """Build a knowledge base for one (chunk_size, overlap) pair and run all
    questions at the given top_k. Returns one result row per question."""

    kb, errors = build_knowledge_base(
        docs_dir=DOCS_DIR,
        embedding_model_name=EMBEDDING_MODEL,
        ollama_url=OLLAMA_URL,
        chunk_size=chunk_size,
        overlap=overlap,
    )
    if errors:
        print(f"  [warning] file read errors: {errors}")

    rows = []
    for q in QUESTIONS:
        results = kb.search(q["question"], k=top_k)

        relevant_rank = None
        for rank, r in enumerate(results, start=1):
            if chunk_is_relevant(r.chunk.text, q["keywords"]):
                relevant_rank = rank
                break

        avg_score = sum(r.score for r in results) / len(results) if results else 0.0

        rows.append(
            {
                "chunk_size": chunk_size,
                "overlap": overlap,
                "overlap_pct": round(overlap / chunk_size, 2),
                "top_k": top_k,
                "question": q["question"][:60],
                "hit_at_k": int(relevant_rank is not None),
                "relevant_rank": relevant_rank,
                "avg_score_top_k": round(avg_score, 4),
                "num_chunks_total": len(kb.chunks),
                "backend": kb.backend_name,
            }
        )
    return rows


def main() -> None:
    ok, models, message = check_ollama(OLLAMA_URL)
    print(message)
    if not ok:
        print("Start Ollama before running this script.")
        return
    print(f"Installed models: {models}")

    if any(q["question"].startswith("REPLACE") for q in QUESTIONS):
        print(
            "\n[!] You still have placeholder QUESTIONS. "
            "Edit the QUESTIONS list at the top of this file before running.\n"
        )
        return

    all_rows: list[dict] = []
    combos = list(itertools.product(CHUNK_SIZES, OVERLAP_FRACTIONS, TOP_K_VALUES))
    print(f"Running {len(combos)} configurations x {len(QUESTIONS)} questions...\n")

    # Cache knowledge bases per (chunk_size, overlap) so we don't re-embed
    # the same chunks 3 times just because top_k changes.
    kb_cache: dict[tuple[int, int], list[dict]] = {}

    for chunk_size, overlap_frac, top_k in combos:
        overlap = max(1, round(chunk_size * overlap_frac))
        cache_key = (chunk_size, overlap)

        print(f"chunk_size={chunk_size:>3}  overlap={overlap:>3} ({overlap_frac:.0%})  top_k={top_k}")
        start = time.time()

        if cache_key not in kb_cache:
            # We still need per-top_k rows, so evaluate_configuration is called
            # per combo, but build_knowledge_base cost is the expensive part.
            pass

        rows = evaluate_configuration(chunk_size, overlap, top_k)
        all_rows.extend(rows)
        print(f"  done in {time.time() - start:.1f}s\n")

    df = pd.DataFrame(all_rows)
    df.to_csv("eval_results.csv", index=False)

    print("\n=== Summary: Hit Rate & Avg Similarity by Configuration ===\n")
    summary = (
        df.groupby(["chunk_size", "overlap_pct", "top_k"])
        .agg(
            hit_rate=("hit_at_k", "mean"),
            avg_relevant_rank=("relevant_rank", "mean"),
            avg_score_top_k=("avg_score_top_k", "mean"),
        )
        .reset_index()
        .sort_values("hit_rate", ascending=False)
    )
    print(summary.to_string(index=False))
    print("\nFull per-question results saved to eval_results.csv")
    print("Best configuration(s) by hit_rate are listed at the top of the summary above.")


if __name__ == "__main__":
    main()
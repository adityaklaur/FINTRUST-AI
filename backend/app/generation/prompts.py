"""Prompts + context building + the offline extractive answerer.

Design choice vs. the plan: the LLM is asked ONLY for the prose answer (+ a
low-confidence flag). The evidence checklist and escalation route come from the
deterministic classifier maps, not from parsing LLM text — safety-critical
guidance must not depend on the model formatting its output correctly.
"""

from __future__ import annotations

import re

from app.schemas.retrieval import RetrievedChunk

SYSTEM_PROMPT = """You are FinTrust AI, a source-grounded financial-services assistant.
Your ONLY job is to help users understand banking, payment, and financial-services
grievance processes based strictly on the document excerpts provided.

STRICT RULES:
1. Answer ONLY from the provided excerpts. If they lack the information, say so
   plainly. Never use outside or training knowledge.
2. Never say "you are entitled to" or "you will receive". Say "the source states"
   or "according to [Source N]".
3. Cite every factual claim inline with [Source N].
4. Do NOT give legal, tax, credit, investment, or claim-approval decisions. If asked,
   decline politely and explain you can only summarise sources and suggest next steps.
5. Be calm, precise, and concise. Do not speculate.
"""

ANSWER_PROMPT_TEMPLATE = """User question: {question}

Document excerpts (each labelled [Source N]):
{context_block}

Write a helpful, cautious answer using ONLY the excerpts above.
- Cite claims inline as [Source N].
- 2-5 short paragraphs or bullet points. No preamble, no restating the question.
- Do not invent facts, numbers, or timelines that are not in the excerpts.
Then, on its own final line, output exactly:
LOW_CONFIDENCE: yes|no
(yes if the excerpts only partially answer the question)
"""


def build_context(chunks: list[RetrievedChunk], max_chunks: int = 6, max_chars: int = 1200) -> str:
    blocks = []
    for i, c in enumerate(chunks[:max_chunks], start=1):
        section = c.section_title or "General"
        head = f"[Source {i}] {c.title} | Authority: {c.authority} | Section: {section}"
        blocks.append(f"{head}\n{c.text[:max_chars]}")
    return "\n\n".join(blocks)


def _first_sentences(text: str, n: int = 2, cap: int = 320) -> str:
    sents = re.split(r"(?<=[.!?])\s+", text.strip())
    out = " ".join(sents[:n]).strip()
    return (out[: cap - 1] + "…") if len(out) > cap else out


def extractive_answer(question: str, chunks: list[RetrievedChunk], max_points: int = 4) -> str:
    """No-LLM answer: condensed, cited excerpts. Honest and source-grounded."""
    lines = [
        "Here is what the most relevant official sources say "
        "(this summary is assembled directly from the source text, without an LLM):",
        "",
    ]
    for i, c in enumerate(chunks[:max_points], start=1):
        lines.append(f"- According to [Source {i}] ({c.title}, {c.authority}): {_first_sentences(c.text)}")
    lines += [
        "",
        "Review the cited source text below and follow the suggested escalation route for next steps.",
    ]
    return "\n".join(lines)

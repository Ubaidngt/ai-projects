"""Core RAG logic: document parsing, chunking, embeddings, retrieval, answer generation."""

import os
import re

import numpy as np
import requests

_model = None


def get_model(name="all-MiniLM-L6-v2"):
    """Lazy-load the sentence embedding model (downloads on first run)."""
    global _model
    if _model is None:
        from sentence_transformers import SentenceTransformer

        _model = SentenceTransformer(name)
    return _model


def extract_text(path):
    """Extract raw text from a PDF or TXT file."""
    if path.lower().endswith(".pdf"):
        from pypdf import PdfReader

        reader = PdfReader(path)
        return "\n".join((page.extract_text() or "") for page in reader.pages)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()


def chunk_text(text, chunk_size=600, overlap=80):
    """Split text into overlapping chunks for retrieval."""
    text = re.sub(r"\s+", " ", text).strip()
    chunks = []
    start = 0
    while start < len(text):
        chunk = text[start : start + chunk_size].strip()
        if chunk:
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks


def embed_texts(texts, model_name="all-MiniLM-L6-v2"):
    """Embed texts and L2-normalize so cosine similarity = dot product."""
    model = get_model(model_name)
    embs = model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
    norms = np.linalg.norm(embs, axis=1, keepdims=True) + 1e-10
    return embs / norms


def retrieve(query, chunks, embeddings, k=4, model_name="all-MiniLM-L6-v2"):
    """Return the top-k most relevant chunks for the query."""
    q = embed_texts([query], model_name)[0]
    sims = embeddings @ q
    idx = np.argsort(sims)[::-1][:k]
    return [(chunks[i], float(sims[i])) for i in idx]


PROMPT = """Answer the question using ONLY the context below. If the answer is not in the context, say you don't know.

Context:
{context}

Question: {question}
Answer:"""


def generate_answer(query, context_chunks, provider="groq", api_key=None):
    """Generate an answer with an LLM grounded on retrieved chunks.

    Returns (answer_text, model_label).
    """
    context = "\n\n".join(
        f"[Excerpt {i + 1}]\n{c}" for i, (c, _) in enumerate(context_chunks)
    )
    prompt = PROMPT.format(context=context, question=query)
    if provider == "groq":
        return _call_groq(prompt, api_key)
    if provider == "gemini":
        return _call_gemini(prompt, api_key), "Gemini · gemini-2.0-flash"
    raise ValueError(f"Unknown provider: {provider}")


def _call_groq(prompt, api_key):
    url = "https://api.groq.com/openai/v1/chat/completions"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    model = os.getenv("LLM_MODEL", "llama-3.3-70b-versatile")

    def _post(m):
        payload = {
            "model": m,
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.2,
            "max_tokens": 500,
        }
        return requests.post(url, headers=headers, json=payload, timeout=60)

    r = _post(model)
    used = model
    if r.status_code == 404:
        # model retired by Groq — auto-pick a live one
        live = _groq_live_model(headers)
        if live and live != model:
            r = _post(live)
            used = live
    r.raise_for_status()
    content = r.json()["choices"][0]["message"]["content"]
    if not content or not str(content).strip():
        raise RuntimeError(f"model '{used}' returned an empty answer")
    return str(content).strip(), f"Groq · {used}"


def _groq_live_model(headers):
    """Pick a currently-available Groq chat model."""
    try:
        r = requests.get(
            "https://api.groq.com/openai/v1/models", headers=headers, timeout=30
        )
        r.raise_for_status()
        ids = [m["id"] for m in r.json().get("data", [])]
    except Exception:
        return None
    for pref in ("llama-3.3-70b", "llama-3.1-8b", "llama", "qwen", "gpt-oss", "gemma"):
        for i in ids:
            if pref in i.lower():
                return i
    return ids[0] if ids else None


def _call_gemini(prompt, api_key):
    url = (
        "https://generativelanguage.googleapis.com/v1beta/models/"
        f"gemini-2.0-flash:generateContent?key={api_key}"
    )
    payload = {
        "contents": [{"parts": [{"text": prompt}]}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 500},
    }
    r = requests.post(url, json=payload, timeout=60)
    r.raise_for_status()
    return r.json()["candidates"][0]["content"]["parts"][0]["text"].strip()


def extractive_answer(query, context_chunks, demo=True):
    """No-API-key (or AI-failure) fallback: show the most relevant excerpts directly."""
    if demo:
        header = (
            "**Demo mode (no API key):** most relevant excerpts from your document — "
            "add a free API key and the AI will write a proper answer from these.\n"
        )
    else:
        header = (
            "**Fallback (AI answer unavailable):** most relevant excerpts from your document.\n"
        )
    lines = [header]
    for i, (c, s) in enumerate(context_chunks):
        lines.append(f"**Excerpt {i + 1}** (relevance {s:.2f}):\n{c}\n")
    return "\n".join(lines)

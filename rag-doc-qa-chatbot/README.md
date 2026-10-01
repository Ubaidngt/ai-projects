---
title: RAG Document Q&A Chatbot
emoji: 📄
colorFrom: indigo
colorTo: blue
sdk: gradio
app_file: app.py
pinned: false
license: mit
---

# 📄 RAG Document Q&A Chatbot

Upload any PDF or text document, ask questions about it, and get answers grounded
**only** on your document — powered by Retrieval-Augmented Generation (RAG).

## How it works

1. **Parse** — text is extracted from your PDF/TXT
2. **Chunk** — text is split into overlapping chunks (~600 chars)
3. **Embed** — each chunk is turned into a vector with `all-MiniLM-L6-v2`
4. **Retrieve** — your question is embedded too; top-4 chunks are found by cosine similarity
5. **Generate** — an LLM (Groq / Gemini) writes the final answer using only those chunks

## Tech stack

Python · Gradio · sentence-transformers · NumPy · PyPDF · Groq / Gemini API

## Run it

```bash
pip install -r requirements.txt
python app.py
```

Then open the local URL (usually http://127.0.0.1:7860), upload a document,
click **Index document**, and ask away.

> First run downloads the embedding model (~80 MB) — one time only.

## Full AI answers (free API key)

Without a key the app runs in **demo mode** and shows the most relevant excerpts.
For proper generated answers, add a free key:

```bash
# copy the example and fill in your key
cp .env.example .env   # then edit LLM_API_KEY
```

Or set environment variables directly:

```bash
export LLM_PROVIDER=groq
export LLM_API_KEY=your_key_here
python app.py
```

- Groq free key: https://console.groq.com
- Gemini free key: https://aistudio.google.com (set `LLM_PROVIDER=gemini`)

## Try it

1. Upload `sample_doc.txt` and ask *"What is RAG?"*
2. Upload your own CV and ask *"What are my top skills?"*

## LinkedIn tips

- Push this to GitHub and link it in your profile's **Projects** section
- Record a 30-second screen demo and add it to **Featured** — demo videos get the most views
- Write one post: what RAG is and what you learned building it

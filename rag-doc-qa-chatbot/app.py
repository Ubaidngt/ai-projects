"""RAG Document Q&A Chatbot — Gradio web app.

Upload a PDF/TXT, it gets chunked + embedded, then ask questions.
Answers are grounded ONLY on your document (retrieval-augmented generation).
"""

import os

from dotenv import load_dotenv

import gradio as gr
import spaces

from rag import (
    chunk_text,
    embed_texts,
    extract_text,
    extractive_answer,
    generate_answer,
    retrieve,
)

load_dotenv()  # load LLM_API_KEY etc. from a .env file if present

PROVIDER = os.getenv("LLM_PROVIDER", "groq").lower()
API_KEY = os.getenv("LLM_API_KEY", "").strip()


@spaces.GPU(duration=180)
def index_document(file):
    if file is None:
        return "Please upload a PDF or TXT file first.", None
    text = extract_text(file.name)
    if not text.strip():
        return "No text found in this file (scanned PDFs need OCR).", None
    chunks = chunk_text(text)
    embeddings = embed_texts(chunks)
    store = {"chunks": chunks, "embeddings": embeddings}
    return f"Indexed {len(chunks)} chunks. Now ask a question!", store


def answer_question(question, store):
    if not question or not question.strip():
        return "Type a question first.", ""
    if store is None:
        return "Upload and index a document first.", ""
    hits = retrieve(question, store["chunks"], store["embeddings"], k=4)
    if API_KEY:
        try:
            ans, label = generate_answer(question, hits, provider=PROVIDER, api_key=API_KEY)
            ans = f"{ans}\n\n*{label} — answer grounded only on your document*"
        except Exception as e:  # fall back to excerpts if the LLM call fails
            ans = (
                f"⚠️ AI jawab nahi ban saka ({e}).\n\n"
                "Neeche relevant excerpts dekh lo:\n\n"
                + extractive_answer(question, hits, demo=False)
            )
    else:
        ans = extractive_answer(question, hits, demo=True)
    sources = "\n\n".join(
        f"**Source {i + 1}:**\n{c[:300]}..." for i, (c, _) in enumerate(hits)
    )
    return ans, sources


with gr.Blocks(title="RAG Document Q&A Chatbot") as demo:
    key_status = (
        "🔑 API key loaded — full AI answers on"
        if API_KEY
        else "⚠️ No API key found — demo mode (excerpts only)"
    )
    gr.Markdown(
        "# 📄 RAG Document Q&A Chatbot\n"
        "Upload a document, then ask questions — answers come **only** from your document.\n\n"
        f"*{key_status}*"
    )
    with gr.Row():
        doc = gr.File(label="Upload PDF or TXT", file_types=[".pdf", ".txt"])
        index_btn = gr.Button("Index document")
    status = gr.Markdown()
    store = gr.State(None)

    question = gr.Textbox(
        label="Your question",
        placeholder="e.g. What are the key skills mentioned in the document?",
    )
    ask_btn = gr.Button("Ask", variant="primary")
    answer = gr.Markdown(label="Answer")
    sources = gr.Markdown(label="Retrieved sources")

    index_btn.click(index_document, inputs=doc, outputs=[status, store])
    ask_btn.click(answer_question, inputs=[question, store], outputs=[answer, sources])

if __name__ == "__main__":
    # ssr_mode=False: Hugging Face Spaces pe SSR (Node proxy) se startup
    # error aata hai, is liye classic mode use karo
    demo.launch(ssr_mode=False)

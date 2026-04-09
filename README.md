# RAG Q&A API 🤖

> An AI-powered Document Question & Answer API — upload any PDF and get instant AI answers using Retrieval Augmented Generation (RAG).

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green)
![LangChain](https://img.shields.io/badge/LangChain-latest-orange)
![Groq](https://img.shields.io/badge/Groq-LLaMA3.3-purple)
![License](https://img.shields.io/badge/License-MIT-yellow)

---

## What It Does

This API allows you to:
- Upload any PDF document via a REST endpoint
- Ask natural language questions about the document
- Get accurate, context-aware answers powered by LLaMA 3.3 running on Groq

It uses the **RAG (Retrieval Augmented Generation)** pattern — the gold standard for building reliable AI applications on top of private documents.

---

## Architecture

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  PDF Upload  │────▶│   LangChain  │────▶│   ChromaDB      │
│             │     │   Chunking   │     │  Vector Store   │
└─────────────┘     └──────────────┘     └─────────────────┘
                                                  │
                                                  ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│   Answer    │◀────│  Groq LLM    │◀────│ Semantic Search │
│            │     │  LLaMA 3.3   │     │  Top 3 Chunks   │
└─────────────┘     └──────────────┘     └─────────────────┘
```

**Flow:**
1. PDF is loaded and split into 500-token chunks with 50-token overlap
2. Each chunk is embedded using HuggingFace `all-MiniLM-L6-v2` (runs locally, free)
3. Embeddings are stored in ChromaDB (local vector database)
4. When a question is asked, it is embedded and compared against all chunks
5. Top 3 most relevant chunks are retrieved and sent to Groq LLM as context
6. LLaMA 3.3 generates a grounded answer using only the document context

---

## Tech Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| API Framework | FastAPI | REST endpoints, auto Swagger UI |
| Document Loading | LangChain | PDF parsing and text chunking |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) | Free local text embeddings |
| Vector Database | ChromaDB | Semantic similarity search |
| LLM | Groq — LLaMA 3.3 70B | Fast, free answer generation |
| Server | Uvicorn | ASGI server |

---

## Project Structure

```
rag-qa-api/
├── main.py           # FastAPI app — endpoints and routing
├── rag_engine.py     # RAG logic — embed, store, retrieve, answer
├── requirements.txt  # Python dependencies
├── .env              # API keys (not committed to git)
├── .gitignore        # Ignores .env, chroma_db, venv
└── README.md         # This file
```

---

## Getting Started

### Prerequisites
- Python 3.10+
- A free Groq API key from [console.groq.com](https://console.groq.com)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/YOUR_USERNAME/rag-qa-api.git
   cd rag-qa-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**

   Create a `.env` file in the root folder:
   ```
   GROQ_API_KEY=gsk_your_groq_api_key_here
   ```

5. **Run the server**
   ```bash
   uvicorn main:app --reload
   ```

6. **Open the interactive API docs**
   ```
   http://localhost:8000/docs
   ```

---

## API Reference

### `GET /`
Health check — confirms the API is running.

**Response:**
```json
{
  "message": "RAG Q&A API is running!"
}
```

---

### `POST /upload`
Upload a PDF or TXT file to be indexed into the vector database.

**Request:** `multipart/form-data` with a `file` field.

**Supported formats:** `.pdf`, `.txt`

**Response:**
```json
{
  "message": "Document indexed successfully",
  "filename": "my_document.pdf",
  "chunks_created": 103
}
```

---

### `POST /ask`
Ask a natural language question about the uploaded document.

**Request body:**
```json
{
  "question": "What are the main topics covered in this document?"
}
```

**Response:**
```json
{
  "question": "What are the main topics covered in this document?",
  "answer": "Based on the document, the main topics covered are..."
}
```

---

## Usage Example

```bash
# 1. Upload a document
curl -X POST http://localhost:8000/upload \
  -F "file=@my_document.pdf"

# 2. Ask a question
curl -X POST http://localhost:8000/ask \
  -H "Content-Type: application/json" \
  -d '{"question": "What is this document about?"}'
```

---

## Key Concepts Demonstrated

- **RAG Pipeline** — retrieval augmented generation for accurate, grounded answers
- **Vector Embeddings** — converting text to semantic vectors for similarity search
- **REST API Design** — clean FastAPI endpoints with automatic OpenAPI documentation
- **LLM Integration** — connecting to Groq's free LLaMA 3.3 model via API
- **Local Vector DB** — ChromaDB for persistent, fast similarity search

---


---

## License

MIT License — free to use and modify.

---

## Author

Built as part of an Agentic AI / GenAI engineering portfolio.

Connect on [LinkedIn](https://www.linkedin.com/in/marisha-dwivedi-513269271/) | [GitHub](https://github.com/marisha119-AI/)

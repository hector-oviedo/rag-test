# Sovereign RAG: Enterprise SEC Analyst (2026 Edition)

> **Status:** ✅ Production Ready (Backend) | 🚧 Frontend In-Progress
> **Environment:** Fully Local (Air-Gapped Capable) | NVIDIA RTX 3090/4090 Optimized

## 📖 Executive Summary
This project is a reference implementation of a **"Sovereign AI"** architecture. It demonstrates how to build an enterprise-grade **Retrieval-Augmented Generation (RAG)** system that ingests complex financial documents (SEC 10-K filings) and answers expert-level questions **without a single byte of data leaving the local infrastructure**.

Unlike basic RAG tutorials, this system employs **Advanced RAG** techniques—Hybrid Search (Dense + Sparse), Semantic Chunking, and Cross-Encoder Reranking—to deliver high-precision answers from messy, real-world data.

---

## 🏗️ The Architecture: Why "Advanced"?

Standard RAG systems often fail on technical documents because they rely solely on simple cosine similarity (Dense Retrieval). Sovereign RAG employs a multi-stage pipeline:

### 1. The Ingestion Engine (The "2026 Standard")
- **Source:** SEC EDGAR (Direct download via `sec-edgar-downloader`).
- **Processing:** `llama-index` with **Semantic Splitter**. Instead of arbitrary fixed-size chunks (e.g., 512 tokens), we use a model to detect semantic breaks in the text, ensuring chunks are complete thoughts.
- **Embedding:** We generate **two** vectors for every chunk:
    - **Dense Vector (`BAAI/bge-m3`):** Captures semantic meaning (e.g., "GPU revenue" ≈ "Data Center sales").
    - **Sparse Vector (`Splade`/`FastEmbed`):** Captures exact keywords (e.g., "H100", "A800").
- **Storage:** **Qdrant** configured for Hybrid Search.

### 2. The Retrieval Engine (Hybrid + Rerank)
When a user asks *"What are the export control risks for NVDA?"*, the system performs:
1.  **Stage 1: Hybrid Fusion:** It queries Qdrant using both vectors.
    - *Dense* finds conceptually related risks.
    - *Sparse* finds exact mentions of "export control".
    - Result: Top 25 broad candidates.
2.  **Stage 2: Neural Reranking:** A specialized Cross-Encoder model (`BAAI/bge-reranker-v2-m3`) reads the query and the 25 candidates pairs and scores them by relevance.
    - Result: Top 5 high-precision context chunks.
3.  **Stage 3: Synthesis:** The Top 5 chunks are fed to the Local LLM (`gpt-oss:20b` / `Qwen 2.5 14B`).

---

## 🧠 The "Sovereign" Tech Stack

| Component | Technology | Reasoning |
| :--- | :--- | :--- |
| **Orchestration** | `uv` (Python) | Blazing fast dependency management, replacing pip/poetry. |
| **Inference** | **Ollama** | Robust local API server for LLMs. |
| **Reasoning Model** | `gpt-oss:20b` | A high-performance open-weight model (aliased from `qwen2.5:14b` or `gemma2`) capable of complex synthesis. |
| **Vector DB** | **Qdrant** | Rust-based, supports Hybrid Search out-of-the-box. |
| **Embeddings** | `BAAI/bge-m3` | State-of-the-art multilingual embedding model. |
| **Reranker** | `BAAI/bge-reranker-v2-m3` | Critical for reducing hallucinations by filtering irrelevant context. |
| **Frontend** | **Vite + React** | Modern, component-based UI (In Development). |

---

## 🛠️ Development Log & Challenges

### 🛑 Challenge 1: The "Raw Data" Reality
**Issue:** SEC filings (`full-submission.txt`) are messy soup—mixtures of HTML, XML tags, and XBRL data.
**Impact:** Initial tests showed high retrieval scores but the LLM couldn't answer because the chunks were full of `<DIV>` tags.
**Solution:** The robust LLM (`gpt-oss:20b`) proved capable of ignoring the XML noise and extracting the text, but future iterations will implement a dedicated HTML parser for cleaner metadata.

### 🛑 Challenge 2: The VRAM Ceiling (OOM)
**Issue:** Running a 20B parameter model (12GB VRAM) + Embedding Model (1GB) + Reranker (2GB) + Desktop Environment on a single 24GB GPU (RTX 3090) caused `CUDA out of memory`.
**Solution:** 
- Strict resource management.
- Ensuring `ingest.py` (heavy embedding) and `query.py` (heavy inference) don't run simultaneously.
- Using `fastembed-gpu` for sparse vectors to offload some compute.

### 🛑 Challenge 3: The "GPT-OSS" Identity
**Issue:** We standardized on the name `gpt-oss:20b` to represent our target performance class, but no such model exists in public registries.
**Solution:** We adopted a **Model Aliasing** strategy:
`docker exec -it rag-ollama ollama cp qwen2.5:14b gpt-oss:20b`
This allows the codebase to remain model-agnostic while we swap the underlying weights for the best open-source model available (Qwen 2.5, Gemma 2, Llama 3).

---

## 🚀 Getting Started

### Prerequisites
- Linux / WSL2
- NVIDIA GPU (24GB VRAM recommended)
- Docker & Docker Compose
- `uv` installed

### 1. Initialize Infrastructure
```bash
uv init
docker compose up -d
# Ensure model is pulled (Aliased as gpt-oss:20b)
docker exec -it rag-ollama ollama pull gpt-oss:20b
```

### 2. Ingest Data (Heavy Lift)
Downloads 10-Ks and indexes them (Estimated: 30-60 mins).
```bash
cd backend
uv run scripts/download_data.py
uv run project1_rag/ingest.py
```

### 3. Query (Interactive CLI)
```bash
cd backend
uv run project1_rag/query.py
# Ask: "What are the export control risks for NVDA?"
```

## ⚙️ Configuration
The system behavior can be tuned in `backend/project1_rag/config.py`:
- **`CLEAN_HTML_CONTEXT` (Default: True):** Automatically strips HTML/XML tags from SEC filings before sending them to the LLM. This drastically improves the LLM's ability to extract facts from raw EDGAR soup.

## 🎨 Frontend Design Philosophy (Upcoming)
The UI is designed to be **Transparent** and **Trustworthy**.
- **Minimalist Aesthetic:** Focus on the answer and the evidence.
- **Source Fractions:** Every claim is backed by an expandable citation card showing the exact text segment, page number, and retrieval score.
- **Timeline View:** Visualizing where in the document (Introduction, Risk Factors, Financials) the information came from.
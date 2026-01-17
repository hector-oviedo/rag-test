# Sovereign RAG Implementation Plan

**Stack:**
- **Manager:** `uv`
- **Inference:** `Ollama` (running `gpt-oss:20b`)
- **Vector DB:** `Qdrant`
- **Ingestion:** `LlamaIndex`
- **Reasoning:** `gpt-oss:20b`
- **Frontend:** Vite (React), Modular Component Architecture.

## Phase 1: The "Agnostic" Infrastructure
- [x] **1.1 Project Initialization**
    - [ ] Initialize `backend` directory with `uv init`.
    - [ ] Create initial virtual environment and minimal dependency file.
- [x] **1.2 Container Orchestration**
    - [x] Create `docker-compose.yaml`.
    - [x] Configure **Qdrant** service (Ports 6333/6334, persistent volume).
    - [x] Configure **Ollama** service with GPU passthrough (deploy resources).
    - [x] Ensure **Ollama** pulls/runs `gpt-oss:20b`.
- [x] **1.3 Infrastructure Verification**
    - [ ] **HALT & VERIFY:** User runs `docker compose up` and curls localhost to ensure services are responding.

## Phase 2: Sovereign Data Acquisition
- [x] **2.1 Downloader Script**
    - [ ] Add `sec-edgar-downloader` to backend dependencies.
    - [ ] Create `backend/scripts/download_data.py`.
- [x] **2.2 Data Fetching**
    - [x] Implement logic to download 10-K filings for `NVDA` and `MSFT` to a local directory.
- [x] **2.3 Data Verification**
    - [ ] **HALT & VERIFY:** User checks file system for valid physical PDF/HTML files.

## Phase 3: Semantic Ingestion Pipeline (The 2026 Standard)
- [x] **3.1 Ingestion Setup**
    - [x] Create `backend/project1_rag/ingest.py`.
    - [x] Add `llama-index` and related dependencies to backend.
- [x] **3.2 Pipeline Logic**
    - [x] Configure **Embedding**: `HuggingFaceEmbedding` (model: `BAAI/bge-m3`).
    - [x] Configure **Chunking**: `SemanticSplitterNodeParser` (breakpoint_percentile_threshold=95).
    - [x] Configure **Indexing**: Connect to Qdrant with `enable_hybrid=True`.
- [x] **3.3 Execution & Verification**
    - [x] **HALT & VERIFY:** User runs ingestion script and confirms "Ingestion Complete" logs and Qdrant population. (Verified logic with `scripts/verify_ingestion_logic.py`).

## Phase 4: The Hybrid Retrieval Engine
- [x] **4.1 Query System Setup**
    - [x] Create `backend/project1_rag/query.py`.
- [x] **4.2 Retrieval Logic**
    - [x] Implement **Stage 1**: Hybrid Search (Top 25).
    - [x] Implement **Stage 2**: Reranking (`SentenceTransformerRerank`, `BAAI/bge-reranker-v2-m3`), Filter to Top 5.
    - [x] Implement **Stage 3**: Synthesis via Ollama (`gpt-oss:20b`).
- [ ] **4.3 End-to-End Verification**
    - [ ] **HALT & VERIFY:** User runs sample query ("What are the export control risks for NVDA?") and validates the answer and sources.

## Phase 5: The Frontend Experience
- [ ] **5.1 Frontend Structure**
    - [ ] Ensure `frontend/src/components` exists and is used.
    - [ ] Setup API client in frontend to talk to backend.
- [ ] **5.2 Interface Implementation**
    - [ ] Implement Chat Interface with Timeline/Source view.
    - [ ] **Feature:** "Source Fractions" - expandable source citations to verify chatbot answers.
    - [ ] **Design:** Minimalist, high-quality UI using modular hooks.
- [ ] **5.3 Frontend Verification**
    - [ ] **HALT & VERIFY:** User launches web UI and interacts.
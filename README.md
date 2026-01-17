# Sovereign RAG System (2026 Edition)

## 📌 Project Overview
This project is a state-of-the-art **Retrieval-Augmented Generation (RAG)** system designed for "Sovereign AI" environments—fully local, air-gapped, and privacy-centric. It specializes in ingesting, indexing, and reasoning over complex financial documents (specifically SEC 10-K filings) without relying on external cloud APIs.

## 🎯 Purpose
To demonstrate a production-grade, enterprise-ready architecture for sensitive document analysis using open-source Large Language Models (LLMs) and vector search technologies running entirely on local hardware (e.g., NVIDIA RTX 3090/4090).

## 🛠️ Tech Stack & Justification

### Backend & Orchestration
- **`uv` (Project Manager):** Selected for its blazing speed in dependency resolution and virtual environment management, replacing legacy tools like `pip` and `poetry`.
- **Python:** The lingua franca of AI/ML development.
- **Docker & Docker Compose:** Ensures reproducible, containerized deployment of infrastructure services.

### AI & Inference
- **Ollama:** The standard for local LLM inference. It provides a robust API compatible with OpenAI clients, enabling seamless integration.
- **Model: `gpt-oss:20b`:** A high-performance open-source model chosen for its balance of reasoning capability and resource efficiency, suitable for single-GPU deployments.
- **LlamaIndex:** The leading framework for connecting data to LLMs, providing advanced abstractions for ingestion, chunking, and retrieval.

### Vector Database
- **Qdrant:** A high-performance, Rust-based vector database. It is chosen for its native support of **Hybrid Search** (Dense + Sparse embeddings), which is critical for precise retrieval in technical domains.

### Frontend
- **Vite (React):** Chosen for its fast development server and optimized build process.
- **Architecture:** Component-based, modular design using Hooks to separate logic from UI, ensuring maintainability and scalability.

## 🧪 Testing & Verification Strategy
We adhere to a strict **"Golden Protocol"** of iterative development:
1.  ✅ **Infrastructure Verification:** COMPLETED. Containers (Qdrant, Ollama) are healthy and reachable.
2.  **Data Integrity:** Verifying physical downloads of 10-K filings.
3.  **Ingestion Validation:** confirming that text chunks and embeddings are correctly indexed in Qdrant.
4.  **Retrieval Evaluation:** Testing specific queries (e.g., "Export control risks for NVDA") to verify that the system retrieves relevant context before generating answers.

## 🚀 Getting Started

### Prerequisites
- Linux Environment
- NVIDIA GPU with drivers installed
- Conda environment: `rag-test`
- Docker & Docker Compose

### Installation
1.  Clone the repository.
2.  Ensure you are in the `rag-test` environment.
3.  Run `docker compose up -d` to start the infrastructure.
4.  Follow the phase-by-phase scripts in `backend/` to ingest data and run queries.

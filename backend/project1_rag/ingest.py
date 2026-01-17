"""
Sovereign Ingestion Pipeline.

This module handles the ingestion of 10-K filings into the Qdrant vector database.
It utilizes advanced semantic chunking and hybrid search capabilities.
"""

import os
import sys
from typing import List

from llama_index.core import (
    SimpleDirectoryReader,
    VectorStoreIndex,
    StorageContext,
    Settings,
)
from llama_index.core.node_parser import SemanticSplitterNodeParser
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


class IngestionPipeline:
    """
    Orchestrates the loading, chunking, and indexing of documents.
    """

    def __init__(self, data_dir: str, collection_name: str = "sec_filings"):
        """
        Initialize the pipeline.

        Args:
            data_dir (str): Directory containing the documents to ingest.
            collection_name (str): Name of the Qdrant collection.
        """
        self.data_dir = data_dir
        self.collection_name = collection_name
        self._setup_settings()
        self._setup_storage()

    def _setup_settings(self):
        """Configures global settings for LlamaIndex."""
        print("[INFO] Loading Embedding Model (BAAI/bge-m3)...")
        # High-performance multi-lingual embedding model
        Settings.embedding_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-m3",
            device="cuda"  # Explicitly request CUDA
        )
        
        # We don't need an LLM for ingestion, but to be safe/explicit:
        Settings.llm = None 

    def _setup_storage(self):
        """Initializes Qdrant client and vector store."""
        print("[INFO] Connecting to Qdrant...")
        self.client = QdrantClient(host="localhost", port=6333)
        
        self.vector_store = QdrantVectorStore(
            client=self.client,
            collection_name=self.collection_name,
            enable_hybrid=True, # CRITICAL: Enables sparse vectors for hybrid search
            batch_size=32 # Optimization for bulk ingestion
        )
        
        self.storage_context = StorageContext.from_defaults(
            vector_store=self.vector_store
        )

    def load_documents(self) -> List:
        """Loads documents from the data directory."""
        print(f"[INFO] Loading documents from {self.data_dir}...")
        if not os.path.exists(self.data_dir):
            print(f"[ERROR] Data directory {self.data_dir} not found.")
            return []
            
        reader = SimpleDirectoryReader(
            input_dir=self.data_dir,
            recursive=True,
            required_exts=[".html", ".xml", ".pdf", ".txt"] # EDGAR often has these
        )
        return reader.load_data()

    def run(self):
        """Executes the full ingestion pipeline."""
        documents = self.load_documents()
        if not documents:
            print("[WARN] No documents found to ingest.")
            return

        print(f"[INFO] Found {len(documents)} documents. Starting Semantic Chunking...")
        
        # 2026 Standard: Semantic Splitting
        splitter = SemanticSplitterNodeParser(
            buffer_size=1,
            breakpoint_percentile_threshold=95,
            embed_model=Settings.embedding_model
        )
        
        # We process manually to ensure control or just let Index handle it via transformation
        # Using VectorStoreIndex.from_documents handles the transformation if we pass transformations
        
        print("[INFO] Indexing documents (this may take a while)...")
        VectorStoreIndex.from_documents(
            documents,
            storage_context=self.storage_context,
            transformations=[splitter],
            show_progress=True
        )
        
        print("[SUCCESS] Ingestion Complete. Data is now searchable.")

def main():
    """Main entry point."""
    # Path resolution relative to this script
    # backend/project1_rag/ingest.py -> backend/data/sec-edgar-filings
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data", "sec-edgar-filings")
    
    pipeline = IngestionPipeline(data_dir=DATA_DIR)
    pipeline.run()

if __name__ == "__main__":
    main()

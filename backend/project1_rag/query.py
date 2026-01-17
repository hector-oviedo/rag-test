# Sovereign Hybrid Retrieval Engine.
#
# This module implements the retrieval and synthesis logic.
# It combines:
# 1. Hybrid Search (Dense + Sparse) via Qdrant.
# 2. Reranking via BAAI/bge-reranker-v2-m3.
# 3. Synthesis via Ollama (gpt-oss:20b).

import os
from typing import List, Optional

from llama_index.core import (
    VectorStoreIndex,
    StorageContext,
    Settings,
    get_response_synthesizer,
)
from llama_index.core.retrievers import VectorIndexRetriever
from llama_index.core.query_engine import RetrieverQueryEngine
from llama_index.core.postprocessor import SentenceTransformerRerank
from llama_index.core.chat_engine import ContextChatEngine
from llama_index.core.memory import ChatMemoryBuffer
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.vector_stores.qdrant import QdrantVectorStore
from qdrant_client import QdrantClient


class RAGQueryEngine:
    """
    The main engine for querying the RAG system.
    """

    def __init__(self, collection_name: str = "sec_filings"):
        self.collection_name = collection_name
        self._setup_settings()
        self._setup_index()
        self._setup_engine()

    def _setup_settings(self):
        """Configures LLM and Embedding models."""
        print("[INFO] Loading Embedding Model (BAAI/bge-m3)...")
        self.embed_model = HuggingFaceEmbedding(
            model_name="BAAI/bge-m3",
            device="cuda"
        )
        Settings.embed_model = self.embed_model

        print("[INFO] Connecting to Ollama (gpt-oss:20b)...")
        self.llm = Ollama(
            model="gpt-oss:20b",
            request_timeout=300.0,
            context_window=4096 
        )
        Settings.llm = self.llm

    def _setup_index(self):
        """Connects to existing Qdrant index."""
        print("[INFO] Connecting to Qdrant Storage...")
        client = QdrantClient(host="localhost", port=6333)
        
        vector_store = QdrantVectorStore(
            client=client,
            collection_name=self.collection_name,
            enable_hybrid=True 
        )
        
        # We don't ingest here, just load the index view
        self.index = VectorStoreIndex.from_vector_store(
            vector_store=vector_store,
            embed_model=self.embed_model
        )

    def _setup_engine(self):
        """Builds the retrieval and query engine pipeline."""
        print("[INFO] Configuring Hybrid Retriever & Reranker...")
        
        # 1. Hybrid Retriever (Top 25)
        self.retriever = VectorIndexRetriever(
            index=self.index,
            similarity_top_k=25,
            vector_store_query_mode="hybrid", # Explicitly request hybrid
            embed_model=self.embed_model
        )

        # 2. Reranker (Filter to Top 5)
        print("[INFO] Loading Reranker (BAAI/bge-reranker-v2-m3)...")
        self.reranker = SentenceTransformerRerank(
            model="BAAI/bge-reranker-v2-m3",
            top_n=5,
            device="cuda"
        )
        
        # 4. Chat Engine (Stateful)
        memory = ChatMemoryBuffer.from_defaults(token_limit=4000)
        
        self.chat_engine = ContextChatEngine.from_defaults(
            retriever=self.retriever,
            node_postprocessors=[self.reranker],
            llm=self.llm,
            memory=memory,
            system_prompt=(
                "You are a Sovereign Financial Analyst AI. "
                "You have access to SEC 10-K filings. "
                "Always cite your sources specifically using the context provided. "
                "If you don't know, say 'I cannot find that in the filings'."
            )
        )

    def chat(self, text: str):
        """Stateful chat."""
        return self.chat_engine.chat(text)


def main():
    """Interactive CLI testing."""
    engine = RAGQueryEngine()
    print("\n✅ System Ready. Type 'exit' to quit.\n")
    
    while True:
        try:
            user_input = input("Query > ")
            if user_input.lower() in ["exit", "quit"]:
                break
            
            # Use chat for conversation
            response = engine.chat(user_input)
            print("\n🤖 Answer:")
            print(response)
            
            print("\n📄 Sources:")
            for node in response.source_nodes:
                # Basic metadata print
                meta = node.metadata
                score = node.score
                print(f"- [Score: {score:.3f}] {meta.get('file_name', 'Unknown')} (Page {meta.get('page_label', '?')})")
                print(f"  > Content: {node.get_text()[:300].replace(chr(10), ' ')}...")
                
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

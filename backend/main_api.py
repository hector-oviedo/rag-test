"""
Sovereign RAG API.

This module exposes the RAG engine via a REST API using FastAPI.
It handles:
- Chat interactions.
- Source retrieval.
- Health checks.
"""

from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import uvicorn
import sys
import os

# Ensure backend modules are found
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from project1_rag.query import RAGQueryEngine

app = FastAPI(title="Sovereign RAG API", version="1.0.0")

# CORS Configuration (Allow Frontend)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], # For development; restrict in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global Engine Instance
engine: Optional[RAGQueryEngine] = None

class ChatRequest(BaseModel):
    message: str

class SourceNode(BaseModel):
    file_name: str
    page_label: str
    score: float
    content: str

class ChatResponse(BaseModel):
    answer: str
    sources: List[SourceNode]

@app.on_event("startup")
async def startup_event():
    """Initialize the RAG Engine on startup."""
    global engine
    print("[API] Initializing RAG Engine...")
    try:
        engine = RAGQueryEngine()
        print("[API] RAG Engine Ready.")
    except Exception as e:
        print(f"[API] Failed to initialize engine: {e}")
        # We don't exit here to allow API to start, but requests will fail
        pass

@app.get("/health")
async def health_check():
    return {"status": "ok", "engine_loaded": engine is not None}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Process a chat message and return the answer with sources.
    """
    global engine
    if not engine:
        raise HTTPException(status_code=503, detail="RAG Engine not initialized")
    
    try:
        response = engine.chat(request.message)
        
        # Extract sources
        sources = []
        for node in response.source_nodes:
            sources.append(SourceNode(
                file_name=node.metadata.get("file_name", "Unknown"),
                page_label=node.metadata.get("page_label", "?"),
                score=node.score if node.score else 0.0,
                content=node.get_text()
            ))
            
        return ChatResponse(
            answer=str(response),
            sources=sources
        )
        
    except Exception as e:
        print(f"[API Error] {e}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main_api:app", host="0.0.0.0", port=8000, reload=True)

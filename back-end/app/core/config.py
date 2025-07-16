from pydantic_settings import BaseSettings
from typing import Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    """Application settings"""
    
    # Application
    app_name: str = "RAG Chatbot API"
    app_version: str = "1.0.0"
    debug: bool = True
    
    # Google API
    google_api_key: str
    
    # LangChain (Optional)
    langchain_tracing_v2: Optional[str] = None
    langchain_endpoint: Optional[str] = None
    langchain_api_key: Optional[str] = None
    
    # Model Configuration
    llm_model: str = "gemini-2.0-flash"
    embedding_model: str = "models/embedding-001"
    max_tokens: Optional[int] = 1000
    temperature: float = 0.0
    
    # RAG Configuration
    chunk_size: int = 1000
    chunk_overlap: int = 200
    max_retrieval_docs: int = 4
    
    # Paths
    vector_store_path: str = "./vector_store"
    documents_path: str = "./data/documents"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

# Global settings instance
settings = Settings()

# Create directories if they don't exist
def create_directories():
    """Create necessary directories"""
    Path(settings.vector_store_path).mkdir(parents=True, exist_ok=True)
    Path(settings.documents_path).mkdir(parents=True, exist_ok=True)

create_directories() 
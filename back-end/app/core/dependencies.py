from fastapi import Depends
from app.core.config import settings
from app.services.rag_service import RAGService
from app.services.document_service import DocumentService
from app.services.chat_service import ChatService

# Dependency to get RAG service
def get_rag_service() -> RAGService:
    """Get RAG service instance"""
    return RAGService()

# Dependency to get document service
def get_document_service() -> DocumentService:
    """Get document service instance"""
    return DocumentService()

# Dependency to get chat service
def get_chat_service(
    rag_service: RAGService = Depends(get_rag_service)
) -> ChatService:
    """Get chat service instance"""
    return ChatService(rag_service)

# Dependency to get settings
def get_settings():
    """Get application settings"""
    return settings 
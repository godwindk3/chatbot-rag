from pydantic import BaseModel, Field, HttpUrl
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum

class DocumentType(str, Enum):
    """Document type enumeration"""
    TEXT = "text"
    PDF = "pdf"
    WEB = "web"
    MARKDOWN = "markdown"

class DocumentStatus(str, Enum):
    """Document processing status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"

class DocumentUploadRequest(BaseModel):
    """Document upload request"""
    content: str = Field(..., description="Document content", min_length=1)
    title: Optional[str] = Field(None, description="Document title")
    source: Optional[str] = Field(None, description="Document source/URL")
    doc_type: DocumentType = Field(DocumentType.TEXT, description="Document type")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "content": "This is a sample document content...",
                "title": "Sample Document",
                "source": "https://example.com",
                "doc_type": "text",
                "metadata": {"category": "general"}
            }
        }

class WebDocumentRequest(BaseModel):
    """Web document loading request"""
    url: HttpUrl = Field(..., description="URL to load document from")
    title: Optional[str] = Field(None, description="Document title")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    
    class Config:
        json_schema_extra = {
            "example": {
                "url": "https://lilianweng.github.io/posts/2023-06-23-agent/",
                "title": "LLM Powered Autonomous Agents",
                "metadata": {"category": "AI"}
            }
        }

class DocumentInfo(BaseModel):
    """Document information"""
    doc_id: str = Field(..., description="Document ID")
    title: Optional[str] = Field(None, description="Document title")
    source: Optional[str] = Field(None, description="Document source")
    doc_type: DocumentType = Field(..., description="Document type")
    status: DocumentStatus = Field(..., description="Processing status")
    chunk_count: Optional[int] = Field(None, description="Number of chunks created")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class DocumentResponse(BaseModel):
    """Document operation response"""
    doc_id: str = Field(..., description="Document ID")
    message: str = Field(..., description="Operation result message")
    status: DocumentStatus = Field(..., description="Document status")
    
    class Config:
        json_schema_extra = {
            "example": {
                "doc_id": "doc_123",
                "message": "Document processed successfully",
                "status": "completed"
            }
        }

class DocumentListResponse(BaseModel):
    """Document list response"""
    documents: List[DocumentInfo] = Field(..., description="List of documents")
    total: int = Field(..., description="Total number of documents")
    
class ChunkInfo(BaseModel):
    """Document chunk information"""
    chunk_id: str = Field(..., description="Chunk ID")
    doc_id: str = Field(..., description="Parent document ID")
    content: str = Field(..., description="Chunk content")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)
    embedding_status: Optional[str] = Field(None, description="Embedding status")

class VectorStoreStatus(BaseModel):
    """Vector store status"""
    total_documents: int = Field(..., description="Total documents in store")
    total_chunks: int = Field(..., description="Total chunks in store")
    last_updated: Optional[datetime] = Field(None, description="Last update time")
    
    class Config:
        json_schema_extra = {
            "example": {
                "total_documents": 5,
                "total_chunks": 50,
                "last_updated": "2024-01-01T12:00:00Z"
            }
        } 
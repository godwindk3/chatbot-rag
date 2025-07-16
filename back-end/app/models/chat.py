from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime

class ChatMessage(BaseModel):
    """Single chat message"""
    role: str = Field(..., description="Role of the message sender (user/assistant)")
    content: str = Field(..., description="Content of the message")
    timestamp: Optional[datetime] = Field(default_factory=datetime.now)

class ChatRequest(BaseModel):
    """Chat request model"""
    message: str = Field(..., description="User's message", min_length=1, max_length=2000)
    conversation_id: Optional[str] = Field(None, description="Conversation ID for context")
    include_sources: bool = Field(True, description="Whether to include source documents in response")
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "What is Task Decomposition?",
                "conversation_id": "conv_123",
                "include_sources": True
            }
        }

class SourceDocument(BaseModel):
    """Source document used in RAG response"""
    content: str = Field(..., description="Document content snippet")
    source: Optional[str] = Field(None, description="Document source/URL")
    score: Optional[float] = Field(None, description="Relevance score")
    metadata: Optional[Dict[str, Any]] = Field(default_factory=dict)

class ChatResponse(BaseModel):
    """Chat response model"""
    message: str = Field(..., description="Assistant's response")
    conversation_id: str = Field(..., description="Conversation ID")
    sources: Optional[List[SourceDocument]] = Field(None, description="Source documents used")
    processing_time: Optional[float] = Field(None, description="Processing time in seconds")
    timestamp: datetime = Field(default_factory=datetime.now)
    
    class Config:
        json_schema_extra = {
            "example": {
                "message": "Task decomposition is the process of breaking down complex tasks...",
                "conversation_id": "conv_123",
                "sources": [
                    {
                        "content": "Task decomposition involves...",
                        "source": "https://example.com",
                        "score": 0.95
                    }
                ],
                "processing_time": 1.23,
                "timestamp": "2024-01-01T12:00:00Z"
            }
        }

class ConversationHistory(BaseModel):
    """Conversation history"""
    conversation_id: str = Field(..., description="Conversation ID")
    messages: List[ChatMessage] = Field(..., description="List of messages in conversation")
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)

class ErrorResponse(BaseModel):
    """Error response model"""
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: Optional[str] = Field(None, description="Error code") 
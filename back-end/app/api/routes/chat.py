from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.chat import (
    ChatRequest, 
    ChatResponse, 
    ConversationHistory, 
    ErrorResponse
)
from app.services.chat_service import ChatService
from app.core.dependencies import get_chat_service

router = APIRouter(prefix="/chat", tags=["chat"])

@router.post("/", response_model=ChatResponse, summary="Send a chat message")
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Send a message to the chatbot and get a response.
    
    - **message**: The user's message/question
    - **conversation_id**: Optional conversation ID to continue existing conversation
    - **include_sources**: Whether to include source documents in response
    """
    try:
        response = chat_service.chat(
            message=request.message,
            conversation_id=request.conversation_id,
            include_sources=request.include_sources
        )
        return response
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error processing chat: {str(e)}"
        )

@router.get("/conversations", response_model=List[ConversationHistory], summary="List all conversations")
async def list_conversations(
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Get a list of all conversation histories.
    """
    try:
        conversations = chat_service.list_conversations()
        return conversations
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing conversations: {str(e)}"
        )

@router.get("/conversations/{conversation_id}", response_model=ConversationHistory, summary="Get conversation history")
async def get_conversation(
    conversation_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Get the history of a specific conversation.
    """
    try:
        conversation = chat_service.get_conversation_history(conversation_id)
        if not conversation:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Conversation not found"
            )
        return conversation
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting conversation: {str(e)}"
        )

@router.delete("/conversations/{conversation_id}", summary="Delete a conversation")
async def delete_conversation(
    conversation_id: str,
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Delete a specific conversation.
    """
    try:
        result = chat_service.delete_conversation(conversation_id)
        if result["status"] == "error":
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=result["message"]
            )
        return result
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error deleting conversation: {str(e)}"
        )

@router.delete("/conversations", summary="Clear all conversations")
async def clear_conversations(
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Clear all conversation histories.
    """
    try:
        result = chat_service.clear_all_conversations()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing conversations: {str(e)}"
        )

@router.get("/stats", summary="Get chat statistics")
async def get_chat_stats(
    chat_service: ChatService = Depends(get_chat_service)
):
    """
    Get chat statistics including total conversations, messages, etc.
    """
    try:
        stats = chat_service.get_chat_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting chat stats: {str(e)}"
        ) 
from typing import List, Dict, Any, Optional, Tuple
import logging
import uuid
import time
from datetime import datetime

from app.services.rag_service import RAGService
from app.models.chat import ChatMessage, ChatResponse, SourceDocument, ConversationHistory

logger = logging.getLogger(__name__)

class ChatService:
    """Chat service for handling conversations"""
    
    def __init__(self, rag_service: RAGService):
        self.rag_service = rag_service
        self.conversations = {}  # Simple in-memory storage for demo
    
    def chat(
        self,
        message: str,
        conversation_id: Optional[str] = None,
        include_sources: bool = True
    ) -> ChatResponse:
        """Process a chat message and return response"""
        try:
            start_time = time.time()
            
            # Generate conversation ID if not provided
            if not conversation_id:
                conversation_id = str(uuid.uuid4())
            
            # Get or create conversation history
            if conversation_id not in self.conversations:
                self.conversations[conversation_id] = ConversationHistory(
                    conversation_id=conversation_id,
                    messages=[]
                )
            
            conversation = self.conversations[conversation_id]
            
            # Add user message to conversation
            user_message = ChatMessage(
                role="user",
                content=message,
                timestamp=datetime.now()
            )
            conversation.messages.append(user_message)
            
            # Query RAG system
            response_text, source_docs = self.rag_service.query(message)
            
            # Process source documents
            sources = None
            if include_sources and source_docs:
                sources = []
                for doc in source_docs:
                    source = SourceDocument(
                        content=doc.page_content[:500] + "..." if len(doc.page_content) > 500 else doc.page_content,
                        source=doc.metadata.get("source"),
                        metadata=doc.metadata
                    )
                    sources.append(source)
            
            # Add assistant message to conversation
            assistant_message = ChatMessage(
                role="assistant",
                content=response_text,
                timestamp=datetime.now()
            )
            conversation.messages.append(assistant_message)
            
            # Update conversation
            conversation.updated_at = datetime.now()
            self.conversations[conversation_id] = conversation
            
            processing_time = time.time() - start_time
            
            # Create response
            response = ChatResponse(
                message=response_text,
                conversation_id=conversation_id,
                sources=sources,
                processing_time=processing_time,
                timestamp=datetime.now()
            )
            
            logger.info(f"Chat processed successfully for conversation {conversation_id}")
            
            return response
            
        except Exception as e:
            logger.error(f"Error processing chat: {str(e)}")
            # Return error response
            return ChatResponse(
                message="Xin lỗi, đã có lỗi xảy ra khi xử lý câu hỏi của bạn. Vui lòng thử lại.",
                conversation_id=conversation_id or str(uuid.uuid4()),
                sources=None,
                processing_time=0,
                timestamp=datetime.now()
            )
    
    def get_conversation_history(self, conversation_id: str) -> Optional[ConversationHistory]:
        """Get conversation history by ID"""
        try:
            return self.conversations.get(conversation_id)
        except Exception as e:
            logger.error(f"Error getting conversation history: {str(e)}")
            return None
    
    def list_conversations(self) -> List[ConversationHistory]:
        """List all conversations"""
        try:
            conversations = list(self.conversations.values())
            # Sort by updated_at descending
            conversations.sort(key=lambda x: x.updated_at, reverse=True)
            return conversations
        except Exception as e:
            logger.error(f"Error listing conversations: {str(e)}")
            return []
    
    def delete_conversation(self, conversation_id: str) -> Dict[str, Any]:
        """Delete a conversation"""
        try:
            if conversation_id not in self.conversations:
                return {"status": "error", "message": "Conversation not found"}
            
            del self.conversations[conversation_id]
            
            logger.info(f"Conversation {conversation_id} deleted successfully")
            
            return {"status": "success", "message": "Conversation deleted successfully"}
            
        except Exception as e:
            logger.error(f"Error deleting conversation {conversation_id}: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def clear_all_conversations(self) -> Dict[str, Any]:
        """Clear all conversations"""
        try:
            count = len(self.conversations)
            self.conversations.clear()
            
            logger.info(f"Cleared {count} conversations")
            
            return {"status": "success", "message": f"Cleared {count} conversations"}
            
        except Exception as e:
            logger.error(f"Error clearing conversations: {str(e)}")
            return {"status": "error", "message": str(e)}
    
    def get_chat_stats(self) -> Dict[str, Any]:
        """Get chat statistics"""
        try:
            total_conversations = len(self.conversations)
            total_messages = sum(len(conv.messages) for conv in self.conversations.values())
            
            # Calculate average messages per conversation
            avg_messages = total_messages / total_conversations if total_conversations > 0 else 0
            
            return {
                "total_conversations": total_conversations,
                "total_messages": total_messages,
                "average_messages_per_conversation": round(avg_messages, 2)
            }
            
        except Exception as e:
            logger.error(f"Error getting chat stats: {str(e)}")
            return {"total_conversations": 0, "total_messages": 0, "average_messages_per_conversation": 0} 
from typing import List, Dict, Any, Optional
import logging
import uuid
import json
import os
from datetime import datetime
from pathlib import Path

import bs4
from langchain_community.document_loaders import WebBaseLoader
from langchain_core.documents import Document

from app.core.config import settings
from app.models.document import DocumentType, DocumentStatus, DocumentInfo
from app.services.rag_service import RAGService
from app.utils.helpers import create_document_metadata

logger = logging.getLogger(__name__)

class DocumentService:
    """Document processing and management service"""
    
    def __init__(self):
        self.documents_db = {}  # Simple in-memory storage for demo
        self.documents_db_file = os.path.join(settings.documents_path, "documents_db.json")
        self._load_documents_db()
    
    def _load_documents_db(self):
        """Load documents database from file"""
        try:
            if os.path.exists(self.documents_db_file):
                with open(self.documents_db_file, 'r', encoding='utf-8') as f:
                    self.documents_db = json.load(f)
                logger.info(f"Loaded {len(self.documents_db)} documents from database")
            else:
                self.documents_db = {}
                logger.info("Created new documents database")
        except Exception as e:
            logger.error(f"Error loading documents database: {str(e)}")
            self.documents_db = {}
    
    def _save_documents_db(self):
        """Save documents database to file"""
        try:
            os.makedirs(os.path.dirname(self.documents_db_file), exist_ok=True)
            with open(self.documents_db_file, 'w', encoding='utf-8') as f:
                json.dump(self.documents_db, f, ensure_ascii=False, indent=2, default=str)
            logger.info("Documents database saved successfully")
        except Exception as e:
            logger.error(f"Error saving documents database: {str(e)}")
    
    def add_text_document(
        self,
        content: str,
        title: Optional[str] = None,
        source: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        rag_service: Optional[RAGService] = None
    ) -> Dict[str, Any]:
        """Add a text document"""
        try:
            # Generate document ID
            doc_id = str(uuid.uuid4())
            
            # Create document info
            doc_info = {
                "doc_id": doc_id,
                "title": title or f"Document {doc_id[:8]}",
                "source": source,
                "doc_type": DocumentType.TEXT.value,
                "status": DocumentStatus.PROCESSING.value,
                "chunk_count": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Save document info
            self.documents_db[doc_id] = doc_info
            self._save_documents_db()
            
            # Create LangChain document with filtered metadata
            doc_metadata = create_document_metadata(
                doc_id=doc_id,
                doc_type=DocumentType.TEXT.value,
                title=title,
                source=source,
                custom_metadata=metadata
            )
            
            langchain_doc = Document(
                page_content=content,
                metadata=doc_metadata
            )
            
            # Add to RAG system if provided
            if rag_service:
                result = rag_service.add_documents([langchain_doc])
                doc_info["chunk_count"] = result["chunks_created"]
                doc_info["status"] = DocumentStatus.COMPLETED.value
                doc_info["updated_at"] = datetime.now().isoformat()
                
                # Update database
                self.documents_db[doc_id] = doc_info
                self._save_documents_db()
                
                logger.info(f"Text document {doc_id} added successfully with {result['chunks_created']} chunks")
            else:
                doc_info["status"] = DocumentStatus.PENDING.value
                self.documents_db[doc_id] = doc_info
                self._save_documents_db()
            
            return {
                "doc_id": doc_id,
                "status": doc_info["status"],
                "message": "Document added successfully",
                "chunk_count": doc_info["chunk_count"]
            }
            
        except Exception as e:
            logger.error(f"Error adding text document: {str(e)}")
            # Update status to failed
            if doc_id in self.documents_db:
                self.documents_db[doc_id]["status"] = DocumentStatus.FAILED.value
                self._save_documents_db()
            raise
    
    def add_web_document(
        self,
        url: str,
        title: Optional[str] = None,
        metadata: Optional[Dict[str, Any]] = None,
        rag_service: Optional[RAGService] = None
    ) -> Dict[str, Any]:
        """Add a web document"""
        try:
            # Generate document ID
            doc_id = str(uuid.uuid4())
            
            # Create document info
            doc_info = {
                "doc_id": doc_id,
                "title": title or f"Web Document {doc_id[:8]}",
                "source": url,
                "doc_type": DocumentType.WEB.value,
                "status": DocumentStatus.PROCESSING.value,
                "chunk_count": 0,
                "created_at": datetime.now().isoformat(),
                "updated_at": datetime.now().isoformat(),
                "metadata": metadata or {}
            }
            
            # Save document info
            self.documents_db[doc_id] = doc_info
            self._save_documents_db()
            
            # Load web content
            loader = WebBaseLoader(
                web_paths=(url,),
                bs_kwargs=dict(
                    parse_only=bs4.SoupStrainer(
                        class_=("post-content", "post-title", "post-header", "content", "article", "main")
                    )
                ),
            )
            docs = loader.load()
            
            if not docs:
                raise ValueError("No content could be loaded from the URL")
            
            # Update document metadata with filtered values
            for doc in docs:
                doc_metadata = create_document_metadata(
                    doc_id=doc_id,
                    doc_type=DocumentType.WEB.value,
                    title=title,
                    source=url,
                    custom_metadata=metadata
                )
                doc.metadata.update(doc_metadata)
            
            # Add to RAG system if provided
            if rag_service:
                result = rag_service.add_documents(docs)
                doc_info["chunk_count"] = result["chunks_created"]
                doc_info["status"] = DocumentStatus.COMPLETED.value
                doc_info["updated_at"] = datetime.now().isoformat()
                
                # Update database
                self.documents_db[doc_id] = doc_info
                self._save_documents_db()
                
                logger.info(f"Web document {doc_id} added successfully with {result['chunks_created']} chunks")
            else:
                doc_info["status"] = DocumentStatus.PENDING.value
                self.documents_db[doc_id] = doc_info
                self._save_documents_db()
            
            return {
                "doc_id": doc_id,
                "status": doc_info["status"],
                "message": "Web document loaded and added successfully",
                "chunk_count": doc_info["chunk_count"]
            }
            
        except Exception as e:
            logger.error(f"Error adding web document: {str(e)}")
            # Update status to failed
            if doc_id in self.documents_db:
                self.documents_db[doc_id]["status"] = DocumentStatus.FAILED.value
                self._save_documents_db()
            raise
    
    def get_document(self, doc_id: str) -> Optional[DocumentInfo]:
        """Get document information by ID"""
        try:
            if doc_id in self.documents_db:
                doc_data = self.documents_db[doc_id]
                return DocumentInfo(**doc_data)
            return None
        except Exception as e:
            logger.error(f"Error getting document {doc_id}: {str(e)}")
            return None
    
    def list_documents(self) -> List[DocumentInfo]:
        """List all documents"""
        try:
            documents = []
            for doc_data in self.documents_db.values():
                documents.append(DocumentInfo(**doc_data))
            
            # Sort by created_at descending
            documents.sort(key=lambda x: x.created_at, reverse=True)
            return documents
            
        except Exception as e:
            logger.error(f"Error listing documents: {str(e)}")
            return []
    
    def delete_document(self, doc_id: str) -> Dict[str, Any]:
        """Delete a document"""
        try:
            if doc_id not in self.documents_db:
                return {"status": "error", "message": "Document not found"}
            
            # Remove from database
            del self.documents_db[doc_id]
            self._save_documents_db()
            
            # Note: In a production system, you would also need to remove 
            # the chunks from the vector store, which requires more complex logic
            
            logger.info(f"Document {doc_id} deleted successfully")
            
            return {"status": "success", "message": "Document deleted successfully"}
            
        except Exception as e:
            logger.error(f"Error deleting document {doc_id}: {str(e)}")
            raise
    
    def get_stats(self) -> Dict[str, Any]:
        """Get document statistics"""
        try:
            total_docs = len(self.documents_db)
            status_counts = {}
            type_counts = {}
            
            for doc_data in self.documents_db.values():
                status = doc_data["status"]
                doc_type = doc_data["doc_type"]
                
                status_counts[status] = status_counts.get(status, 0) + 1
                type_counts[doc_type] = type_counts.get(doc_type, 0) + 1
            
            return {
                "total_documents": total_docs,
                "by_status": status_counts,
                "by_type": type_counts
            }
            
        except Exception as e:
            logger.error(f"Error getting document stats: {str(e)}")
            return {"total_documents": 0, "by_status": {}, "by_type": {}} 
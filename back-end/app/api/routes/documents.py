from fastapi import APIRouter, Depends, HTTPException, status
from typing import List

from app.models.document import (
    DocumentUploadRequest,
    WebDocumentRequest,
    DocumentResponse,
    DocumentListResponse,
    DocumentInfo,
    VectorStoreStatus
)
from app.services.document_service import DocumentService
from app.services.rag_service import RAGService
from app.core.dependencies import get_document_service, get_rag_service

router = APIRouter(prefix="/documents", tags=["documents"])

@router.post("/text", response_model=DocumentResponse, summary="Add text document")
async def add_text_document(
    request: DocumentUploadRequest,
    document_service: DocumentService = Depends(get_document_service),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Add a text document to the knowledge base.
    
    - **content**: The text content of the document
    - **title**: Optional title for the document
    - **source**: Optional source URL or reference
    - **doc_type**: Document type (automatically set to 'text')
    - **metadata**: Optional metadata dictionary
    """
    try:
        result = document_service.add_text_document(
            content=request.content,
            title=request.title,
            source=request.source,
            metadata=request.metadata,
            rag_service=rag_service
        )
        
        return DocumentResponse(
            doc_id=result["doc_id"],
            message=result["message"],
            status=result["status"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding text document: {str(e)}"
        )

@router.post("/web", response_model=DocumentResponse, summary="Add web document")
async def add_web_document(
    request: WebDocumentRequest,
    document_service: DocumentService = Depends(get_document_service),
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Load and add a document from a web URL.
    
    - **url**: The URL to load the document from
    - **title**: Optional title for the document
    - **metadata**: Optional metadata dictionary
    """
    try:
        result = document_service.add_web_document(
            url=str(request.url),
            title=request.title,
            metadata=request.metadata,
            rag_service=rag_service
        )
        
        return DocumentResponse(
            doc_id=result["doc_id"],
            message=result["message"],
            status=result["status"]
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error adding web document: {str(e)}"
        )

@router.get("/", response_model=DocumentListResponse, summary="List all documents")
async def list_documents(
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Get a list of all documents in the knowledge base.
    """
    try:
        documents = document_service.list_documents()
        return DocumentListResponse(
            documents=documents,
            total=len(documents)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error listing documents: {str(e)}"
        )

@router.get("/{doc_id}", response_model=DocumentInfo, summary="Get document by ID")
async def get_document(
    doc_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Get detailed information about a specific document.
    """
    try:
        document = document_service.get_document(doc_id)
        if not document:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Document not found"
            )
        return document
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document: {str(e)}"
        )

@router.delete("/{doc_id}", summary="Delete document")
async def delete_document(
    doc_id: str,
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Delete a document from the knowledge base.
    Note: This only removes the document metadata. In a production system,
    you would also need to remove the chunks from the vector store.
    """
    try:
        result = document_service.delete_document(doc_id)
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
            detail=f"Error deleting document: {str(e)}"
        )

@router.get("/stats/overview", summary="Get document statistics")
async def get_document_stats(
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Get statistics about documents in the knowledge base.
    """
    try:
        stats = document_service.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting document stats: {str(e)}"
        )

@router.get("/vectorstore/status", response_model=VectorStoreStatus, summary="Get vector store status")
async def get_vectorstore_status(
    rag_service: RAGService = Depends(get_rag_service),
    document_service: DocumentService = Depends(get_document_service)
):
    """
    Get status information about the vector store.
    """
    try:
        rag_stats = rag_service.get_vectorstore_stats()
        doc_stats = document_service.get_stats()
        
        return VectorStoreStatus(
            total_documents=doc_stats.get("total_documents", 0),
            total_chunks=rag_stats.get("total_chunks", 0),
            last_updated=None  # Could be implemented to track last update time
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error getting vector store status: {str(e)}"
        )

@router.delete("/vectorstore/clear", summary="Clear vector store")
async def clear_vectorstore(
    rag_service: RAGService = Depends(get_rag_service)
):
    """
    Clear all documents from the vector store.
    WARNING: This will remove all embedded documents!
    """
    try:
        result = rag_service.clear_vectorstore()
        return result
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error clearing vector store: {str(e)}"
        ) 
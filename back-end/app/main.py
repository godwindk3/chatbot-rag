from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import sys
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.routes import chat, documents

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler("app.log")
    ]
)
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan manager"""
    # Startup
    logger.info("Starting up RAG Chatbot API...")
    logger.info(f"App Name: {settings.app_name}")
    logger.info(f"Version: {settings.app_version}")
    logger.info(f"Debug: {settings.debug}")
    
    try:
        # Test Google API connection on startup
        from app.services.rag_service import RAGService
        rag_service = RAGService()
        logger.info("RAG service initialized successfully")
        
        yield
        
    except Exception as e:
        logger.error(f"Failed to initialize application: {str(e)}")
        raise
    finally:
        # Shutdown
        logger.info("Shutting down RAG Chatbot API...")

# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    RAG Chatbot API - Một hệ thống chatbot thông minh sử dụng Retrieval Augmented Generation (RAG)
    
    ## Tính năng chính:
    
    * **Chat**: Tương tác với chatbot thông minh
    * **Quản lý tài liệu**: Thêm, xem, xóa tài liệu trong knowledge base
    * **RAG**: Tìm kiếm và trả lời dựa trên ngữ cảnh từ tài liệu
    * **Vector Store**: Lưu trữ và tìm kiếm embedding vectors
    
    ## Cách sử dụng:
    
    1. Thêm tài liệu vào knowledge base thông qua `/documents/text` hoặc `/documents/web`
    2. Sử dụng `/chat/` để tương tác với chatbot
    3. Chatbot sẽ trả lời dựa trên thông tin từ tài liệu đã thêm
    
    """,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(chat.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")

@app.get("/", tags=["health"])
async def root():
    """Root endpoint - API health check"""
    return {
        "message": "RAG Chatbot API is running!",
        "app_name": settings.app_name,
        "version": settings.app_version,
        "status": "healthy",
        "docs_url": "/docs",
        "redoc_url": "/redoc"
    }

@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint"""
    try:
        # Basic health check
        # Could add more sophisticated checks like DB connectivity, etc.
        return {
            "status": "healthy",
            "app_name": settings.app_name,
            "version": settings.app_version,
            "debug": settings.debug
        }
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        raise HTTPException(status_code=503, detail="Service unavailable")

@app.get("/api/v1/info", tags=["info"])
async def api_info():
    """API information endpoint"""
    return {
        "app_name": settings.app_name,
        "version": settings.app_version,
        "description": "RAG Chatbot API using LangChain and Google Generative AI",
        "endpoints": {
            "chat": "/api/v1/chat/",
            "documents": "/api/v1/documents/",
            "health": "/health",
            "docs": "/docs"
        },
        "models": {
            "llm": settings.llm_model,
            "embedding": settings.embedding_model
        },
        "configuration": {
            "chunk_size": settings.chunk_size,
            "chunk_overlap": settings.chunk_overlap,
            "max_retrieval_docs": settings.max_retrieval_docs,
            "temperature": settings.temperature
        }
    }

# Global exception handler
@app.exception_handler(Exception)
async def global_exception_handler(request, exc):
    """Global exception handler"""
    logger.error(f"Global exception: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "detail": str(exc) if settings.debug else "An unexpected error occurred"
        }
    )

if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug,
        log_level="info"
    ) 
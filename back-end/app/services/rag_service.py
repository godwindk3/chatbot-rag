from typing import List, Dict, Any, Optional, Tuple
import logging
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough
from langchain import hub
import os
import uuid

from app.core.config import settings
from app.utils.helpers import filter_metadata

logger = logging.getLogger(__name__)

class RAGService:
    """RAG (Retrieval Augmented Generation) Service"""
    
    def __init__(self):
        self.embeddings = None
        self.vectorstore = None
        self.llm = None
        self.text_splitter = None
        self.rag_chain = None
        self._initialize_components()
    
    def _initialize_components(self):
        """Initialize LangChain components"""
        try:
            # Initialize embeddings
            self.embeddings = GoogleGenerativeAIEmbeddings(
                model=settings.embedding_model,
                google_api_key=settings.google_api_key
            )
            
            # Initialize LLM
            self.llm = ChatGoogleGenerativeAI(
                model=settings.llm_model,
                temperature=settings.temperature,
                max_tokens=settings.max_tokens,
                google_api_key=settings.google_api_key
            )
            
            # Initialize text splitter
            self.text_splitter = RecursiveCharacterTextSplitter(
                chunk_size=settings.chunk_size,
                chunk_overlap=settings.chunk_overlap
            )
            
            # Initialize or load existing vectorstore
            self._initialize_vectorstore()
            
            # Setup RAG chain
            self._setup_rag_chain()
            
            logger.info("RAG components initialized successfully")
            
        except Exception as e:
            logger.error(f"Error initializing RAG components: {str(e)}")
            raise
    
    def _initialize_vectorstore(self):
        """Initialize vector store"""
        try:
            # Check if vectorstore already exists
            if os.path.exists(settings.vector_store_path):
                self.vectorstore = Chroma(
                    persist_directory=settings.vector_store_path,
                    embedding_function=self.embeddings
                )
                logger.info("Loaded existing vector store")
            else:
                # Create new empty vectorstore
                self.vectorstore = Chroma(
                    persist_directory=settings.vector_store_path,
                    embedding_function=self.embeddings
                )
                logger.info("Created new vector store")
                
        except Exception as e:
            logger.error(f"Error initializing vector store: {str(e)}")
            raise
    
    def _setup_rag_chain(self):
        """Setup RAG chain"""
        try:
            # Get retriever
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": settings.max_retrieval_docs}
            )
            
            # Try to load prompt from hub, fallback to custom prompt
            try:
                prompt = hub.pull("rlm/rag-prompt")
            except:
                # Fallback prompt
                template = """Bạn là một trợ lý AI thông minh cho việc trả lời câu hỏi. Sử dụng thông tin từ ngữ cảnh được cung cấp để trả lời câu hỏi. Nếu bạn không biết câu trả lời, hãy nói rằng bạn không biết. Hãy giữ câu trả lời ngắn gọn và chính xác.

Ngữ cảnh: {context}

Câu hỏi: {question}

Trả lời:"""
                prompt = ChatPromptTemplate.from_template(template)
            
            # Create RAG chain
            def format_docs(docs):
                return "\\n\\n".join(doc.page_content for doc in docs)
            
            self.rag_chain = (
                {"context": retriever | format_docs, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
            )
            
            logger.info("RAG chain setup completed")
            
        except Exception as e:
            logger.error(f"Error setting up RAG chain: {str(e)}")
            raise
    
    def add_documents(self, documents: List[Document]) -> Dict[str, Any]:
        """Add documents to vector store"""
        try:
            # Split documents into chunks
            chunks = self.text_splitter.split_documents(documents)
            
            # Add chunks to vectorstore with filtered metadata
            doc_ids = []
            for chunk in chunks:
                # Generate unique ID for each chunk
                chunk_id = str(uuid.uuid4())
                
                # Filter metadata and add chunk_id
                filtered_metadata = filter_metadata(chunk.metadata)
                filtered_metadata["chunk_id"] = chunk_id
                chunk.metadata = filtered_metadata
                
                doc_ids.append(chunk_id)
            
            # Add to vectorstore
            self.vectorstore.add_documents(chunks)
            
            # Persist the vectorstore
            self.vectorstore.persist()
            
            logger.info(f"Added {len(chunks)} chunks from {len(documents)} documents")
            
            return {
                "status": "success",
                "documents_added": len(documents),
                "chunks_created": len(chunks),
                "chunk_ids": doc_ids
            }
            
        except Exception as e:
            logger.error(f"Error adding documents: {str(e)}")
            raise
    
    def query(self, question: str) -> Tuple[str, List[Document]]:
        """Query the RAG system"""
        try:
            # Get retriever for source documents
            retriever = self.vectorstore.as_retriever(
                search_kwargs={"k": settings.max_retrieval_docs}
            )
            
            # Get source documents
            source_docs = retriever.invoke(question)
            
            # Generate response using RAG chain
            response = self.rag_chain.invoke(question)
            
            logger.info(f"Query processed successfully, found {len(source_docs)} source documents")
            
            return response, source_docs
            
        except Exception as e:
            logger.error(f"Error processing query: {str(e)}")
            raise
    
    def similarity_search(self, query: str, k: int = 4) -> List[Document]:
        """Perform similarity search"""
        try:
            results = self.vectorstore.similarity_search(query, k=k)
            return results
        except Exception as e:
            logger.error(f"Error in similarity search: {str(e)}")
            raise
    
    def get_vectorstore_stats(self) -> Dict[str, Any]:
        """Get vector store statistics"""
        try:
            # Get collection info
            collection = self.vectorstore._collection
            count = collection.count()
            
            return {
                "total_chunks": count,
                "vectorstore_path": settings.vector_store_path
            }
            
        except Exception as e:
            logger.error(f"Error getting vectorstore stats: {str(e)}")
            return {"total_chunks": 0, "vectorstore_path": settings.vector_store_path}
    
    def clear_vectorstore(self) -> Dict[str, Any]:
        """Clear all documents from vector store"""
        try:
            # Delete and recreate vectorstore
            import shutil
            if os.path.exists(settings.vector_store_path):
                shutil.rmtree(settings.vector_store_path)
            
            # Reinitialize vectorstore
            self._initialize_vectorstore()
            
            logger.info("Vector store cleared successfully")
            
            return {"status": "success", "message": "Vector store cleared"}
            
        except Exception as e:
            logger.error(f"Error clearing vectorstore: {str(e)}")
            raise 
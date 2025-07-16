#!/usr/bin/env python3
"""
Test script for RAG Chatbot API
Demonstrates basic functionality of the API
"""

import requests
import json
import time
from typing import Dict, Any

# API Configuration
API_BASE_URL = "http://localhost:8000"
API_V1_BASE = f"{API_BASE_URL}/api/v1"

def test_health_check():
    """Test health check endpoint"""
    print("🏥 Testing health check...")
    try:
        response = requests.get(f"{API_BASE_URL}/health")
        if response.status_code == 200:
            print("✅ Health check passed")
            print(f"Response: {response.json()}")
        else:
            print(f"❌ Health check failed: {response.status_code}")
    except Exception as e:
        print(f"❌ Health check error: {str(e)}")
    print()

def test_api_info():
    """Test API info endpoint"""
    print("ℹ️ Testing API info...")
    try:
        response = requests.get(f"{API_V1_BASE}/info")
        if response.status_code == 200:
            print("✅ API info retrieved")
            info = response.json()
            print(f"App: {info['app_name']}")
            print(f"Version: {info['version']}")
            print(f"LLM Model: {info['models']['llm']}")
        else:
            print(f"❌ API info failed: {response.status_code}")
    except Exception as e:
        print(f"❌ API info error: {str(e)}")
    print()

def add_sample_document():
    """Add a sample text document"""
    print("📄 Adding sample document...")
    
    sample_content = """
    Task Decomposition là một kỹ thuật quan trọng trong xử lý ngôn ngữ tự nhiên và trí tuệ nhân tạo. 
    Đây là quá trình chia nhỏ một nhiệm vụ phức tạp thành các nhiệm vụ con đơn giản hơn, 
    dễ quản lý hơn. Kỹ thuật này giúp các mô hình AI có thể xử lý các vấn đề phức tạp 
    một cách hiệu quả bằng cách giải quyết từng phần nhỏ.
    
    Ưu điểm của Task Decomposition:
    1. Giảm độ phức tạp của bài toán
    2. Tăng tính hiểu biết và kiểm soát
    3. Cho phép song song hóa xử lý
    4. Dễ dàng debug và maintenance
    
    Các phương pháp phổ biến:
    - Chain of Thought (CoT)
    - Tree of Thoughts
    - Subgoal decomposition
    """
    
    document_data = {
        "content": sample_content,
        "title": "Task Decomposition - Kỹ thuật chia nhỏ nhiệm vụ",
        "metadata": {
            "category": "AI/NLP",
            "language": "Vietnamese",
            "topic": "Task Decomposition"
        }
    }
    
    try:
        response = requests.post(
            f"{API_V1_BASE}/documents/text",
            json=document_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document added successfully")
            print(f"Document ID: {result['doc_id']}")
            print(f"Status: {result['status']}")
            return result['doc_id']
        else:
            print(f"❌ Failed to add document: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error adding document: {str(e)}")
        return None

def add_web_document():
    """Add a web document"""
    print("🌐 Adding web document...")
    
    web_data = {
        "url": "https://lilianweng.github.io/posts/2023-06-23-agent/",
        "title": "LLM Powered Autonomous Agents",
        "metadata": {
            "category": "AI Research",
            "source": "Lilian Weng Blog"
        }
    }
    
    try:
        response = requests.post(
            f"{API_V1_BASE}/documents/web",
            json=web_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Web document added successfully")
            print(f"Document ID: {result['doc_id']}")
            return result['doc_id']
        else:
            print(f"❌ Failed to add web document: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Error adding web document: {str(e)}")
        return None

def test_chat(question: str):
    """Test chat functionality"""
    print(f"💬 Testing chat with question: '{question}'")
    
    chat_data = {
        "message": question,
        "include_sources": True
    }
    
    try:
        response = requests.post(
            f"{API_V1_BASE}/chat/",
            json=chat_data,
            headers={"Content-Type": "application/json"}
        )
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Chat response received")
            print(f"Response: {result['message']}")
            print(f"Conversation ID: {result['conversation_id']}")
            print(f"Processing Time: {result['processing_time']:.2f}s")
            
            if result.get('sources'):
                print(f"Sources found: {len(result['sources'])}")
                for i, source in enumerate(result['sources'][:2]):  # Show first 2 sources
                    print(f"  Source {i+1}: {source['content'][:100]}...")
            
            return result['conversation_id']
        else:
            print(f"❌ Chat failed: {response.status_code}")
            print(f"Error: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Chat error: {str(e)}")
        return None

def test_document_list():
    """Test document listing"""
    print("📚 Testing document list...")
    
    try:
        response = requests.get(f"{API_V1_BASE}/documents/")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Document list retrieved")
            print(f"Total documents: {result['total']}")
            
            for doc in result['documents'][:3]:  # Show first 3 documents
                print(f"  - {doc['title']} ({doc['doc_type']}) - {doc['status']}")
        else:
            print(f"❌ Failed to get documents: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting documents: {str(e)}")

def test_vectorstore_status():
    """Test vector store status"""
    print("🗄️ Testing vector store status...")
    
    try:
        response = requests.get(f"{API_V1_BASE}/documents/vectorstore/status")
        
        if response.status_code == 200:
            result = response.json()
            print("✅ Vector store status retrieved")
            print(f"Total documents: {result['total_documents']}")
            print(f"Total chunks: {result['total_chunks']}")
        else:
            print(f"❌ Failed to get vector store status: {response.status_code}")
            
    except Exception as e:
        print(f"❌ Error getting vector store status: {str(e)}")

def main():
    """Main test function"""
    print("🚀 Starting RAG Chatbot API Tests")
    print("=" * 50)
    
    # Test basic connectivity
    test_health_check()
    test_api_info()
    
    # Add sample documents
    print("📄 DOCUMENT MANAGEMENT TESTS")
    print("-" * 30)
    
    # Add text document
    doc_id = add_sample_document()
    time.sleep(2)  # Wait for processing
    
    # Add web document (might take longer)
    web_doc_id = add_web_document()
    time.sleep(5)  # Wait for web loading and processing
    
    # Test document listing
    test_document_list()
    print()
    
    # Test vector store
    test_vectorstore_status()
    print()
    
    # Test chat functionality
    print("💬 CHAT TESTS")
    print("-" * 15)
    
    # Test questions
    questions = [
        "Task Decomposition là gì?",
        "Ưu điểm của Task Decomposition là gì?",
        "What is an autonomous agent?",
        "Explain planning in AI agents"
    ]
    
    for question in questions:
        test_chat(question)
        print()
        time.sleep(1)  # Brief pause between requests
    
    print("🎉 API Tests Completed!")
    print("\n📋 Summary:")
    print("- Health check and API info")
    print("- Document upload (text and web)")
    print("- Document listing and vector store status")
    print("- Chat functionality with source retrieval")
    print("\n🌐 Access API documentation at:")
    print(f"- Swagger UI: {API_BASE_URL}/docs")
    print(f"- ReDoc: {API_BASE_URL}/redoc")

if __name__ == "__main__":
    main() 
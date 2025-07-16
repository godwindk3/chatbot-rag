#!/usr/bin/env python3
"""
Debug script để kiểm tra kết nối và tìm nguyên nhân lỗi "Mất kết nối"
"""

import requests
import subprocess
import sys
import json
import os
from urllib.parse import urljoin

def check_port(port):
    """Kiểm tra xem port có đang được sử dụng không"""
    try:
        result = subprocess.run(['netstat', '-ano'], capture_output=True, text=True, shell=True)
        return f':{port}' in result.stdout
    except:
        return False

def check_backend_health(base_url):
    """Kiểm tra health endpoint của backend"""
    health_urls = [
        f"{base_url}/health",
        f"{base_url}/api/v1/health", 
        f"{base_url}/docs",  # FastAPI docs
    ]
    
    for url in health_urls:
        try:
            print(f"🔍 Checking: {url}")
            response = requests.get(url, timeout=5)
            print(f"✅ {url} - Status: {response.status_code}")
            if response.status_code == 200:
                try:
                    data = response.json()
                    print(f"   Response: {json.dumps(data, indent=2)}")
                except:
                    print(f"   Response: {response.text[:200]}")
            return True
        except requests.exceptions.ConnectionError:
            print(f"❌ {url} - Connection refused")
        except requests.exceptions.Timeout:
            print(f"⏰ {url} - Timeout")
        except Exception as e:
            print(f"❌ {url} - Error: {e}")
    
    return False

def check_frontend_config():
    """Kiểm tra cấu hình frontend"""
    config_files = [
        'front-end/vite.config.ts',
        'front-end/src/services/api.ts',
        'front-end/.env',
        'front-end/.env.local'
    ]
    
    print("\n📁 Frontend Configuration:")
    for file_path in config_files:
        if os.path.exists(file_path):
            print(f"✅ Found: {file_path}")
            if 'api.ts' in file_path:
                with open(file_path, 'r', encoding='utf-8') as f:
                    content = f.read()
                    if 'baseURL' in content:
                        lines = content.split('\n')
                        for i, line in enumerate(lines):
                            if 'baseURL' in line:
                                print(f"   Line {i+1}: {line.strip()}")
        else:
            print(f"❌ Missing: {file_path}")

def main():
    print("🔍 RAG Chatbot Connection Debug")
    print("=" * 50)
    
    # 1. Kiểm tra backend ports
    print("\n🔌 Port Check:")
    backend_ports = [8000, 8080, 3000]
    running_ports = []
    
    for port in backend_ports:
        if check_port(port):
            print(f"✅ Port {port} is in use")
            running_ports.append(port)
        else:
            print(f"❌ Port {port} is free")
    
    # 2. Kiểm tra backend health
    print("\n🏥 Backend Health Check:")
    backend_running = False
    
    if running_ports:
        for port in running_ports:
            base_url = f"http://localhost:{port}"
            print(f"\n🔍 Testing backend at {base_url}")
            if check_backend_health(base_url):
                backend_running = True
                break
    else:
        print("❌ No backend ports detected")
        # Try common URLs anyway
        for port in [8000, 8080]:
            base_url = f"http://localhost:{port}"
            print(f"\n🔍 Testing backend at {base_url}")
            if check_backend_health(base_url):
                backend_running = True
                break
    
    # 3. Kiểm tra frontend config
    check_frontend_config()
    
    # 4. Đưa ra kết luận và hướng dẫn
    print("\n" + "=" * 50)
    print("📊 DIAGNOSTIC SUMMARY:")
    print("=" * 50)
    
    if not backend_running:
        print("❌ PROBLEM: Backend is not running")
        print("\n🔧 SOLUTIONS:")
        print("1. Start the backend server:")
        print("   cd back-end")
        print("   python -m uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload")
        print("\n2. Or run with python directly:")
        print("   cd back-end")
        print("   python -m app.main")
    else:
        print("✅ Backend appears to be running")
        print("\n🔧 If frontend still shows 'Mất kết nối', check:")
        print("1. CORS configuration in backend")
        print("2. Frontend proxy configuration")
        print("3. Browser console for actual error messages")
    
    print("\n🌐 Frontend URLs to test:")
    print("- Development server: http://localhost:5173")
    print("- Backend API: http://localhost:8000")
    print("- Backend docs: http://localhost:8000/docs")

if __name__ == "__main__":
    main() 
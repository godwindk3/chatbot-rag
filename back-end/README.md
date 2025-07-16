# RAG Chatbot API

Hệ thống chatbot thông minh sử dụng Retrieval Augmented Generation (RAG) với LangChain và Google Generative AI.

## 🚀 Tính năng

- **Chatbot thông minh**: Trả lời câu hỏi dựa trên knowledge base
- **RAG (Retrieval Augmented Generation)**: Tìm kiếm và trả lời dựa trên ngữ cảnh
- **Quản lý tài liệu**: Thêm tài liệu từ text hoặc web URL
- **Vector Search**: Tìm kiếm semantic với embeddings
- **FastAPI**: API hiện đại với documentation tự động
- **Modular Architecture**: Dễ bảo trì và mở rộng

## 🛠️ Công nghệ sử dụng

- **FastAPI**: Web framework cho API
- **LangChain**: Framework cho ứng dụng LLM
- **Google Generative AI**: LLM và embeddings (free tier)
- **ChromaDB**: Vector database
- **Pydantic**: Data validation
- **Beautiful Soup**: Web scraping

## 📋 Yêu cầu hệ thống

- Python 3.8+
- Google API Key (free tier)

## 🔧 Cài đặt

### 1. Clone repository

```bash
git clone <repository-url>
cd chatbot-rag/back-end
```

### 2. Tạo virtual environment

```bash
python -m venv venv

# Windows
venv\\Scripts\\activate

# Linux/Mac
source venv/bin/activate
```

### 3. Cài đặt dependencies

```bash
pip install -r requirements.txt
```

### 4. Cấu hình environment

Tạo file `.env` trong thư mục `back-end`:

```env
# Google API Configuration
GOOGLE_API_KEY=your_google_api_key_here

# LangChain Configuration (Optional)
LANGCHAIN_TRACING_V2=false
LANGCHAIN_ENDPOINT=
LANGCHAIN_API_KEY=

# Application Configuration
APP_NAME=RAG Chatbot API
APP_VERSION=1.0.0
DEBUG=True

# Database Configuration
VECTOR_STORE_PATH=./vector_store
DOCUMENTS_PATH=./data/documents

# API Configuration
MAX_TOKENS=1000
TEMPERATURE=0.0
CHUNK_SIZE=1000
CHUNK_OVERLAP=200
```

### 5. Lấy Google API Key

1. Truy cập [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Tạo API key mới
3. Copy và paste vào file `.env`

## 🚀 Chạy ứng dụng

### Development mode

```bash
cd back-end
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Production mode

```bash
cd back-end
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

API sẽ chạy tại: http://localhost:8000

## 📚 API Documentation

Sau khi chạy server, truy cập:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **API Info**: http://localhost:8000/api/v1/info

## 🔗 API Endpoints

### Chat

- `POST /api/v1/chat/` - Gửi tin nhắn tới chatbot
- `GET /api/v1/chat/conversations` - Lấy danh sách cuộc hội thoại
- `GET /api/v1/chat/conversations/{id}` - Lấy chi tiết cuộc hội thoại
- `DELETE /api/v1/chat/conversations/{id}` - Xóa cuộc hội thoại
- `GET /api/v1/chat/stats` - Thống kê chat

### Documents

- `POST /api/v1/documents/text` - Thêm tài liệu text
- `POST /api/v1/documents/web` - Thêm tài liệu từ web URL
- `GET /api/v1/documents/` - Lấy danh sách tài liệu
- `GET /api/v1/documents/{id}` - Lấy chi tiết tài liệu
- `DELETE /api/v1/documents/{id}` - Xóa tài liệu
- `GET /api/v1/documents/vectorstore/status` - Trạng thái vector store

## 📝 Ví dụ sử dụng

### 1. Thêm tài liệu

```bash
curl -X POST "http://localhost:8000/api/v1/documents/text" \\
  -H "Content-Type: application/json" \\
  -d '{
    "content": "Task decomposition là quá trình chia nhỏ một tác vụ phức tạp thành các tác vụ con đơn giản hơn.",
    "title": "Task Decomposition",
    "metadata": {"category": "AI"}
  }'
```

### 2. Chat với bot

```bash
curl -X POST "http://localhost:8000/api/v1/chat/" \\
  -H "Content-Type: application/json" \\
  -d '{
    "message": "Task decomposition là gì?",
    "include_sources": true
  }'
```

### 3. Thêm tài liệu từ web

```bash
curl -X POST "http://localhost:8000/api/v1/documents/web" \\
  -H "Content-Type: application/json" \\
  -d '{
    "url": "https://lilianweng.github.io/posts/2023-06-23-agent/",
    "title": "LLM Powered Autonomous Agents"
  }'
```

## 🏗️ Kiến trúc

```
back-end/
├── app/
│   ├── __init__.py
│   ├── main.py                 # FastAPI application
│   ├── core/
│   │   ├── config.py          # Configuration settings
│   │   └── dependencies.py    # FastAPI dependencies
│   ├── models/
│   │   ├── chat.py           # Chat Pydantic models
│   │   └── document.py       # Document Pydantic models
│   ├── services/
│   │   ├── rag_service.py    # RAG logic with LangChain
│   │   ├── document_service.py # Document processing
│   │   └── chat_service.py   # Chat logic
│   ├── api/
│   │   └── routes/
│   │       ├── chat.py       # Chat endpoints
│   │       └── documents.py  # Document endpoints
│   └── utils/
│       └── helpers.py        # Utility functions
├── vector_store/             # ChromaDB storage
├── data/
│   └── documents/           # Document metadata
├── requirements.txt
└── README.md
```

## 🔄 Workflow

1. **Thêm tài liệu**: Upload text hoặc load từ web URL
2. **Text Splitting**: Chia tài liệu thành chunks
3. **Embedding**: Tạo vector embeddings cho chunks
4. **Vector Store**: Lưu embeddings vào ChromaDB
5. **Query**: User gửi câu hỏi
6. **Retrieval**: Tìm chunks liên quan từ vector store
7. **Generation**: LLM tạo câu trả lời dựa trên context
8. **Response**: Trả về câu trả lời kèm sources

## 🌐 Kết nối Frontend

API được thiết kế để dễ dàng kết nối với frontend:

- **CORS enabled**: Cho phép cross-origin requests
- **JSON API**: Standard REST API với JSON
- **Error handling**: Consistent error responses
- **Documentation**: Auto-generated API docs

### Ví dụ JavaScript

```javascript
// Chat với bot
async function sendMessage(message) {
  const response = await fetch('http://localhost:8000/api/v1/chat/', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      message: message,
      include_sources: true
    })
  });
  
  const data = await response.json();
  return data;
}

// Thêm tài liệu
async function addDocument(content, title) {
  const response = await fetch('http://localhost:8000/api/v1/documents/text', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      content: content,
      title: title
    })
  });
  
  const data = await response.json();
  return data;
}
```

## 🐛 Troubleshooting

### Lỗi Google API Key

```
Error: Invalid API key
```

**Giải pháp**: 
- Kiểm tra API key trong file `.env`
- Đảm bảo API key có quyền truy cập Generative AI API

### Lỗi Import

```
ModuleNotFoundError: No module named 'app'
```

**Giải pháp**:
```bash
# Chạy từ thư mục back-end
cd back-end
python -m uvicorn app.main:app --reload
```

### Lỗi Vector Store

```
Error initializing vector store
```

**Giải pháp**:
- Xóa thư mục `vector_store`
- Restart server để tạo lại

## 📈 Monitoring

- **Logs**: Xem file `app.log`
- **Health check**: `GET /health`
- **Stats**: `GET /api/v1/chat/stats`

## 🔒 Security Notes

- **Production**: Thay đổi `allow_origins=["*"]` thành domains cụ thể
- **API Key**: Không commit API key vào git
- **Environment**: Sử dụng environment variables cho production

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Create Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết. 
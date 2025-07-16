import React, { useEffect } from 'react'
import { useApp } from '@/context/AppContext'
import { Button, Loading } from '@/components/ui'
import { 
  Server, 
  Database, 
  Settings, 
  RefreshCw, 
  Trash2, 
  CheckCircle, 
  XCircle,
  Info
} from 'lucide-react'
// import { clsx } from 'clsx' // Not used

const SettingsPage: React.FC = () => {
  const { state, actions } = useApp()

  useEffect(() => {
    actions.fetchApiInfo()
    actions.fetchVectorStoreStatus()
    actions.fetchDocumentStats()
  }, [])

  const handleRefreshConnection = async () => {
    try {
      await actions.checkConnection()
      await actions.fetchApiInfo()
    } catch (error) {
      console.error('Failed to refresh connection:', error)
    }
  }

  const handleClearVectorStore = async () => {
    if (window.confirm('Bạn có chắc chắn muốn xóa toàn bộ vector store? Hành động này không thể hoàn tác.')) {
      try {
        await actions.clearVectorStore()
      } catch (error) {
        console.error('Failed to clear vector store:', error)
      }
    }
  }

  const handleClearConversations = async () => {
    if (window.confirm('Bạn có chắc chắn muốn xóa toàn bộ lịch sử trò chuyện?')) {
      try {
        await actions.clearAllConversations()
      } catch (error) {
        console.error('Failed to clear conversations:', error)
      }
    }
  }

  return (
    <div className="h-full overflow-y-auto bg-gray-50">
      <div className="max-w-4xl mx-auto p-6 space-y-6">
        {/* Page Header */}
        <div>
          <h1 className="text-2xl font-bold text-gray-900">Cài đặt</h1>
          <p className="text-gray-600 mt-1">
            Quản lý và cấu hình hệ thống RAG Chatbot
          </p>
        </div>

        {/* Connection Status */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Server className="w-6 h-6 text-gray-600" />
              <h2 className="text-lg font-semibold text-gray-900">Kết nối Backend</h2>
            </div>
            <Button
              variant="secondary"
              size="sm"
              onClick={handleRefreshConnection}
              loading={state.app.loading.isLoading}
              className="flex items-center gap-2"
            >
              <RefreshCw className="w-4 h-4" />
              Kiểm tra lại
            </Button>
          </div>

          <div className="space-y-3">
            <div className="flex items-center gap-3">
              {state.app.isConnected ? (
                <>
                  <CheckCircle className="w-5 h-5 text-green-600" />
                  <span className="text-green-600 font-medium">Đã kết nối</span>
                </>
              ) : (
                <>
                  <XCircle className="w-5 h-5 text-red-600" />
                  <span className="text-red-600 font-medium">Mất kết nối</span>
                </>
              )}
            </div>

            {state.app.apiInfo && (
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                <div className="space-y-2">
                  <h3 className="text-sm font-medium text-gray-700">Thông tin API</h3>
                  <div className="text-sm text-gray-600 space-y-1">
                    <div>Tên: {state.app.apiInfo.app_name}</div>
                    <div>Phiên bản: {state.app.apiInfo.version}</div>
                    <div>LLM Model: {state.app.apiInfo.models.llm}</div>
                    <div>Embedding: {state.app.apiInfo.models.embedding}</div>
                  </div>
                </div>
                <div className="space-y-2">
                  <h3 className="text-sm font-medium text-gray-700">Cấu hình</h3>
                  <div className="text-sm text-gray-600 space-y-1">
                    <div>Chunk Size: {state.app.apiInfo.configuration.chunk_size}</div>
                    <div>Chunk Overlap: {state.app.apiInfo.configuration.chunk_overlap}</div>
                    <div>Max Retrieval: {state.app.apiInfo.configuration.max_retrieval_docs}</div>
                    <div>Temperature: {state.app.apiInfo.configuration.temperature}</div>
                  </div>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Vector Store Management */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Database className="w-6 h-6 text-gray-600" />
              <h2 className="text-lg font-semibold text-gray-900">Vector Store</h2>
            </div>
            {state.documents.vectorStoreStatus && state.documents.vectorStoreStatus.total_documents > 0 && (
              <Button
                variant="danger"
                size="sm"
                onClick={handleClearVectorStore}
                className="flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Xóa toàn bộ
              </Button>
            )}
          </div>

          {state.documents.loading.isLoading ? (
            <Loading text="Đang tải thông tin vector store..." />
          ) : state.documents.vectorStoreStatus ? (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">
                  {state.documents.vectorStoreStatus.total_documents}
                </div>
                <div className="text-sm text-gray-600">Tài liệu</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">
                  {state.documents.vectorStoreStatus.total_chunks}
                </div>
                <div className="text-sm text-gray-600">Chunks</div>
              </div>
              <div className="text-center p-4 bg-gray-50 rounded-lg">
                <div className="text-2xl font-bold text-primary-600">
                  {Math.round((state.documents.vectorStoreStatus.total_chunks / 
                    Math.max(state.documents.vectorStoreStatus.total_documents, 1)) * 10) / 10}
                </div>
                <div className="text-sm text-gray-600">Chunks/Doc</div>
              </div>
            </div>
          ) : (
            <div className="text-center py-8 text-gray-500">
              <Database className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <p>Không có thông tin vector store</p>
            </div>
          )}
        </div>

        {/* Chat Management */}
        <div className="card p-6">
          <div className="flex items-center justify-between mb-4">
            <div className="flex items-center gap-3">
              <Settings className="w-6 h-6 text-gray-600" />
              <h2 className="text-lg font-semibold text-gray-900">Quản lý Chat</h2>
            </div>
            <Button
              variant="danger"
              size="sm"
              onClick={handleClearConversations}
              className="flex items-center gap-2"
            >
              <Trash2 className="w-4 h-4" />
              Xóa lịch sử
            </Button>
          </div>

          <div className="space-y-3">
            <p className="text-sm text-gray-600">
              Xóa toàn bộ lịch sử trò chuyện để bắt đầu lại từ đầu.
            </p>
            
            <div className="flex items-center gap-2 text-sm text-gray-600">
              <Info className="w-4 h-4" />
              <span>Cuộc trò chuyện hiện tại: {state.chat.conversations.length}</span>
            </div>
          </div>
        </div>

        {/* System Information */}
        <div className="card p-6">
          <div className="flex items-center gap-3 mb-4">
            <Info className="w-6 h-6 text-gray-600" />
            <h2 className="text-lg font-semibold text-gray-900">Thông tin Hệ thống</h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Frontend</h3>
              <div className="text-sm text-gray-600 space-y-1">
                <div>Framework: React + TypeScript</div>
                <div>Styling: Tailwind CSS</div>
                <div>Routing: React Router</div>
                <div>State: Context API</div>
              </div>
            </div>

            <div>
              <h3 className="text-sm font-medium text-gray-700 mb-2">Backend</h3>
              <div className="text-sm text-gray-600 space-y-1">
                <div>API: FastAPI</div>
                <div>LLM: Google Generative AI</div>
                <div>Vector DB: ChromaDB</div>
                <div>Framework: LangChain</div>
              </div>
            </div>
          </div>

          <div className="mt-6 p-4 bg-blue-50 rounded-lg">
            <h4 className="text-sm font-medium text-blue-900 mb-2">Hướng dẫn sử dụng</h4>
            <div className="text-sm text-blue-800 space-y-1">
              <div>1. Thêm tài liệu vào knowledge base qua trang "Tài liệu"</div>
              <div>2. Bắt đầu trò chuyện với chatbot qua trang "Chat"</div>
              <div>3. Chatbot sẽ trả lời dựa trên thông tin từ tài liệu đã thêm</div>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default SettingsPage 
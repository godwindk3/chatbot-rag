import axios, { AxiosInstance, AxiosResponse } from 'axios'
import {
  ChatRequest,
  ChatResponse,
  ConversationHistory,
  DocumentUploadRequest,
  WebDocumentRequest,
  DocumentResponse,
  DocumentListResponse,
  DocumentInfo,
  VectorStoreStatus,
  HealthResponse,
  ApiInfo,
  ChatStats,
  DocumentStats,
  ApiError,
} from '@/types'

class ApiService {
  private api: AxiosInstance

  constructor() {
    this.api = axios.create({
      baseURL: import.meta.env.VITE_API_BASE_URL || '/api/v1',
      timeout: 30000,
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Request interceptor
    this.api.interceptors.request.use(
      (config) => {
        // You can add auth headers here if needed
        return config
      },
      (error) => Promise.reject(error)
    )

    // Response interceptor
    this.api.interceptors.response.use(
      (response: AxiosResponse) => response,
      (error) => {
        const apiError: ApiError = {
          error: error.response?.data?.detail || error.message || 'An error occurred',
          detail: error.response?.data?.detail,
          code: error.response?.status?.toString(),
        }
        return Promise.reject(apiError)
      }
    )
  }

  // Health and Info endpoints
  async getHealth(): Promise<HealthResponse> {
    const response = await axios.get('/health')
    return response.data
  }

  async getApiInfo(): Promise<ApiInfo> {
    const response = await this.api.get('/info')
    return response.data
  }

  // Chat endpoints
  async sendMessage(request: ChatRequest): Promise<ChatResponse> {
    const response = await this.api.post('/chat/', request)
    return response.data
  }

  async getConversations(): Promise<ConversationHistory[]> {
    const response = await this.api.get('/chat/conversations')
    return response.data
  }

  async getConversation(conversationId: string): Promise<ConversationHistory> {
    const response = await this.api.get(`/chat/conversations/${conversationId}`)
    return response.data
  }

  async deleteConversation(conversationId: string): Promise<{ status: string; message: string }> {
    const response = await this.api.delete(`/chat/conversations/${conversationId}`)
    return response.data
  }

  async clearConversations(): Promise<{ status: string; message: string }> {
    const response = await this.api.delete('/chat/conversations')
    return response.data
  }

  async getChatStats(): Promise<ChatStats> {
    const response = await this.api.get('/chat/stats')
    return response.data
  }

  // Document endpoints
  async addTextDocument(request: DocumentUploadRequest): Promise<DocumentResponse> {
    const response = await this.api.post('/documents/text', request)
    return response.data
  }

  async addWebDocument(request: WebDocumentRequest): Promise<DocumentResponse> {
    const response = await this.api.post('/documents/web', request)
    return response.data
  }

  async getDocuments(): Promise<DocumentListResponse> {
    const response = await this.api.get('/documents/')
    return response.data
  }

  async getDocument(docId: string): Promise<DocumentInfo> {
    const response = await this.api.get(`/documents/${docId}`)
    return response.data
  }

  async deleteDocument(docId: string): Promise<{ status: string; message: string }> {
    const response = await this.api.delete(`/documents/${docId}`)
    return response.data
  }

  async getDocumentStats(): Promise<DocumentStats> {
    const response = await this.api.get('/documents/stats/overview')
    return response.data
  }

  async getVectorStoreStatus(): Promise<VectorStoreStatus> {
    const response = await this.api.get('/documents/vectorstore/status')
    return response.data
  }

  async clearVectorStore(): Promise<{ status: string; message: string }> {
    const response = await this.api.delete('/documents/vectorstore/clear')
    return response.data
  }
}

// Create singleton instance
export const apiService = new ApiService()
export default apiService 
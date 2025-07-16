// Chat Types
export interface ChatMessage {
  role: 'user' | 'assistant'
  content: string
  timestamp?: string
}

export interface ChatRequest {
  message: string
  conversation_id?: string
  include_sources?: boolean
}

export interface SourceDocument {
  content: string
  source?: string
  score?: number
  metadata?: Record<string, any>
}

export interface ChatResponse {
  message: string
  conversation_id: string
  sources?: SourceDocument[]
  processing_time?: number
  timestamp: string
}

export interface ConversationHistory {
  conversation_id: string
  messages: ChatMessage[]
  created_at: string
  updated_at: string
}

// Document Types
export type DocumentType = 'text' | 'pdf' | 'web' | 'markdown'
export type DocumentStatus = 'pending' | 'processing' | 'completed' | 'failed'

export interface DocumentUploadRequest {
  content: string
  title?: string
  source?: string
  doc_type?: DocumentType
  metadata?: Record<string, any>
}

export interface WebDocumentRequest {
  url: string
  title?: string
  metadata?: Record<string, any>
}

export interface DocumentInfo {
  doc_id: string
  title?: string
  source?: string
  doc_type: DocumentType
  status: DocumentStatus
  chunk_count?: number
  created_at: string
  updated_at: string
  metadata?: Record<string, any>
}

export interface DocumentResponse {
  doc_id: string
  message: string
  status: DocumentStatus
}

export interface DocumentListResponse {
  documents: DocumentInfo[]
  total: number
}

export interface VectorStoreStatus {
  total_documents: number
  total_chunks: number
  last_updated?: string
}

// API Response Types
export interface ApiResponse<T = any> {
  data?: T
  error?: string
  detail?: string
  code?: string
}

export interface HealthResponse {
  status: string
  app_name: string
  version: string
  debug: boolean
}

export interface ApiInfo {
  app_name: string
  version: string
  description: string
  endpoints: Record<string, string>
  models: {
    llm: string
    embedding: string
  }
  configuration: {
    chunk_size: number
    chunk_overlap: number
    max_retrieval_docs: number
    temperature: number
  }
}

// Error Types
export interface ApiError {
  error: string
  detail?: string
  code?: string
}

// Stats Types
export interface ChatStats {
  total_conversations: number
  total_messages: number
  average_messages_per_conversation: number
}

export interface DocumentStats {
  total_documents: number
  by_status: Record<DocumentStatus, number>
  by_type: Record<DocumentType, number>
} 
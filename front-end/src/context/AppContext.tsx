import React, { createContext, useContext, useReducer, useEffect, ReactNode } from 'react'
import { toast } from 'react-hot-toast'
import {
  AppState,
  ChatState,
  DocumentState,
  LoadingState,
  ApiInfo,
  ConversationHistory,
  ChatMessage,
  DocumentInfo,
  VectorStoreStatus,
  DocumentStats,
  // ChatStats, // Not used yet
} from '@/types'
import { apiService } from '@/services/api'

// Initial States
const initialLoadingState: LoadingState = {
  isLoading: false,
  error: undefined,
}

const initialAppState: AppState = {
  isConnected: false,
  apiInfo: undefined,
  loading: initialLoadingState,
}

const initialChatState: ChatState = {
  currentConversation: undefined,
  conversations: [],
  messages: [],
  isTyping: false,
  loading: initialLoadingState,
}

const initialDocumentState: DocumentState = {
  documents: [],
  vectorStoreStatus: undefined,
  stats: undefined,
  loading: initialLoadingState,
}

// Combined State
interface GlobalState {
  app: AppState
  chat: ChatState
  documents: DocumentState
}

const initialState: GlobalState = {
  app: initialAppState,
  chat: initialChatState,
  documents: initialDocumentState,
}

// Action Types
type AppAction = 
  | { type: 'SET_LOADING'; payload: { section: keyof GlobalState; loading: Partial<LoadingState> } }
  | { type: 'SET_API_INFO'; payload: ApiInfo }
  | { type: 'SET_CONNECTION_STATUS'; payload: boolean }
  | { type: 'SET_CONVERSATIONS'; payload: ConversationHistory[] }
  | { type: 'SET_CURRENT_CONVERSATION'; payload: string | undefined }
  | { type: 'SET_MESSAGES'; payload: ChatMessage[] }
  | { type: 'ADD_MESSAGE'; payload: ChatMessage }
  | { type: 'SET_TYPING'; payload: boolean }
  | { type: 'SET_DOCUMENTS'; payload: DocumentInfo[] }
  | { type: 'ADD_DOCUMENT'; payload: DocumentInfo }
  | { type: 'REMOVE_DOCUMENT'; payload: string }
  | { type: 'UPDATE_DOCUMENT'; payload: DocumentInfo }
  | { type: 'SET_VECTOR_STORE_STATUS'; payload: VectorStoreStatus }
  | { type: 'SET_DOCUMENT_STATS'; payload: DocumentStats }

// Reducer
function appReducer(state: GlobalState, action: AppAction): GlobalState {
  switch (action.type) {
    case 'SET_LOADING':
      return {
        ...state,
        [action.payload.section]: {
          ...state[action.payload.section],
          loading: {
            ...state[action.payload.section].loading,
            ...action.payload.loading,
          },
        },
      }

    case 'SET_API_INFO':
      return {
        ...state,
        app: {
          ...state.app,
          apiInfo: action.payload,
        },
      }

    case 'SET_CONNECTION_STATUS':
      return {
        ...state,
        app: {
          ...state.app,
          isConnected: action.payload,
        },
      }

    case 'SET_CONVERSATIONS':
      return {
        ...state,
        chat: {
          ...state.chat,
          conversations: action.payload,
        },
      }

    case 'SET_CURRENT_CONVERSATION':
      return {
        ...state,
        chat: {
          ...state.chat,
          currentConversation: action.payload,
        },
      }

    case 'SET_MESSAGES':
      return {
        ...state,
        chat: {
          ...state.chat,
          messages: action.payload,
        },
      }

    case 'ADD_MESSAGE':
      return {
        ...state,
        chat: {
          ...state.chat,
          messages: [...state.chat.messages, action.payload],
        },
      }

    case 'SET_TYPING':
      return {
        ...state,
        chat: {
          ...state.chat,
          isTyping: action.payload,
        },
      }

    case 'SET_DOCUMENTS':
      return {
        ...state,
        documents: {
          ...state.documents,
          documents: action.payload,
        },
      }

    case 'ADD_DOCUMENT':
      return {
        ...state,
        documents: {
          ...state.documents,
          documents: [...state.documents.documents, action.payload],
        },
      }

    case 'REMOVE_DOCUMENT':
      return {
        ...state,
        documents: {
          ...state.documents,
          documents: state.documents.documents.filter(doc => doc.doc_id !== action.payload),
        },
      }

    case 'UPDATE_DOCUMENT':
      return {
        ...state,
        documents: {
          ...state.documents,
          documents: state.documents.documents.map(doc =>
            doc.doc_id === action.payload.doc_id ? action.payload : doc
          ),
        },
      }

    case 'SET_VECTOR_STORE_STATUS':
      return {
        ...state,
        documents: {
          ...state.documents,
          vectorStoreStatus: action.payload,
        },
      }

    case 'SET_DOCUMENT_STATS':
      return {
        ...state,
        documents: {
          ...state.documents,
          stats: action.payload,
        },
      }

    default:
      return state
  }
}

// Context
interface AppContextType {
  state: GlobalState
  dispatch: React.Dispatch<AppAction>
  actions: {
    // App actions
    checkConnection: () => Promise<void>
    fetchApiInfo: () => Promise<void>
    
    // Chat actions
    sendMessage: (message: string, conversationId?: string) => Promise<void>
    fetchConversations: () => Promise<void>
    loadConversation: (conversationId: string) => Promise<void>
    deleteConversation: (conversationId: string) => Promise<void>
    clearAllConversations: () => Promise<void>
    
    // Document actions
    fetchDocuments: () => Promise<void>
    addTextDocument: (content: string, title?: string, metadata?: Record<string, any>) => Promise<void>
    addWebDocument: (url: string, title?: string, metadata?: Record<string, any>) => Promise<void>
    deleteDocument: (docId: string) => Promise<void>
    fetchVectorStoreStatus: () => Promise<void>
    fetchDocumentStats: () => Promise<void>
    clearVectorStore: () => Promise<void>
  }
}

const AppContext = createContext<AppContextType | undefined>(undefined)

// Provider
interface AppProviderProps {
  children: ReactNode
}

export function AppProvider({ children }: AppProviderProps) {
  const [state, dispatch] = useReducer(appReducer, initialState)

  // Helper function to handle loading states
  const withLoading = async <T,>(
    section: keyof GlobalState,
    asyncFn: () => Promise<T>
  ): Promise<T | undefined> => {
    try {
      dispatch({ type: 'SET_LOADING', payload: { section, loading: { isLoading: true, error: undefined } } })
      const result = await asyncFn()
      dispatch({ type: 'SET_LOADING', payload: { section, loading: { isLoading: false } } })
      return result
    } catch (error: any) {
      dispatch({ 
        type: 'SET_LOADING', 
        payload: { section, loading: { isLoading: false, error: error.error || error.message } }
      })
      toast.error(error.error || error.message || 'An error occurred')
      throw error
    }
  }

  // App Actions
  const checkConnection = async () => {
    try {
      await apiService.getHealth()
      dispatch({ type: 'SET_CONNECTION_STATUS', payload: true })
    } catch (error) {
      dispatch({ type: 'SET_CONNECTION_STATUS', payload: false })
    }
  }

  const fetchApiInfo = async () => {
    await withLoading('app', async () => {
      const info = await apiService.getApiInfo()
      dispatch({ type: 'SET_API_INFO', payload: info })
    })
  }

  // Chat Actions
  const sendMessage = async (message: string, conversationId?: string) => {
    // Add user message immediately
    const userMessage: ChatMessage = {
      role: 'user',
      content: message,
      timestamp: new Date().toISOString(),
    }
    dispatch({ type: 'ADD_MESSAGE', payload: userMessage })
    dispatch({ type: 'SET_TYPING', payload: true })

    await withLoading('chat', async () => {
      const response = await apiService.sendMessage({
        message,
        conversation_id: conversationId,
        include_sources: true,
      })

      // Add assistant message
      const assistantMessage: ChatMessage = {
        role: 'assistant',
        content: response.message,
        timestamp: response.timestamp,
      }
      dispatch({ type: 'ADD_MESSAGE', payload: assistantMessage })
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: response.conversation_id })
      dispatch({ type: 'SET_TYPING', payload: false })
    })
  }

  const fetchConversations = async () => {
    await withLoading('chat', async () => {
      const conversations = await apiService.getConversations()
      dispatch({ type: 'SET_CONVERSATIONS', payload: conversations })
    })
  }

  const loadConversation = async (conversationId: string) => {
    await withLoading('chat', async () => {
      const conversation = await apiService.getConversation(conversationId)
      dispatch({ type: 'SET_MESSAGES', payload: conversation.messages })
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: conversationId })
    })
  }

  const deleteConversation = async (conversationId: string) => {
    await withLoading('chat', async () => {
      await apiService.deleteConversation(conversationId)
      // Refresh conversations list
      await fetchConversations()
      
      // Clear current conversation if it was deleted
      if (state.chat.currentConversation === conversationId) {
        dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: undefined })
        dispatch({ type: 'SET_MESSAGES', payload: [] })
      }
      toast.success('Conversation deleted')
    })
  }

  const clearAllConversations = async () => {
    await withLoading('chat', async () => {
      await apiService.clearConversations()
      dispatch({ type: 'SET_CONVERSATIONS', payload: [] })
      dispatch({ type: 'SET_CURRENT_CONVERSATION', payload: undefined })
      dispatch({ type: 'SET_MESSAGES', payload: [] })
      toast.success('All conversations cleared')
    })
  }

  // Document Actions
  const fetchDocuments = async () => {
    await withLoading('documents', async () => {
      const response = await apiService.getDocuments()
      dispatch({ type: 'SET_DOCUMENTS', payload: response.documents })
    })
  }

  const addTextDocument = async (content: string, title?: string, metadata?: Record<string, any>) => {
    await withLoading('documents', async () => {
      await apiService.addTextDocument({
        content,
        title,
        metadata,
      })
      toast.success('Document added successfully')
      // Refresh documents list
      await fetchDocuments()
    })
  }

  const addWebDocument = async (url: string, title?: string, metadata?: Record<string, any>) => {
    await withLoading('documents', async () => {
      await apiService.addWebDocument({
        url,
        title,
        metadata,
      })
      toast.success('Web document added successfully')
      // Refresh documents list
      await fetchDocuments()
    })
  }

  const deleteDocument = async (docId: string) => {
    await withLoading('documents', async () => {
      await apiService.deleteDocument(docId)
      dispatch({ type: 'REMOVE_DOCUMENT', payload: docId })
      toast.success('Document deleted')
    })
  }

  const fetchVectorStoreStatus = async () => {
    await withLoading('documents', async () => {
      const status = await apiService.getVectorStoreStatus()
      dispatch({ type: 'SET_VECTOR_STORE_STATUS', payload: status })
    })
  }

  const fetchDocumentStats = async () => {
    await withLoading('documents', async () => {
      const stats = await apiService.getDocumentStats()
      dispatch({ type: 'SET_DOCUMENT_STATS', payload: stats })
    })
  }

  const clearVectorStore = async () => {
    await withLoading('documents', async () => {
      await apiService.clearVectorStore()
      dispatch({ type: 'SET_DOCUMENTS', payload: [] })
      dispatch({ type: 'SET_VECTOR_STORE_STATUS', payload: { total_documents: 0, total_chunks: 0 } })
      toast.success('Vector store cleared')
    })
  }

  // Initialize on mount
  useEffect(() => {
    checkConnection()
    fetchApiInfo()
    fetchDocuments()
    fetchVectorStoreStatus()
  }, [])

  const actions = {
    checkConnection,
    fetchApiInfo,
    sendMessage,
    fetchConversations,
    loadConversation,
    deleteConversation,
    clearAllConversations,
    fetchDocuments,
    addTextDocument,
    addWebDocument,
    deleteDocument,
    fetchVectorStoreStatus,
    fetchDocumentStats,
    clearVectorStore,
  }

  return (
    <AppContext.Provider value={{ state, dispatch, actions }}>
      {children}
    </AppContext.Provider>
  )
}

// Hook
export function useApp() {
  const context = useContext(AppContext)
  if (context === undefined) {
    throw new Error('useApp must be used within an AppProvider')
  }
  return context
} 
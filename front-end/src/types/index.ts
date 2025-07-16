export * from './api'

// UI State Types
export interface LoadingState {
  isLoading: boolean
  error?: string
}

export interface AppState {
  isConnected: boolean
  apiInfo?: import('./api').ApiInfo
  loading: LoadingState
}

export interface ChatState {
  currentConversation?: string
  conversations: import('./api').ConversationHistory[]
  messages: import('./api').ChatMessage[]
  isTyping: boolean
  loading: LoadingState
}

export interface DocumentState {
  documents: import('./api').DocumentInfo[]
  vectorStoreStatus?: import('./api').VectorStoreStatus
  stats?: import('./api').DocumentStats
  loading: LoadingState
}

// Component Props Types
export interface BaseComponentProps {
  className?: string
  children?: React.ReactNode
}

export interface ButtonProps extends BaseComponentProps {
  variant?: 'primary' | 'secondary' | 'danger' | 'ghost'
  size?: 'sm' | 'md' | 'lg'
  disabled?: boolean
  loading?: boolean
  onClick?: () => void
  type?: 'button' | 'submit' | 'reset'
  title?: string
}

export interface InputProps extends BaseComponentProps {
  type?: string
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  disabled?: boolean
  error?: string
}

export interface ModalProps extends BaseComponentProps {
  isOpen: boolean
  onClose: () => void
  title?: string
  size?: 'sm' | 'md' | 'lg' | 'xl'
}

// Navigation Types
export type Route = {
  path: string
  name: string
  icon?: React.ComponentType<any>
  component: React.ComponentType<any>
}

// Theme Types
export type Theme = 'light' | 'dark'

// Utility Types
export type Optional<T, K extends keyof T> = Omit<T, K> & Partial<Pick<T, K>>
export type RequiredFields<T, K extends keyof T> = T & Required<Pick<T, K>>

// Form Types
export interface FormField {
  name: string
  label: string
  type: 'text' | 'textarea' | 'url' | 'file' | 'select'
  required?: boolean
  placeholder?: string
  options?: { value: string; label: string }[]
  validation?: (value: any) => string | undefined
}

export interface FormState {
  values: Record<string, any>
  errors: Record<string, string>
  touched: Record<string, boolean>
  isSubmitting: boolean
} 
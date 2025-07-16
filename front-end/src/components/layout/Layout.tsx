import React from 'react'
import { Link, useLocation } from 'react-router-dom'
import { MessageSquare, FileText, Settings, Bot, Wifi, WifiOff } from 'lucide-react'
import { clsx } from 'clsx'
import { useApp } from '@/context/AppContext'

interface LayoutProps {
  children: React.ReactNode
}

const Layout: React.FC<LayoutProps> = ({ children }) => {
  const location = useLocation()
  const { state } = useApp()

  const navigation = [
    {
      name: 'Chat',
      href: '/chat',
      icon: MessageSquare,
      current: location.pathname === '/' || location.pathname === '/chat',
    },
    {
      name: 'Tài liệu',
      href: '/documents',
      icon: FileText,
      current: location.pathname === '/documents',
    },
    {
      name: 'Cài đặt',
      href: '/settings',
      icon: Settings,
      current: location.pathname === '/settings',
    },
  ]

  return (
    <div className="flex h-screen bg-gray-100">
      {/* Sidebar */}
      <div className="flex flex-col w-64 bg-white shadow-sm">
        {/* Logo */}
        <div className="flex items-center gap-3 px-6 py-4 border-b border-gray-200">
          <div className="w-8 h-8 bg-primary-600 rounded-lg flex items-center justify-center">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">RAG Chatbot</h1>
            <p className="text-xs text-gray-500">
              {state.app.apiInfo?.version || 'v1.0.0'}
            </p>
          </div>
        </div>

        {/* Navigation */}
        <nav className="flex-1 px-4 py-4 space-y-2">
          {navigation.map((item) => {
            const Icon = item.icon
            return (
              <Link
                key={item.name}
                to={item.href}
                className={clsx(
                  'flex items-center gap-3 px-3 py-2 rounded-lg text-sm font-medium transition-colors duration-200',
                  item.current
                    ? 'bg-primary-50 text-primary-700 border border-primary-200'
                    : 'text-gray-600 hover:bg-gray-50 hover:text-gray-900'
                )}
              >
                <Icon className="w-5 h-5" />
                {item.name}
              </Link>
            )
          })}
        </nav>

        {/* Connection status */}
        <div className="px-4 py-3 border-t border-gray-200">
          <div className="flex items-center gap-3">
            {state.app.isConnected ? (
              <>
                <Wifi className="w-4 h-4 text-green-600" />
                <span className="text-sm text-green-600">Đã kết nối</span>
              </>
            ) : (
              <>
                <WifiOff className="w-4 h-4 text-red-600" />
                <span className="text-sm text-red-600">Mất kết nối</span>
              </>
            )}
          </div>
          
          {state.app.apiInfo && (
            <div className="mt-2 text-xs text-gray-500">
              <div>Model: {state.app.apiInfo.models.llm}</div>
              <div>Embeddings: {state.app.apiInfo.models.embedding}</div>
            </div>
          )}
        </div>
      </div>

      {/* Main content */}
      <div className="flex-1 flex flex-col overflow-hidden">
        {/* Top bar */}
        <div className="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-3">
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-xl font-semibold text-gray-900">
                {navigation.find(item => item.current)?.name || 'RAG Chatbot'}
              </h2>
            </div>
            
            {/* Quick stats */}
            {state.documents.vectorStoreStatus && (
              <div className="flex items-center gap-6 text-sm text-gray-600">
                <div className="flex items-center gap-2">
                  <FileText className="w-4 h-4" />
                  <span>{state.documents.vectorStoreStatus.total_documents} docs</span>
                </div>
                <div className="flex items-center gap-2">
                  <span className="w-2 h-2 bg-primary-600 rounded-full"></span>
                  <span>{state.documents.vectorStoreStatus.total_chunks} chunks</span>
                </div>
              </div>
            )}
          </div>
        </div>

        {/* Page content */}
        <div className="flex-1 overflow-hidden">
          {children}
        </div>
      </div>
    </div>
  )
}

export default Layout 
import React, { useEffect, useRef } from 'react'
import { useApp } from '@/context/AppContext'
import ChatMessage from './ChatMessage'
import ChatInput from './ChatInput'
import TypingIndicator from './TypingIndicator'
import { Loading } from '@/components/ui'
import { MessageSquare } from 'lucide-react'

const ChatInterface: React.FC = () => {
  const { state, actions } = useApp()
  const { messages, isTyping, loading } = state.chat
  const messagesEndRef = useRef<HTMLDivElement>(null)

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }

  useEffect(() => {
    scrollToBottom()
  }, [messages, isTyping])

  const handleSendMessage = async (message: string) => {
    try {
      await actions.sendMessage(message, state.chat.currentConversation)
    } catch (error) {
      console.error('Failed to send message:', error)
    }
  }

  const isLoading = loading.isLoading

  return (
    <div className="flex flex-col h-full bg-gray-50">
      {/* Chat header */}
      <div className="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-primary-100 rounded-full flex items-center justify-center">
            <MessageSquare className="w-6 h-6 text-primary-600" />
          </div>
          <div>
            <h1 className="text-lg font-semibold text-gray-900">RAG Chatbot</h1>
            <p className="text-sm text-gray-500">
              {state.app.isConnected ? 'Đã kết nối' : 'Mất kết nối'}
            </p>
          </div>
        </div>
      </div>

      {/* Chat messages */}
      <div className="flex-1 overflow-y-auto p-6 space-y-4">
        {loading.isLoading && messages.length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <Loading size="lg" text="Đang tải cuộc trò chuyện..." />
          </div>
        ) : messages.length === 0 ? (
          // Welcome message
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <div className="w-16 h-16 bg-primary-100 rounded-full flex items-center justify-center mx-auto mb-4">
                <MessageSquare className="w-8 h-8 text-primary-600" />
              </div>
              <h2 className="text-xl font-semibold text-gray-900 mb-2">
                Chào mừng đến với RAG Chatbot!
              </h2>
              <p className="text-gray-600 max-w-md">
                Hãy bắt đầu cuộc trò chuyện bằng cách đặt câu hỏi. 
                Tôi có thể trả lời dựa trên thông tin từ tài liệu đã được thêm vào hệ thống.
              </p>
            </div>
          </div>
        ) : (
          // Messages
          <>
            {messages.map((message, index) => (
              <ChatMessage
                key={`${message.timestamp}-${index}`}
                message={message}
                showTimestamp={true}
              />
            ))}
            
            {/* Typing indicator */}
            {isTyping && <TypingIndicator />}
            
            {/* Scroll anchor */}
            <div ref={messagesEndRef} />
          </>
        )}

        {/* Error state */}
        {loading.error && (
          <div className="bg-red-50 border border-red-200 rounded-lg p-4 mx-4">
            <div className="flex">
              <div className="flex-shrink-0">
                <svg className="h-5 w-5 text-red-400" viewBox="0 0 20 20" fill="currentColor">
                  <path fillRule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clipRule="evenodd" />
                </svg>
              </div>
              <div className="ml-3">
                <h3 className="text-sm font-medium text-red-800">
                  Có lỗi xảy ra
                </h3>
                <div className="mt-2 text-sm text-red-700">
                  <p>{loading.error}</p>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>

      {/* Chat input */}
      <div className="flex-shrink-0">
        <ChatInput
          onSendMessage={handleSendMessage}
          disabled={!state.app.isConnected || isLoading}
          loading={isTyping}
          placeholder="Hỏi bất cứ điều gì về tài liệu..."
        />
      </div>
    </div>
  )
}

export default ChatInterface 
import React, { useState, useRef, useEffect } from 'react'
import { Send, StopCircle } from 'lucide-react'
import { Button } from '@/components/ui'
import { clsx } from 'clsx'

interface ChatInputProps {
  onSendMessage: (message: string) => void
  disabled?: boolean
  loading?: boolean
  placeholder?: string
}

const ChatInput: React.FC<ChatInputProps> = ({
  onSendMessage,
  disabled = false,
  loading = false,
  placeholder = "Nhập tin nhắn của bạn...",
}) => {
  const [message, setMessage] = useState('')
  const textareaRef = useRef<HTMLTextAreaElement>(null)

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (message.trim() && !disabled && !loading) {
      onSendMessage(message.trim())
      setMessage('')
      if (textareaRef.current) {
        textareaRef.current.style.height = 'auto'
      }
    }
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSubmit(e)
    }
  }

  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    setMessage(e.target.value)
    
    // Auto-resize textarea
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto'
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 150)}px`
    }
  }

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.focus()
    }
  }, [])

  const isDisabled = disabled || loading
  const canSend = message.trim().length > 0 && !isDisabled

  return (
    <div className="border-t border-gray-200 bg-white p-4">
      <form onSubmit={handleSubmit} className="flex gap-2">
        <div className="flex-1 relative">
          <textarea
            ref={textareaRef}
            value={message}
            onChange={handleChange}
            onKeyDown={handleKeyDown}
            placeholder={placeholder}
            disabled={isDisabled}
            rows={1}
            className={clsx(
              'w-full px-4 py-3 pr-12 border border-gray-300 rounded-lg resize-none',
              'focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-transparent',
              'placeholder-gray-500 text-gray-900',
              'transition-all duration-200',
              {
                'opacity-50 cursor-not-allowed': isDisabled,
                'max-h-[150px] overflow-y-auto': true,
              }
            )}
            style={{ minHeight: '48px' }}
          />
          
          {/* Character count */}
          {message.length > 1500 && (
            <div className="absolute bottom-2 right-14 text-xs text-gray-500">
              {message.length}/2000
            </div>
          )}
        </div>

        <Button
          type="submit"
          disabled={!canSend}
          loading={loading}
          className="px-4 py-3 h-12"
          title={loading ? "Đang gửi..." : "Gửi tin nhắn (Enter)"}
        >
          {loading ? (
            <StopCircle className="w-5 h-5" />
          ) : (
            <Send className="w-5 h-5" />
          )}
        </Button>
      </form>

      {/* Help text */}
      <div className="mt-2 text-xs text-gray-500 flex justify-between">
        <span>Nhấn Enter để gửi, Shift+Enter để xuống dòng</span>
        <span>{message.length}/2000</span>
      </div>
    </div>
  )
}

export default ChatInput 
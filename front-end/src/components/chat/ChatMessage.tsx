import React from 'react'
import { ChatMessage as ChatMessageType } from '@/types'
import { clsx } from 'clsx'
import { User, Bot, Copy, Check } from 'lucide-react'
import { format } from 'date-fns'
import ReactMarkdown from 'react-markdown'
import { Button } from '@/components/ui'
import { useState } from 'react'

interface ChatMessageProps {
  message: ChatMessageType
  showTimestamp?: boolean
}

const ChatMessage: React.FC<ChatMessageProps> = ({
  message,
  showTimestamp = true,
}) => {
  const [copied, setCopied] = useState(false)
  const isUser = message.role === 'user'

  const handleCopy = async () => {
    try {
      await navigator.clipboard.writeText(message.content)
      setCopied(true)
      setTimeout(() => setCopied(false), 2000)
    } catch (error) {
      console.error('Failed to copy text:', error)
    }
  }

  const messageClasses = clsx(
    'max-w-xs sm:max-w-md lg:max-w-lg xl:max-w-xl',
    'px-4 py-3 rounded-lg shadow-sm',
    'relative group',
    {
      'message-user': isUser,
      'message-assistant': !isUser,
    }
  )

  const containerClasses = clsx(
    'flex gap-3 mb-4',
    {
      'justify-end': isUser,
      'justify-start': !isUser,
    }
  )

  return (
    <div className={containerClasses}>
      {/* Avatar */}
      {!isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
          <Bot className="w-5 h-5 text-primary-600" />
        </div>
      )}

      <div className="flex flex-col gap-1">
        {/* Message bubble */}
        <div className={messageClasses}>
          <div className="flex items-start justify-between gap-2">
            <div className="flex-1 min-w-0">
              {isUser ? (
                <p className="text-white whitespace-pre-wrap break-words">
                  {message.content}
                </p>
              ) : (
                <div className="prose prose-sm max-w-none">
                  <ReactMarkdown
                    components={{
                      p: ({ children }) => <p className="mb-2 last:mb-0">{children}</p>,
                      code: ({ children, className }) => {
                        const isInline = !className
                        return isInline ? (
                          <code className="bg-gray-100 px-1 py-0.5 rounded text-sm font-mono">
                            {children}
                          </code>
                        ) : (
                          <pre className="bg-gray-100 p-3 rounded-lg overflow-x-auto">
                            <code className="text-sm font-mono">{children}</code>
                          </pre>
                        )
                      },
                    }}
                  >
                    {message.content}
                  </ReactMarkdown>
                </div>
              )}
            </div>

            {/* Copy button */}
            <Button
              variant="ghost"
              size="sm"
              onClick={handleCopy}
              className={clsx(
                'opacity-0 group-hover:opacity-100 transition-opacity p-1 h-auto',
                isUser ? 'text-white hover:bg-white/20' : 'text-gray-500 hover:bg-gray-100'
              )}
            >
              {copied ? (
                <Check className="w-4 h-4" />
              ) : (
                <Copy className="w-4 h-4" />
              )}
            </Button>
          </div>
        </div>

        {/* Timestamp */}
        {showTimestamp && message.timestamp && (
          <div className={clsx(
            'text-xs text-gray-500 px-2',
            isUser ? 'text-right' : 'text-left'
          )}>
            {format(new Date(message.timestamp), 'HH:mm')}
          </div>
        )}
      </div>

      {/* User avatar */}
      {isUser && (
        <div className="flex-shrink-0 w-8 h-8 bg-primary-600 rounded-full flex items-center justify-center">
          <User className="w-5 h-5 text-white" />
        </div>
      )}
    </div>
  )
}

export default ChatMessage 
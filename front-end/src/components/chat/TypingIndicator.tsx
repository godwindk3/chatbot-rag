import React from 'react'
import { Bot } from 'lucide-react'

const TypingIndicator: React.FC = () => {
  return (
    <div className="flex gap-3 mb-4">
      {/* Bot avatar */}
      <div className="flex-shrink-0 w-8 h-8 bg-primary-100 rounded-full flex items-center justify-center">
        <Bot className="w-5 h-5 text-primary-600" />
      </div>

      {/* Typing indicator */}
      <div className="bg-white border border-gray-200 px-4 py-3 rounded-lg shadow-sm max-w-xs">
        <div className="flex items-center gap-1">
          <div className="flex gap-1">
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" 
                 style={{ animationDelay: '0ms', animationDuration: '1.4s' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" 
                 style={{ animationDelay: '200ms', animationDuration: '1.4s' }} />
            <div className="w-2 h-2 bg-gray-400 rounded-full animate-pulse" 
                 style={{ animationDelay: '400ms', animationDuration: '1.4s' }} />
          </div>
          <span className="text-gray-500 text-sm ml-2">AI đang trả lời...</span>
        </div>
      </div>
    </div>
  )
}

export default TypingIndicator 
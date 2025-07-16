import React from 'react'
import { clsx } from 'clsx'
import { Loader2 } from 'lucide-react'

interface LoadingProps {
  size?: 'sm' | 'md' | 'lg'
  text?: string
  className?: string
}

const Loading: React.FC<LoadingProps> = ({
  size = 'md',
  text,
  className,
}) => {
  const sizeClasses = {
    sm: 'w-4 h-4',
    md: 'w-6 h-6',
    lg: 'w-8 h-8',
  }

  return (
    <div className={clsx('flex items-center justify-center gap-2', className)}>
      <Loader2 className={clsx('animate-spin text-primary-600', sizeClasses[size])} />
      {text && (
        <span className="text-gray-600 text-sm">{text}</span>
      )}
    </div>
  )
}

export default Loading 
import React from 'react'
import { clsx } from 'clsx'

interface TextareaProps {
  className?: string
  placeholder?: string
  value?: string
  onChange?: (value: string) => void
  disabled?: boolean
  error?: string
  rows?: number
  resize?: 'none' | 'vertical' | 'horizontal' | 'both'
}

const Textarea: React.FC<TextareaProps> = ({
  className,
  placeholder,
  value,
  onChange,
  disabled = false,
  error,
  rows = 4,
  resize = 'vertical',
  ...props
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLTextAreaElement>) => {
    if (onChange) {
      onChange(e.target.value)
    }
  }

  const resizeClasses = {
    none: 'resize-none',
    vertical: 'resize-y',
    horizontal: 'resize-x',
    both: 'resize',
  }

  const classes = clsx(
    'input',
    resizeClasses[resize],
    {
      'border-red-300 focus:ring-red-500 focus:border-red-500': error,
      'opacity-50 cursor-not-allowed': disabled,
    },
    className
  )

  return (
    <div className="w-full">
      <textarea
        className={classes}
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
        disabled={disabled}
        rows={rows}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}

export default Textarea 
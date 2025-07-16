import React from 'react'
import { InputProps } from '@/types'
import { clsx } from 'clsx'

const Input: React.FC<InputProps> = ({
  className,
  type = 'text',
  placeholder,
  value,
  onChange,
  disabled = false,
  error,
  ...props
}) => {
  const handleChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (onChange) {
      onChange(e.target.value)
    }
  }

  const classes = clsx(
    'input',
    {
      'border-red-300 focus:ring-red-500 focus:border-red-500': error,
      'opacity-50 cursor-not-allowed': disabled,
    },
    className
  )

  return (
    <div className="w-full">
      <input
        type={type}
        className={classes}
        placeholder={placeholder}
        value={value}
        onChange={handleChange}
        disabled={disabled}
        {...props}
      />
      {error && (
        <p className="mt-1 text-sm text-red-600">{error}</p>
      )}
    </div>
  )
}

export default Input 
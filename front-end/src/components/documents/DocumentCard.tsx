import React from 'react'
import { DocumentInfo, DocumentStatus, DocumentType } from '@/types'
import { Button } from '@/components/ui'
import { 
  FileText, 
  Globe, 
  File, 
  Trash2, 
  Clock, 
  CheckCircle, 
  XCircle, 
  Loader2 
} from 'lucide-react'
import { clsx } from 'clsx'
import { format } from 'date-fns'

interface DocumentCardProps {
  document: DocumentInfo
  onDelete?: (docId: string) => void
  loading?: boolean
}

const DocumentCard: React.FC<DocumentCardProps> = ({
  document,
  onDelete,
  loading = false,
}) => {
  const getDocumentIcon = (type: DocumentType) => {
    switch (type) {
      case 'web':
        return Globe
      case 'text':
        return FileText
      default:
        return File
    }
  }

  const getStatusIcon = (status: DocumentStatus) => {
    switch (status) {
      case 'completed':
        return CheckCircle
      case 'failed':
        return XCircle
      case 'processing':
        return Loader2
      default:
        return Clock
    }
  }

  const getStatusColor = (status: DocumentStatus) => {
    switch (status) {
      case 'completed':
        return 'text-green-600 bg-green-100'
      case 'failed':
        return 'text-red-600 bg-red-100'
      case 'processing':
        return 'text-blue-600 bg-blue-100'
      default:
        return 'text-yellow-600 bg-yellow-100'
    }
  }

  const IconComponent = getDocumentIcon(document.doc_type)
  const StatusIcon = getStatusIcon(document.status)

  const handleDelete = () => {
    if (onDelete && !loading) {
      onDelete(document.doc_id)
    }
  }

  return (
    <div className="card p-4 hover:shadow-md transition-shadow duration-200">
      <div className="flex items-start justify-between gap-3">
        {/* Document info */}
        <div className="flex items-start gap-3 flex-1 min-w-0">
          {/* Icon */}
          <div className="flex-shrink-0 w-10 h-10 bg-gray-100 rounded-lg flex items-center justify-center">
            <IconComponent className="w-5 h-5 text-gray-600" />
          </div>

          {/* Content */}
          <div className="flex-1 min-w-0">
            <h3 className="font-medium text-gray-900 truncate">
              {document.title || `Document ${document.doc_id.slice(0, 8)}`}
            </h3>
            
            {document.source && (
              <p className="text-sm text-gray-600 truncate mt-1">
                {document.source}
              </p>
            )}

            <div className="flex items-center gap-4 mt-2 text-xs text-gray-500">
              <span>
                Loại: {document.doc_type}
              </span>
              
              {document.chunk_count && (
                <span>
                  {document.chunk_count} chunks
                </span>
              )}

              <span>
                {format(new Date(document.created_at), 'dd/MM/yyyy HH:mm')}
              </span>
            </div>
          </div>
        </div>

        {/* Status and actions */}
        <div className="flex items-center gap-2 flex-shrink-0">
          {/* Status */}
          <div className={clsx(
            'inline-flex items-center gap-1 px-2 py-1 rounded-full text-xs font-medium',
            getStatusColor(document.status)
          )}>
            <StatusIcon className={clsx(
              'w-3 h-3',
              document.status === 'processing' && 'animate-spin'
            )} />
            <span className="capitalize">{document.status}</span>
          </div>

          {/* Delete button */}
          {document.status !== 'processing' && (
            <Button
              variant="ghost"
              size="sm"
              onClick={handleDelete}
              disabled={loading}
              className="p-1 text-gray-400 hover:text-red-600 hover:bg-red-50"
              title="Xóa tài liệu"
            >
              <Trash2 className="w-4 h-4" />
            </Button>
          )}
        </div>
      </div>

      {/* Metadata */}
      {document.metadata && Object.keys(document.metadata).length > 0 && (
        <div className="mt-3 pt-3 border-t border-gray-100">
          <div className="flex flex-wrap gap-2">
            {Object.entries(document.metadata).slice(0, 3).map(([key, value]) => (
              <span
                key={key}
                className="inline-flex items-center px-2 py-1 rounded-md bg-gray-100 text-xs text-gray-600"
              >
                <span className="font-medium">{key}:</span>
                <span className="ml-1 truncate max-w-20">{String(value)}</span>
              </span>
            ))}
            {Object.keys(document.metadata).length > 3 && (
              <span className="text-xs text-gray-500">
                +{Object.keys(document.metadata).length - 3} more
              </span>
            )}
          </div>
        </div>
      )}
    </div>
  )
}

export default DocumentCard 
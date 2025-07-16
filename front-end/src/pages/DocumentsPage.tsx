import React, { useState, useEffect } from 'react'
import { useApp } from '@/context/AppContext'
import DocumentCard from '@/components/documents/DocumentCard'
import { Button, Modal, Input, Textarea, Loading } from '@/components/ui'
import { Plus, FileText, Globe, Search, Trash2 } from 'lucide-react'

const DocumentsPage: React.FC = () => {
  const { state, actions } = useApp()
  const { documents, loading, vectorStoreStatus } = state.documents
  
  const [showAddModal, setShowAddModal] = useState(false)
  const [addType, setAddType] = useState<'text' | 'web'>('text')
  const [searchQuery, setSearchQuery] = useState('')
  
  // Form states
  const [textContent, setTextContent] = useState('')
  const [title, setTitle] = useState('')
  const [webUrl, setWebUrl] = useState('')
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    actions.fetchDocuments()
    actions.fetchVectorStoreStatus()
  }, [])

  const filteredDocuments = documents.filter(doc =>
    doc.title?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.source?.toLowerCase().includes(searchQuery.toLowerCase()) ||
    doc.doc_type.toLowerCase().includes(searchQuery.toLowerCase())
  )

  const handleAddDocument = async () => {
    if (submitting) return

    try {
      setSubmitting(true)
      
      if (addType === 'text') {
        if (!textContent.trim()) return
        await actions.addTextDocument(textContent, title || undefined)
      } else {
        if (!webUrl.trim()) return
        await actions.addWebDocument(webUrl, title || undefined)
      }
      
      // Reset form
      setTextContent('')
      setTitle('')
      setWebUrl('')
      setShowAddModal(false)
      
    } catch (error) {
      console.error('Failed to add document:', error)
    } finally {
      setSubmitting(false)
    }
  }

  const handleDeleteDocument = async (docId: string) => {
    if (window.confirm('Bạn có chắc chắn muốn xóa tài liệu này?')) {
      try {
        await actions.deleteDocument(docId)
      } catch (error) {
        console.error('Failed to delete document:', error)
      }
    }
  }

  const handleClearVectorStore = async () => {
    if (window.confirm('Bạn có chắc chắn muốn xóa toàn bộ vector store? Hành động này không thể hoàn tác.')) {
      try {
        await actions.clearVectorStore()
      } catch (error) {
        console.error('Failed to clear vector store:', error)
      }
    }
  }

  return (
    <div className="h-full flex flex-col bg-gray-50">
      {/* Header */}
      <div className="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-4">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-gray-900">Quản lý Tài liệu</h1>
            <p className="text-gray-600 mt-1">
              Thêm và quản lý tài liệu cho knowledge base
            </p>
          </div>
          
          <div className="flex items-center gap-3">
            {/* Clear vector store */}
            {documents.length > 0 && (
              <Button
                variant="danger"
                size="sm"
                onClick={handleClearVectorStore}
                className="flex items-center gap-2"
              >
                <Trash2 className="w-4 h-4" />
                Xóa toàn bộ
              </Button>
            )}
            
            {/* Add document */}
            <Button
              onClick={() => setShowAddModal(true)}
              className="flex items-center gap-2"
            >
              <Plus className="w-4 h-4" />
              Thêm tài liệu
            </Button>
          </div>
        </div>
      </div>

      {/* Stats */}
      {vectorStoreStatus && (
        <div className="flex-shrink-0 bg-white border-b border-gray-200 px-6 py-4">
          <div className="flex items-center gap-8 text-sm">
            <div className="flex items-center gap-2">
              <FileText className="w-4 h-4 text-primary-600" />
              <span className="font-medium">{vectorStoreStatus.total_documents}</span>
              <span className="text-gray-600">tài liệu</span>
            </div>
            <div className="flex items-center gap-2">
              <div className="w-2 h-2 bg-primary-600 rounded-full"></div>
              <span className="font-medium">{vectorStoreStatus.total_chunks}</span>
              <span className="text-gray-600">chunks</span>
            </div>
          </div>
        </div>
      )}

      {/* Search */}
      <div className="flex-shrink-0 px-6 py-4">
        <div className="relative max-w-md">
          <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-gray-400" />
          <Input
            placeholder="Tìm kiếm tài liệu..."
            value={searchQuery}
            onChange={setSearchQuery}
            className="pl-10"
          />
        </div>
      </div>

      {/* Content */}
      <div className="flex-1 overflow-y-auto px-6 pb-6">
        {loading.isLoading && documents.length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <Loading size="lg" text="Đang tải tài liệu..." />
          </div>
        ) : filteredDocuments.length === 0 ? (
          <div className="flex items-center justify-center h-64">
            <div className="text-center">
              <FileText className="w-16 h-16 text-gray-300 mx-auto mb-4" />
              <h3 className="text-lg font-medium text-gray-900 mb-2">
                {searchQuery ? 'Không tìm thấy tài liệu' : 'Chưa có tài liệu nào'}
              </h3>
              <p className="text-gray-600 mb-4">
                {searchQuery 
                  ? 'Thử tìm kiếm với từ khóa khác'
                  : 'Thêm tài liệu đầu tiên để bắt đầu xây dựng knowledge base'
                }
              </p>
              {!searchQuery && (
                <Button onClick={() => setShowAddModal(true)}>
                  Thêm tài liệu đầu tiên
                </Button>
              )}
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {filteredDocuments.map((document) => (
              <DocumentCard
                key={document.doc_id}
                document={document}
                onDelete={handleDeleteDocument}
                loading={loading.isLoading}
              />
            ))}
          </div>
        )}
      </div>

      {/* Add Document Modal */}
      <Modal
        isOpen={showAddModal}
        onClose={() => setShowAddModal(false)}
        title="Thêm tài liệu mới"
        size="lg"
      >
        <div className="space-y-4">
          {/* Type selector */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Loại tài liệu
            </label>
            <div className="flex gap-2">
              <Button
                variant={addType === 'text' ? 'primary' : 'secondary'}
                size="sm"
                onClick={() => setAddType('text')}
                className="flex items-center gap-2"
              >
                <FileText className="w-4 h-4" />
                Văn bản
              </Button>
              <Button
                variant={addType === 'web' ? 'primary' : 'secondary'}
                size="sm"
                onClick={() => setAddType('web')}
                className="flex items-center gap-2"
              >
                <Globe className="w-4 h-4" />
                Trang web
              </Button>
            </div>
          </div>

          {/* Title */}
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Tiêu đề (tùy chọn)
            </label>
            <Input
              placeholder="Nhập tiêu đề tài liệu..."
              value={title}
              onChange={setTitle}
            />
          </div>

          {/* Content */}
          {addType === 'text' ? (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Nội dung văn bản
              </label>
              <Textarea
                placeholder="Nhập nội dung tài liệu..."
                value={textContent}
                onChange={setTextContent}
                rows={10}
              />
            </div>
          ) : (
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                URL trang web
              </label>
              <Input
                type="url"
                placeholder="https://example.com"
                value={webUrl}
                onChange={setWebUrl}
              />
            </div>
          )}

          {/* Actions */}
          <div className="flex justify-end gap-3 pt-4">
            <Button
              variant="secondary"
              onClick={() => setShowAddModal(false)}
              disabled={submitting}
            >
              Hủy
            </Button>
            <Button
              onClick={handleAddDocument}
              loading={submitting}
              disabled={
                submitting ||
                (addType === 'text' && !textContent.trim()) ||
                (addType === 'web' && !webUrl.trim())
              }
            >
              Thêm tài liệu
            </Button>
          </div>
        </div>
      </Modal>
    </div>
  )
}

export default DocumentsPage 
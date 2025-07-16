# RAG Chatbot Frontend

Modern React TypeScript frontend for the RAG Chatbot API.

## 🚀 Tính năng

- **Chat Interface**: Giao diện chat thông minh với markdown support
- **Document Management**: Thêm và quản lý tài liệu (text/web)
- **Real-time Updates**: Cập nhật trạng thái real-time
- **Responsive Design**: Hoạt động tốt trên mọi thiết bị
- **Type Safety**: Full TypeScript support
- **Modern UI**: Clean design với Tailwind CSS

## 🛠️ Công nghệ

- **React 18** - UI Framework
- **TypeScript** - Type safety
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **React Router** - Navigation
- **Axios** - HTTP client
- **Lucide React** - Icons
- **React Markdown** - Markdown rendering

## 📦 Cài đặt

### 1. Install dependencies

```bash
cd front-end
npm install
```

### 2. Environment Setup

Tạo file `.env.local` (optional):

```env
VITE_API_BASE_URL=http://localhost:8000/api/v1
```

### 3. Development

```bash
npm run dev
```

App sẽ chạy tại: http://localhost:3000

### 4. Build for production

```bash
npm run build
npm run preview
```

## 🏗️ Cấu trúc Project

```
src/
├── components/          # Reusable components
│   ├── ui/             # Basic UI components
│   ├── chat/           # Chat-specific components
│   ├── documents/      # Document management components
│   └── layout/         # Layout components
├── pages/              # Main pages
├── services/           # API services
├── context/            # State management
├── types/              # TypeScript types
├── utils/              # Utility functions
└── main.tsx           # Entry point
```

## 🎨 Components

### UI Components
- `Button` - Customizable button với variants
- `Input` - Input field với validation
- `Textarea` - Multi-line text input
- `Modal` - Modal dialog với backdrop
- `Loading` - Loading spinner với text

### Chat Components
- `ChatInterface` - Main chat container
- `ChatMessage` - Individual message bubble
- `ChatInput` - Message input với auto-resize
- `TypingIndicator` - Bot typing animation

### Document Components
- `DocumentCard` - Document info card
- `DocumentManager` - Document management interface

## 🔧 Configuration

### Vite Config
- Path aliases (`@/` → `./src/`)
- API proxy để development
- Build optimization

### Tailwind CSS
- Custom color palette
- Component classes
- Responsive breakpoints
- Animation utilities

### TypeScript
- Strict mode enabled
- Path mapping
- Component type checking

## 🌐 API Integration

Frontend tự động proxy API calls trong development:
- `/api/*` → `http://localhost:8000/api/*`

Production cần configure CORS trên backend.

### API Service

```typescript
import { apiService } from '@/services/api'

// Send chat message
const response = await apiService.sendMessage({
  message: "Hello",
  include_sources: true
})

// Add document
await apiService.addTextDocument({
  content: "Document content",
  title: "Document title"
})
```

## 📱 Features

### Chat Interface
- Markdown support in responses
- Copy message functionality
- Typing indicators
- Auto-scroll to latest message
- Source document display

### Document Management
- Add text documents
- Load web documents
- Search and filter
- Delete documents
- View document status

### Settings Page
- Connection status
- System information
- Vector store management
- Configuration display

## 🎯 State Management

Sử dụng Context API với reducer pattern:

```typescript
const { state, actions } = useApp()

// Send message
await actions.sendMessage("Hello")

// Add document
await actions.addTextDocument("Content", "Title")

// Access state
const { messages, isTyping } = state.chat
const { documents } = state.documents
```

## 🚀 Development

### Scripts
- `npm run dev` - Development server
- `npm run build` - Production build
- `npm run preview` - Preview production build
- `npm run lint` - ESLint check
- `npm run type-check` - TypeScript check

### Code Style
- ESLint + TypeScript rules
- Prettier formatting
- Import organization
- Component naming conventions

## 🔄 Integration với Backend

1. **Start Backend**: Chạy FastAPI server trên port 8000
2. **Start Frontend**: Chạy React app trên port 3000
3. **API Proxy**: Vite tự động proxy `/api/*` calls

### Example workflow:
1. Thêm document qua Documents page
2. Chat với bot qua Chat page
3. Bot trả lời dựa trên documents
4. Quản lý system qua Settings page

## 🐛 Troubleshooting

### Common Issues

1. **API Connection Failed**
   ```
   Error: Network Error
   ```
   - Kiểm tra backend đang chạy trên port 8000
   - Check CORS settings trên backend

2. **Build Failed**
   ```
   Type error in component
   ```
   - Run `npm run type-check`
   - Fix TypeScript errors

3. **Styles not loading**
   - Restart dev server
   - Check Tailwind config

### Debug Tips
- Mở Developer Tools → Network tab
- Check API calls và responses
- View Console cho errors
- Use React Developer Tools

## 📦 Deployment

### Build
```bash
npm run build
```

### Static Hosting
Deploy `dist/` folder to:
- Vercel
- Netlify
- GitHub Pages
- Any static hosting

### Environment Variables
Production cần set:
```env
VITE_API_BASE_URL=https://your-api-domain.com/api/v1
```

## 🤝 Contributing

1. Fork repository
2. Create feature branch
3. Make changes
4. Run tests và type check
5. Submit pull request

## 📄 License

MIT License - see LICENSE file for details. 
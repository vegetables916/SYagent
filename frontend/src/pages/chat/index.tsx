import { useState, useRef, useEffect } from 'react'
import { Input, Avatar, Spin, Tooltip } from 'antd'
import { SendOutlined, UserOutlined, RobotOutlined, PaperClipOutlined } from '@ant-design/icons'
import './index.scss'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
  attachments?: FileAttachment[]
}

interface FileAttachment {
  id: string
  name: string
  size: number
  type: string
  file: File
}

// 允许的文件类型：图片 + 文档（pdf/markdown/word/excel）
const ACCEPTED_TYPES = [
  'image/jpeg',
  'image/png',
  'image/gif',
  'image/webp',
  'application/pdf',
  'text/markdown',
  'application/vnd.openxmlformats-officedocument.wordprocessingml.document',
  'application/msword',
  'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
  'application/vnd.ms-excel',
].join(',')

function ChatPage() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      role: 'assistant',
      content: '你好！我是 AI Agent 助手，有什么可以帮你的吗？',
      timestamp: Date.now(),
    },
  ])
  const [inputValue, setInputValue] = useState('')
  const [loading, setLoading] = useState(false)
  const [attachments, setAttachments] = useState<FileAttachment[]>([])
  const messagesEndRef = useRef<HTMLDivElement>(null)
  const fileInputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    const text = inputValue.trim()
    if ((!text && attachments.length === 0) || loading) return

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: Date.now(),
      attachments: attachments.length > 0 ? [...attachments] : undefined,
    }

    setMessages((prev) => [...prev, userMsg])
    setInputValue('')
    setAttachments([])
    setLoading(true)

    // TODO: 调用后端 AI 对话接口
    setTimeout(() => {
      const assistantMsg: Message = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: '这是一个占位回复。后端 AI 对话接口接入后，这里会显示真实的 AI 回复。',
        timestamp: Date.now(),
      }
      setMessages((prev) => [...prev, assistantMsg])
      setLoading(false)
    }, 1000)
  }

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      handleSend()
    }
  }

  const handleFileSelect = () => {
    fileInputRef.current?.click()
  }

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const files = Array.from(e.target.files || [])
    const newAttachments: FileAttachment[] = files.map((file) => ({
      id: `${Date.now()}-${Math.random()}`,
      name: file.name,
      size: file.size,
      type: file.type,
      file,
    }))
    setAttachments((prev) => [...prev, ...newAttachments])
    // 清空 input 值，允许重复选择同一文件
    if (fileInputRef.current) {
      fileInputRef.current.value = ''
    }
  }

  const removeAttachment = (id: string) => {
    setAttachments((prev) => prev.filter((att) => att.id !== id))
  }

  return (
    <div className="chat-page">
      <div className="chat-messages">
        {messages.map((msg) => (
          <div
            key={msg.id}
            className={`chat-message ${msg.role === 'user' ? 'message-user' : 'message-assistant'}`}
          >
            <Avatar
              icon={msg.role === 'user' ? <UserOutlined /> : <RobotOutlined />}
              className="message-avatar"
            />
            <div className="message-content">
              {msg.attachments && msg.attachments.length > 0 && (
                <div className="message-attachments">
                  {msg.attachments.map((att) => (
                    <div key={att.id} className="message-attachment">
                      {att.type.startsWith('image/') ? (
                        <img
                          src={URL.createObjectURL(att.file)}
                          alt={att.name}
                          className="attachment-image"
                        />
                      ) : (
                        <span className="attachment-file-name">{att.name}</span>
                      )}
                    </div>
                  ))}
                </div>
              )}
              <div className="message-bubble">{msg.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="chat-message message-assistant">
            <Avatar icon={<RobotOutlined />} className="message-avatar" />
            <div className="message-content">
              <Spin size="small" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>
      <div className="chat-input-area">
        <div className="chat-input-wrapper">
          <Tooltip title="上传文件（图片/文档）">
            <button className="attach-btn" onClick={handleFileSelect}>
              <PaperClipOutlined />
            </button>
          </Tooltip>
          <input
            ref={fileInputRef}
            type="file"
            accept={ACCEPTED_TYPES}
            multiple
            onChange={handleFileChange}
            style={{ display: 'none' }}
          />
          <Input.TextArea
            value={inputValue}
            onChange={(e) => setInputValue(e.target.value)}
            onKeyDown={handleKeyDown}
            placeholder="输入消息，Enter 发送，Shift+Enter 换行"
            autoSize={{ minRows: 1, maxRows: 4 }}
            className="chat-input"
          />
          <button
            className="send-btn"
            onClick={handleSend}
            disabled={(!inputValue.trim() && attachments.length === 0) || loading}
          >
            <SendOutlined />
          </button>
        </div>
        {attachments.length > 0 && (
          <div className="attachment-preview">
            {attachments.map((att) => (
              <div key={att.id} className="attachment-item">
                <span className="attachment-name">{att.name}</span>
                <span className="attachment-remove" onClick={() => removeAttachment(att.id)}>
                  ×
                </span>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default ChatPage

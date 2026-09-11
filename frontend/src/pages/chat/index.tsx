import { useState, useRef, useEffect } from 'react'
import { Input, Avatar, Spin } from 'antd'
import { SendOutlined, UserOutlined, RobotOutlined } from '@ant-design/icons'
import './index.scss'

interface Message {
  id: string
  role: 'user' | 'assistant'
  content: string
  timestamp: number
}

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
  const messagesEndRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const handleSend = async () => {
    const text = inputValue.trim()
    if (!text || loading) return

    const userMsg: Message = {
      id: Date.now().toString(),
      role: 'user',
      content: text,
      timestamp: Date.now(),
    }

    setMessages((prev) => [...prev, userMsg])
    setInputValue('')
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
            disabled={!inputValue.trim() || loading}
          >
            <SendOutlined />
          </button>
        </div>
      </div>
    </div>
  )
}

export default ChatPage

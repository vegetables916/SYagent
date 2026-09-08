import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import './index.css'

function LoginPage() {
  const navigate = useNavigate()
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = (e: React.FormEvent) => {
    e.preventDefault()
    console.log('登录:', { username, password })
    navigate('/')
  }

  return (
    <div className="login-container">
      <div className="login-box">
        <h2 className="login-title">AI Agent Workflow Platform</h2>
        <form onSubmit={handleLogin} className="login-form">
          <div className="form-item">
            <label className="form-label">用户名</label>
            <input
              type="text"
              className="form-input"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="请输入用户名"
            />
          </div>
          <div className="form-item">
            <label className="form-label">密码</label>
            <input
              type="password"
              className="form-input"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              placeholder="请输入密码"
            />
          </div>
          <button type="submit" className="login-btn">
            登录
          </button>
        </form>
      </div>
    </div>
  )
}

export default LoginPage
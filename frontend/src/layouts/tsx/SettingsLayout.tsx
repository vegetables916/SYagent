import { Outlet, useNavigate, useLocation } from 'react-router-dom'
import {
  Layout,
  Menu,
  Avatar,
  Dropdown,
  message,
} from 'antd'
import {
  AppstoreOutlined,
  MessageOutlined,
  SettingOutlined,
  LogoutOutlined,
  UserOutlined,
} from '@ant-design/icons'
import type { MenuProps } from 'antd'
import logo from '@/assets/logo.png'
import '../css/SettingsLayout.scss'

const menuItems: MenuProps['items'] = [
  {
    key: '/',
    icon: <AppstoreOutlined />,
    label: '工作流画布',
  },
  {
    key: '/chat',
    icon: <MessageOutlined />,
    label: 'AI 对话',
  },
  {
    key: '/settings',
    icon: <SettingOutlined />,
    label: '设置',
  },
]

function SettingsLayout() {
  const navigate = useNavigate()
  const location = useLocation()

  const handleMenuClick: MenuProps['onClick'] = ({ key }) => {
    navigate(key)
  }

  const handleLogout = () => {
    localStorage.removeItem('token')
    message.success('已退出登录')
    navigate('/login')
  }

  const userMenuItems: MenuProps['items'] = [
    {
      key: 'profile',
      icon: <UserOutlined />,
      label: '个人中心',
    },
    {
      type: 'divider',
    },
    {
      key: 'logout',
      icon: <LogoutOutlined />,
      label: '退出登录',
      onClick: handleLogout,
    },
  ]

  return (
    <Layout className="settings-layout">
      <div className="layout-user-fixed">
        <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
          <div className="user-info">
            <Avatar size="small" icon={<UserOutlined />} />
            <span className="user-name">用户</span>
          </div>
        </Dropdown>
      </div>

      <div className="settings-sidebar">
        <div className="settings-sidebar-header">
          <img src={logo} alt="Logo" className="logo-img" />
        </div>
        <div className="settings-sidebar-nav">
          <Menu
            mode="inline"
            selectedKeys={[location.pathname]}
            items={menuItems}
            onClick={handleMenuClick}
          />
        </div>
      </div>
      <div className="settings-main">
        <Outlet />
      </div>
    </Layout>
  )
}

export default SettingsLayout

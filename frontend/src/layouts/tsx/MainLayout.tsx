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
import '../css/MainLayout.scss'

const { Sider, Content } = Layout

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

function MainLayout() {
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
    <Layout className="main-layout">
      <div className="layout-user-fixed">
        <Dropdown menu={{ items: userMenuItems }} placement="bottomRight">
          <div className="user-info">
            <Avatar size="small" icon={<UserOutlined />} />
            <span className="user-name">用户</span>
          </div>
        </Dropdown>
      </div>

      <Sider
        width={220}
        className="main-sider"
        theme="light"
      >
        <div className="sider-logo">
          <img src={logo} alt="Logo" className="logo-img" />
        </div>
        <Menu
          mode="inline"
          selectedKeys={[location.pathname]}
          items={menuItems}
          onClick={handleMenuClick}
        />
      </Sider>
      <Layout className="main-body">
        <Content className="main-content">
          <Outlet />
        </Content>
      </Layout>
    </Layout>
  )
}

export default MainLayout

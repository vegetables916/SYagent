import { createBrowserRouter } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import MainLayout from '@/layouts/tsx/MainLayout'
import ChatLayout from '@/layouts/tsx/ChatLayout'
import SettingsLayout from '@/layouts/tsx/SettingsLayout'
import LoginPage from '@/pages/Login'

const ChatPage = lazy(() => import('@/pages/chat'))
const SettingsPage = lazy(() => import('@/pages/settings'))

const router = createBrowserRouter([
  {
    path: '/login',
    element: <LoginPage />,
  },
  {
    path: '/',
    element: <MainLayout />,
    children: [
      {
        index: true,
        element: <div>工作流画布（待开发）</div>,
      },
    ],
  },
  {
    path: '/chat',
    element: (
      <Suspense fallback={<div>加载中...</div>}>
        <ChatLayout />
      </Suspense>
    ),
    children: [
      {
        index: true,
        element: <ChatPage />,
      },
    ],
  },
  {
    path: '/settings',
    element: (
      <Suspense fallback={<div>加载中...</div>}>
        <SettingsLayout />
      </Suspense>
    ),
    children: [
      {
        index: true,
        element: <SettingsPage />,
      },
    ],
  },
])

export default router

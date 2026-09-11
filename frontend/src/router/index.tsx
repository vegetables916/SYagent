import { createBrowserRouter } from 'react-router-dom'
import { lazy, Suspense } from 'react'
import MainLayout from '@/layouts/tsx/MainLayout'
import NotFound from '@/layouts/tsx/NotFound'
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
      {
        path: 'chat',
        element: (
          <Suspense fallback={<div>加载中...</div>}>
            <ChatPage />
          </Suspense>
        ),
      },
      {
        path: 'settings',
        element: (
          <Suspense fallback={<div>加载中...</div>}>
            <SettingsPage />
          </Suspense>
        ),
      },
    ],
  },
  {
    path: '*',
    element: <NotFound />,
  },
])

export default router

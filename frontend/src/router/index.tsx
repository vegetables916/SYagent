import { createBrowserRouter } from 'react-router-dom'
import MainLayout from '../layout/MainLayout'
import LoginPage from '../pages/Login'

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
        element: <div>首页</div>,
      },
    ],
  },
])

export default router
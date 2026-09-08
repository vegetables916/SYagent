import { Outlet } from 'react-router-dom'

function MainLayout() {
  return (
    <div className="main-layout">
      <header className="layout-header">
        <h1>AI Agent Workflow Platform</h1>
      </header>
      <main className="layout-content">
        <Outlet />
      </main>
    </div>
  )
}

export default MainLayout
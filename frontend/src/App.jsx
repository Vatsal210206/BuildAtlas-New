import { useState } from 'react'
import Sidebar from './components/Sidebar.jsx'
import ModulePage from './components/ModulePage.jsx'
import { modules } from './modules/moduleDefinitions.js'

export default function App() {
  const [activeId, setActiveId] = useState('dashboard')
  const activeModule = modules.find((module) => module.id === activeId) || modules[0]

  return (
    <div className="app-shell">
      <Sidebar activeModule={activeModule} onSelect={setActiveId} />
      <ModulePage module={activeModule} />
    </div>
  )
}

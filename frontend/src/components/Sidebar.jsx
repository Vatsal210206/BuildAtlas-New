import { modules } from '../modules/moduleDefinitions.js'

export default function Sidebar({ activeModule, onSelect }) {
  return (
    <aside className="sidebar">
      <div className="brand-block">
        <div className="brand-mark">▰</div>
        <div>
          <div className="brand-name">BUILDATLAS</div>
          <div className="brand-caption">AI CONSTRUCTION PLATFORM</div>
        </div>
      </div>

      <div className="sidebar-label">Current Page</div>
      <div className="current-page">
        <span className="current-page-icon">{activeModule.icon}</span>
        <span>{activeModule.label}</span>
      </div>

      <div className="sidebar-label quick-access-label">Quick Access</div>
      <nav className="module-nav" aria-label="BuildAtlas modules">
        {modules.map((module) => (
          <button
            className={`nav-item ${module.id === activeModule.id ? 'active' : ''}`}
            key={module.id}
            onClick={() => onSelect(module.id)}
            type="button"
          >
            <span className="nav-icon">{module.icon}</span>
            <span>{module.label}</span>
          </button>
        ))}
      </nav>

      <div className="sidebar-footer">
        <span className="status-dot" />
        <span>Migration foundation</span>
      </div>
    </aside>
  )
}

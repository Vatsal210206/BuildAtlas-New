import CostPredictionPage from './CostPredictionPage.jsx'
import BillScannerPage from './BillScannerPage.jsx'

export default function ModulePage({ module }) {
  const isDashboard = module.id === 'dashboard'

  return (
    <main className="main-content">
      <header className="page-header">
        <div>
          <p className="page-eyebrow">{module.eyebrow}</p>
          <h1>{module.label}</h1>
          <p className="page-description">{module.description}</p>
        </div>
        <div className="page-index">{String(module.id === 'dashboard' ? 1 : 2).padStart(2, '0')} / 10</div>
      </header>

      {isDashboard ? (
        <>
          <section className="metric-grid" aria-label="Dashboard summary">
            <div className="metric-card"><span>Active Projects</span><strong>03</strong><small>Current portfolio</small></div>
            <div className="metric-card"><span>Overall Progress</span><strong>64%</strong><small>Across tracked work</small></div>
            <div className="metric-card"><span>Budget Used</span><strong>₹24.8L</strong><small>Project allocation</small></div>
            <div className="metric-card accent-card"><span>Next Milestone</span><strong>12 days</strong><small>Foundation inspection</small></div>
          </section>
          <section className="dashboard-grid">
            <div className="industrial-panel activity-panel">
              <div className="panel-heading"><span>Project activity</span><span className="panel-kicker">LIVE VIEW</span></div>
              <div className="activity-line"><span className="activity-marker teal" /><div><strong>Foundation work updated</strong><small>Greenfield Residence · 18 min ago</small></div><b>+4%</b></div>
              <div className="activity-line"><span className="activity-marker orange" /><div><strong>Material quote received</strong><small>Urban Edge Villa · 2 hours ago</small></div><b>₹2.4L</b></div>
              <div className="activity-line"><span className="activity-marker blue" /><div><strong>Builder shortlist saved</strong><small>New project · Yesterday</small></div><b>03</b></div>
            </div>
            <div className="industrial-panel signal-panel">
              <div className="panel-heading"><span>Build signal</span><span className="signal-value">72</span></div>
              <div className="signal-ring"><span>STABLE</span></div>
              <p>Planning confidence is based on the current project view.</p>
            </div>
          </section>
        </>
      ) : module.id === 'cost-prediction' ? (
        <CostPredictionPage />
      ) : module.id === 'bill-scanner' ? (
        <BillScannerPage />
      ) : (
        <section className="placeholder-layout">
          <div className="industrial-panel placeholder-panel">
            <div className="panel-heading"><span>Module workspace</span><span className="panel-kicker">FOUNDATION</span></div>
            <div className="placeholder-icon">{module.icon}</div>
            <h2>{module.label} is ready for migration</h2>
            <p>This page preserves the approved BuildAtlas navigation while its existing Streamlit functionality remains the reference implementation.</p>
            <span className="coming-status">Backend service not connected</span>
          </div>
        </section>
      )}
    </main>
  )
}

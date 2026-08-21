import { useState } from 'react'
import { apiConfig } from '../api/client.js'

const initialForm = {
  size: 1000,
  floors: 2,
  project_type: 'Residential',
  city: 'Delhi',
}

function formatApiError(payload) {
  if (typeof payload.detail === 'string') {
    return payload.detail
  }
  if (Array.isArray(payload.detail)) {
    return payload.detail
      .map((item) => `${item.loc?.at(-1) || 'input'}: ${item.msg}`)
      .join(' ')
  }
  return 'Cost prediction could not be completed.'
}

export default function CostPredictionPage() {
  const [form, setForm] = useState(initialForm)
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  function updateField(event) {
    const { name, value } = event.target
    setForm((current) => ({ ...current, [name]: name === 'size' || name === 'floors' ? Number(value) : value }))
  }

  async function submitPrediction(event) {
    event.preventDefault()
    setStatus('loading')
    setResult(null)
    setError('')

    try {
      const response = await fetch(`${apiConfig.baseUrl}/cost/predict`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(form),
      })
      const payload = await response.json()
      if (!response.ok) {
        throw new Error(formatApiError(payload))
      }
      setResult(payload)
      setStatus('success')
    } catch (requestError) {
      setError(requestError.message)
      setStatus('error')
    }
  }

  return (
    <section className="cost-layout">
      <form className="industrial-panel cost-form" onSubmit={submitPrediction}>
        <div className="panel-heading"><span>Project details</span><span className="panel-kicker">INPUTS</span></div>
        <label>
          Area (sqm)
          <input name="size" type="number" min="1" step="1" value={form.size} onChange={updateField} required />
        </label>
        <label>
          Floors
          <input name="floors" type="number" min="1" step="1" value={form.floors} onChange={updateField} required />
        </label>
        <label>
          Project Type
          <select name="project_type" value={form.project_type} onChange={updateField}>
            <option>Residential</option>
            <option>Commercial</option>
            <option>Industrial</option>
          </select>
        </label>
        <label>
          City
          <select name="city" value={form.city} onChange={updateField}>
            <option>Delhi</option>
            <option>Mumbai</option>
            <option>Bangalore</option>
            <option>Hyderabad</option>
            <option>Pune</option>
          </select>
        </label>
        <button className="primary-button" disabled={status === 'loading'} type="submit">
          {status === 'loading' ? 'Predicting...' : 'Predict Cost'}
        </button>
        {status === 'error' && <p className="form-error" role="alert">{error}</p>}
      </form>

      <div className="industrial-panel cost-result-panel">
        <div className="panel-heading"><span>Prediction</span><span className="panel-kicker">MODEL OUTPUT</span></div>
        {status === 'success' && result ? (
          <div className="prediction-result" role="status">
            <span className="result-label">Predicted Total Cost</span>
            <strong>₹{result.total_cost_crore.toFixed(2)} Cr</strong>
            <span className="result-meta">{result.size} sqm · {result.floors} floors · {result.project_type} · {result.city}</span>
          </div>
        ) : (
          <div className="empty-result"><span>₹</span><p>Enter project details to calculate the estimated total cost.</p></div>
        )}
      </div>
    </section>
  )
}

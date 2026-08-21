import { useEffect, useState } from 'react'
import { apiConfig } from '../api/client.js'

function formatApiError(payload) {
  if (typeof payload.detail === 'string') return payload.detail
  return 'Bill scanning could not be completed.'
}

export default function BillScannerPage() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState('')
  const [status, setStatus] = useState('idle')
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  useEffect(() => () => previewUrl && URL.revokeObjectURL(previewUrl), [previewUrl])

  function handleFileChange(event) {
    const selectedFile = event.target.files?.[0] || null
    setFile(selectedFile)
    setResult(null)
    setError('')
    setStatus('idle')
    setPreviewUrl(selectedFile ? URL.createObjectURL(selectedFile) : '')
  }

  async function scanBill(event) {
    event.preventDefault()
    if (!file) {
      setError('Select a JPG, JPEG, or PNG bill image first.')
      setStatus('error')
      return
    }

    setStatus('loading')
    setResult(null)
    setError('')
    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch(`${apiConfig.baseUrl}/bills/scan`, {
        method: 'POST',
        body: formData,
      })
      const payload = await response.json()
      if (!response.ok) throw new Error(formatApiError(payload))
      setResult(payload)
      setStatus('success')
    } catch (requestError) {
      setError(requestError.message)
      setStatus('error')
    }
  }

  return (
    <section className="bill-scanner-layout">
      <form className="industrial-panel bill-upload-panel" onSubmit={scanBill}>
        <div className="panel-heading"><span>📁 Upload Invoice</span><span className="panel-kicker">OCR INPUT</span></div>
        <label className="upload-dropzone" htmlFor="bill-file">
          <span className="upload-icon">▧</span>
          <strong>Drop bill image here</strong>
          <small>JPG, JPEG, or PNG</small>
          <input id="bill-file" type="file" accept=".jpg,.jpeg,.png,image/jpeg,image/png" onChange={handleFileChange} />
        </label>
        {previewUrl && <img className="bill-preview" src={previewUrl} alt="Uploaded bill preview" />}
        {file && <div className="selected-file">{file.name}</div>}
        <button className="primary-button" disabled={status === 'loading' || !file} type="submit">
          {status === 'loading' ? 'Scanning bill...' : '🔍 Scan Bill with OCR'}
        </button>
        {status === 'loading' && <p className="scan-progress" role="status">OCR processing... Azure is reading the invoice.</p>}
        {status === 'error' && <p className="form-error" role="alert">{error}</p>}
      </form>

      <div className="industrial-panel bill-results-panel">
        <div className="panel-heading"><span>📊 Scanned Data Analysis</span><span className="panel-kicker">RESULTS</span></div>
        {status === 'success' && result ? (
          <div className="bill-results" role="status">
            <div className="bill-metrics">
              <div><span>Supplier</span><strong>{result.supplier}</strong></div>
              <div><span>Date</span><strong>{result.date}</strong></div>
              <div><span>Total Amount</span><strong>₹{result.total.toLocaleString('en-IN')}</strong></div>
              <div><span>Items Found</span><strong>{result.materials.length}</strong></div>
            </div>
            <p className="success-message">✅ Bill scanned successfully!</p>
            <div className="material-table-wrap">
              <h2>Materials</h2>
              <table className="material-table">
                <thead><tr><th>Material</th><th>Quantity</th><th>Unit</th><th>Rate</th><th>Total</th></tr></thead>
                <tbody>{result.materials.map((material, index) => <tr key={`${material.name}-${index}`}><td>{material.name}</td><td>{material.quantity}</td><td>{material.unit}</td><td>₹{material.rate}</td><td>₹{material.total}</td></tr>)}</tbody>
              </table>
            </div>
            <details className="raw-ocr"><summary>📄 Raw OCR Text (Extracted)</summary><pre>{result.raw_text || 'No OCR text returned.'}</pre></details>
          </div>
        ) : (
          <div className="empty-result"><span>▤</span><p>Upload a construction bill to review its OCR text and extracted materials.</p></div>
        )}
      </div>
    </section>
  )
}

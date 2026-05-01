import { useMemo, useState } from 'react'

const API_BASE = 'http://localhost:5000/api'
const DIMENSIONS = ['social', 'environment', 'economy']

function ScoreBar({ label, value }) {
  return (
    <div className="bar-row">
      <div className="bar-head"><span>{label}</span><b>{value}</b></div>
      <div className="bar-track"><div className="bar-fill" style={{ width: `${value}%` }} /></div>
    </div>
  )
}

export default function App() {
  const [address, setAddress] = useState('11 Collins St, Melbourne VIC 3000, Australia')
  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')
  const [activeTab, setActiveTab] = useState('social')

  const runAssessment = async (event) => {
    event.preventDefault()
    setLoading(true)
    setError('')
    try {
      const res = await fetch(`${API_BASE}/assess`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ address })
      })
      if (!res.ok) throw new Error('Could not run assessment right now.')
      const json = await res.json()
      setResult(json)
    } catch (e) {
      setError(e.message)
    } finally {
      setLoading(false)
    }
  }

  const activeMetrics = useMemo(() => {
    if (!result) return []
    return result.dimensions[activeTab]?.metrics ?? []
  }, [result, activeTab])

  return (
    <main className="container">
      <header className="hero panel">
        <h1>Australia Property Liveability Studio</h1>
        <p>Explore address-level liveability with market signals, facilities proximity and quality-of-life dimensions.</p>
      </header>

      <form className="panel search" onSubmit={runAssessment}>
        <input value={address} onChange={(e) => setAddress(e.target.value)} placeholder="Enter an Australian address" />
        <button disabled={loading} type="submit">{loading ? 'Assessing…' : 'Assess Address'}</button>
      </form>

      {error ? <p className="error">{error}</p> : null}

      {result && (
        <>
          <section className="panel top-grid">
            <div>
              <p className="kicker">Address</p>
              <h2>{result.address}</h2>
              <p>{result.cityContext}, {result.country}</p>
            </div>
            <div className="overall-card">
              <p className="kicker">Overall Score</p>
              <h2>{result.overallScore}</h2>
            </div>
            <div>
              <p className="kicker">Assessment Types</p>
              <div className="chips">{result.assessmentTypes.map((x) => <span key={x}>{x}</span>)}</div>
            </div>
          </section>

          <section className="panel split">
            <div>
              <h3>Dimension Snapshot</h3>
              {DIMENSIONS.map((d) => (
                <ScoreBar key={d} label={d[0].toUpperCase() + d.slice(1)} value={result.dimensions[d].score} />
              ))}

              <div className="tab-row">
                {DIMENSIONS.map((d) => (
                  <button key={d} type="button" className={activeTab === d ? 'active' : ''} onClick={() => setActiveTab(d)}>
                    {d[0].toUpperCase() + d.slice(1)}
                  </button>
                ))}
              </div>

              <div className="metrics-list">
                {activeMetrics.map((m) => (
                  <ScoreBar key={m.name} label={m.name} value={m.score} />
                ))}
              </div>
            </div>

            <aside>
              <h3>Market Signals</h3>
              <ul className="signal-list">
                <li><span>Median Price</span><b>${result.marketSignals.medianPriceAUD.toLocaleString()}</b></li>
                <li><span>Monthly Trend</span><b>+{result.marketSignals.monthlyTrendPct}%</b></li>
                <li><span>Annual Trend</span><b>+{result.marketSignals.annualTrendPct}%</b></li>
                <li><span>Rental Yield</span><b>{result.marketSignals.rentalYieldPct}%</b></li>
              </ul>

              <h3>Nearby Amenities</h3>
              <div className="amenities">
                {Object.entries(result.nearby).map(([group, items]) => (
                  <div key={group}>
                    <h4>{group}</h4>
                    {items.map((i) => <p key={i.name}>{i.name} · {i.distanceKm} km</p>)}
                  </div>
                ))}
              </div>

              <h3>Key Highlights</h3>
              <ul className="highlights">
                {result.highlights.map((h) => <li key={h}>{h}</li>)}
              </ul>
            </aside>
          </section>
        </>
      )}
    </main>
  )
}

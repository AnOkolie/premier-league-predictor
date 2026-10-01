import { useState } from 'react'
import './App.css'

const SEASONS = Array.from({ length: 8 }, (_, index) => 2019 + index)
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

function firstValue(source, keys) {
  for (const key of keys) {
    if (source?.[key] !== undefined && source?.[key] !== null) return source[key]
  }
  return undefined
}

function normalizePlayer(payload) {
  const candidate = payload?.player ?? payload?.data?.player ?? payload?.data ?? payload?.result ?? payload
  const stats = candidate?.stats ?? candidate?.predictions ?? candidate
  const previousValue = firstValue(stats, ['previous_transfer_value', 'previous_value', 'previous_season_value', 'start_val'])
  const currentValue = firstValue(stats, ['predicted_transfer_value', 'predicted_value', 'transfer_value', 'valuation', 'end_val'])
  const explicitChange = firstValue(stats, ['value_change_percent', 'transfer_value_change_percent', 'change_percent'])
  const change = explicitChange ?? (
    Number.isFinite(Number(previousValue)) && Number(previousValue) !== 0 && Number.isFinite(Number(currentValue))
      ? ((Number(currentValue) - Number(previousValue)) / Number(previousValue)) * 100
      : undefined
  )

  return {
    name: firstValue(candidate, ['player_name', 'name']) ?? firstValue(stats, ['player_name', 'name']),
    team: firstValue(candidate, ['team', 'team_name']),
    position: firstValue(candidate, ['position']),
    transferValue: currentValue,
    previousValue,
    change: change === undefined ? undefined : Number(change),
    goals: firstValue(stats, ['predicted_goals', 'goals', 'projected_goals']),
    assists: firstValue(stats, ['predicted_assists', 'assists', 'projected_assists']),
    minutes: firstValue(stats, ['predicted_minutes', 'minutes', 'projected_minutes']),
  }
}

function formatCurrency(value) {
  const amount = Number(value)
  if (!Number.isFinite(amount)) return '—'
  return new Intl.NumberFormat('en-GB', {
    style: 'currency',
    currency: 'EUR',
    notation: amount >= 1_000_000 ? 'compact' : 'standard',
    maximumFractionDigits: amount >= 1_000_000 ? 1 : 0,
  }).format(amount)
}

function TrendIcon({ up }) {
  return (
    <svg viewBox="0 0 24 24" aria-hidden="true" className="trend-icon">
      {up ? <path d="m4 16 6-6 4 4 6-7M14 7h6v6" /> : <path d="m4 8 6 6 4-4 6 7M14 17h6v-6" />}
    </svg>
  )
}

function StatCard({ label, value, unit, icon }) {
  return (
    <article className="stat-card">
      <div className="stat-card-top">
        <span className="stat-icon" aria-hidden="true">{icon}</span>
        <span className="stat-label">{label}</span>
      </div>
      <p className="stat-value">{value ?? '—'}<span>{unit}</span></p>
      <p className="stat-caption">Projected season total</p>
    </article>
  )
}

function App() {
  const [name, setName] = useState('')
  const [season, setSeason] = useState(2026)
  const [player, setPlayer] = useState(null)
  const [status, setStatus] = useState('idle')
  const [error, setError] = useState('')

  async function handleSubmit(event) {
    event.preventDefault()
    const query = name.trim()
    if (!query) {
      setError('Enter a player name to start your search.')
      setStatus('error')
      return
    }

    setStatus('loading')
    setError('')
    setPlayer(null)

    try {
      const params = new URLSearchParams({ name: query, season: String(season) })
      const response = await fetch(`${API_BASE_URL}/player/?${params.toString()}`)
      if (!response.ok) throw new Error(`The server returned an error (${response.status}).`)
      const payload = await response.json()
      const result = normalizePlayer(payload)
      if (!result.name && result.transferValue == null && result.goals == null && result.assists == null && result.minutes == null) {
        throw new Error(payload?.detail || 'No prediction found. Check the player name and try again.')
      }
      setPlayer(result)
      setStatus('success')
    } catch (requestError) {
      setError(requestError.message || 'Could not reach the prediction service. Please try again.')
      setStatus('error')
    }
  }

  const isTrendingUp = Number(player?.change) >= 0

  return (
    <main className="app-shell">
      <header className="topbar">
        <a className="brand" href="#top" aria-label="Touchline home">
          <span className="brand-mark" aria-hidden="true">T</span>
          <span>touchline<span className="brand-period">.</span></span>
        </a>
        <span className="topbar-note"><span className="live-dot" /> PLAYER INTELLIGENCE</span>
      </header>

      <section className="hero" id="top">
        <div className="hero-copy">
          <p className="eyebrow"><span /> THE SCOUTING DESK</p>
          <h1>See the season<br /><span>taking shape.</span></h1>
          <p className="hero-description">A clearer view of what comes next. Search a player to explore their projected value and season performance.</p>
        </div>

        <form className="search-panel" onSubmit={handleSubmit}>
          <label className="field-label" htmlFor="player-name">PLAYER NAME</label>
          <div className="search-input-wrap">
            <svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="10.8" cy="10.8" r="6.8" /><path d="m16 16 4.5 4.5" /></svg>
            <input
              id="player-name"
              type="search"
              value={name}
              onChange={(event) => setName(event.target.value)}
              placeholder="e.g. Erling Haaland"
              autoComplete="off"
            />
          </div>
          <div className="search-bottom">
            <div className="season-field">
              <label className="field-label" htmlFor="season">SEASON</label>
              <div className="select-wrap">
                <select id="season" value={season} onChange={(event) => setSeason(Number(event.target.value))}>
                  {SEASONS.map((year) => <option key={year} value={year}>{year} / {String(year + 1).slice(-2)}</option>)}
                </select>
                <svg viewBox="0 0 16 16" aria-hidden="true"><path d="m4 6 4 4 4-4" /></svg>
              </div>
            </div>
            <button className="search-button" type="submit" disabled={status === 'loading'}>
              {status === 'loading' ? <><span className="spinner" /> Searching</> : <>Explore player <span aria-hidden="true">↗</span></>}
            </button>
          </div>
          <p className="form-footnote">PREMIER LEAGUE <span>·</span> SEASON PROJECTIONS</p>
        </form>

        <div className="hero-index" aria-hidden="true">01 <span /> 03</div>
      </section>

      <section className="results-section" aria-live="polite">
        <div className="section-heading">
          <div>
            <p className="eyebrow">PLAYER OVERVIEW</p>
            <h2>{player?.name || 'Your next discovery'}</h2>
          </div>
          {player && <span className="season-chip">{season} / {String(season + 1).slice(-2)} SEASON</span>}
        </div>

        {status === 'idle' && (
          <div className="empty-state">
            <span className="empty-ball" aria-hidden="true"><span /></span>
            <p>Start with a name above.</p>
            <span>Your player’s projected season stats will appear here.</span>
          </div>
        )}
        {status === 'loading' && (
          <div className="loading-state"><span className="spinner dark" /> Pulling the latest projections…</div>
        )}
        {status === 'error' && (
          <div className="message-state error-state" role="alert">
            <span className="message-mark">!</span>
            <div><strong>We couldn’t load that player.</strong><p>{error}</p></div>
          </div>
        )}
        {status === 'success' && player && (
          <>
            <div className="player-card">
              <div className="player-identity">
                <div className="player-avatar" aria-hidden="true">{(player.name || '?').split(' ').map((part) => part[0]).slice(0, 2).join('').toUpperCase()}</div>
                <div><span className="player-kicker">SEASON PROJECTION</span><h3>{player.name || name}</h3><p>{[player.position, player.team].filter(Boolean).join(' · ') || 'Premier League'}</p></div>
              </div>
              <div className="value-block">
                <span className="player-kicker">PREDICTED TRANSFER VALUE</span>
                <strong>{formatCurrency(player.transferValue)}</strong>
                {player.change !== undefined && Number.isFinite(player.change) ? (
                  <span className={`trend-badge ${isTrendingUp ? 'up' : 'down'}`}>
                    <TrendIcon up={isTrendingUp} /> {isTrendingUp ? '+' : ''}{player.change.toFixed(1)}% <span>vs previous season</span>
                  </span>
                ) : <span className="trend-unavailable">Change vs previous season unavailable</span>}
              </div>
            </div>
            <div className="stats-grid">
              <StatCard label="GOALS" value={player.goals ?? '—'} unit=" goals" icon="⚽" />
              <StatCard label="ASSISTS" value={player.assists ?? '—'} unit=" assists" icon="✳" />
              <StatCard label="MINUTES" value={player.minutes == null ? '—' : Number(player.minutes).toLocaleString('en-GB')} unit=" min" icon="◷" />
            </div>
          </>
        )}
      </section>

      <footer className="site-footer"><span>TOUCHLINE <span className="brand-period">.</span></span><span>DATA-LED. GAME-READY.</span><span>2019 — 2026</span></footer>
    </main>
  )
}

export default App

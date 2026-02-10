import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'
import type { Game } from '../types'

export function SchedulePage() {
  const [games, setGames] = useState<Game[]>([])
  const [from, setFrom] = useState('')
  const [to, setTo] = useState('')

  useEffect(() => {
    const params = new URLSearchParams()
    if (from) params.set('from', from)
    if (to) params.set('to', to)
    const query = params.toString() ? `?${params.toString()}` : ''
    void apiGet<Game[]>(`/schedule${query}`).then(setGames)
  }, [from, to])

  return (
    <div>
      <h2>Schedule</h2>
      <div className="filters">
        <input type="date" value={from} onChange={(e) => setFrom(e.target.value)} />
        <input type="date" value={to} onChange={(e) => setTo(e.target.value)} />
      </div>
      {games.map((g) => (
        <article key={g.id} className="card">
          <p>{g.away_team_name} @ {g.home_team_name}</p>
          <p>{new Date(g.start_time).toLocaleString()} · {g.field}</p>
          <p>{g.status === 'FINAL' ? `Final ${g.away_score}-${g.home_score}` : 'Scheduled'}</p>
        </article>
      ))}
    </div>
  )
}

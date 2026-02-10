import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'
import type { StandingsRow } from '../types'

export function StandingsPage() {
  const [rows, setRows] = useState<StandingsRow[]>([])

  useEffect(() => {
    void apiGet<StandingsRow[]>('/standings').then(setRows)
  }, [])

  return (
    <div>
      <h2>Standings</h2>
      <table>
        <thead><tr><th>Team</th><th>W</th><th>L</th><th>GP</th><th>RF</th><th>RA</th></tr></thead>
        <tbody>
          {rows.map((r) => <tr key={r.team_id}><td>{r.team_name}</td><td>{r.wins}</td><td>{r.losses}</td><td>{r.games_played}</td><td>{r.runs_for}</td><td>{r.runs_against}</td></tr>)}
        </tbody>
      </table>
    </div>
  )
}

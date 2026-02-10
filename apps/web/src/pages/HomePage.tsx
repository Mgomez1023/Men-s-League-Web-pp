import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'
import type { Announcement, Game, StandingsRow } from '../types'

export function HomePage() {
  const [nextGame, setNextGame] = useState<Game | null>(null)
  const [announcements, setAnnouncements] = useState<Announcement[]>([])
  const [standings, setStandings] = useState<StandingsRow[]>([])

  useEffect(() => {
    void apiGet<Game[]>('/schedule').then((games) => setNextGame(games.find((g) => g.status === 'SCHEDULED') ?? null))
    void apiGet<Announcement[]>('/announcements').then((items) => setAnnouncements(items.slice(0, 3)))
    void apiGet<StandingsRow[]>('/standings').then((rows) => setStandings(rows.slice(0, 3)))
  }, [])

  return (
    <div>
      <h2>Next Game</h2>
      {nextGame ? <p>{nextGame.away_team_name} @ {nextGame.home_team_name} — {new Date(nextGame.start_time).toLocaleString()}</p> : <p>No upcoming games.</p>}

      <h2>Recent Announcements</h2>
      {announcements.map((a) => <article key={a.id}><strong>{a.title}</strong><p>{a.body}</p></article>)}

      <h2>Standings Preview</h2>
      <ul>{standings.map((row) => <li key={row.team_id}>{row.team_name} ({row.wins}-{row.losses})</li>)}</ul>
    </div>
  )
}

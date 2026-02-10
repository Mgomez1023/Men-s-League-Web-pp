import { useEffect, useState } from 'react'
import { useParams } from 'react-router-dom'
import { apiGet } from '../api/client'
import type { Game, TeamDetail } from '../types'

export function TeamDetailPage() {
  const { teamId } = useParams()
  const [team, setTeam] = useState<TeamDetail | null>(null)
  const [schedule, setSchedule] = useState<Game[]>([])

  useEffect(() => {
    if (!teamId) return
    void apiGet<TeamDetail>(`/teams/${teamId}`).then(setTeam)
    void apiGet<Game[]>('/schedule').then((games) => setSchedule(games.filter((g) => g.home_team_id === teamId || g.away_team_id === teamId)))
  }, [teamId])

  if (!team) return <p>Loading...</p>

  return (
    <div>
      <h2>{team.name}</h2>
      <h3>Roster</h3>
      <ul>{team.roster.map((p) => <li key={p.id}>#{p.number ?? '--'} {p.name} {p.position ? `(${p.position})` : ''}</li>)}</ul>
      <h3>Upcoming Games</h3>
      <ul>{schedule.filter((g) => g.status === 'SCHEDULED').map((g) => <li key={g.id}>{g.away_team_name} @ {g.home_team_name} on {new Date(g.start_time).toLocaleDateString()}</li>)}</ul>
    </div>
  )
}

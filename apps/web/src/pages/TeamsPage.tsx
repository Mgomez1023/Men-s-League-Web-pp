import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { apiGet } from '../api/client'
import type { Team } from '../types'

export function TeamsPage() {
  const [teams, setTeams] = useState<Team[]>([])

  useEffect(() => {
    void apiGet<Team[]>('/teams').then(setTeams)
  }, [])

  return <ul>{teams.map((team) => <li key={team.id}><Link to={`/teams/${team.id}`}>{team.name}</Link></li>)}</ul>
}

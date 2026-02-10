export type GameStatus = 'SCHEDULED' | 'FINAL'

export interface Team {
  id: string
  name: string
  slug: string
}

export interface Player {
  id: string
  team_id: string
  name: string
  number?: number | null
  position?: string | null
}

export interface TeamDetail extends Team {
  roster: Player[]
}

export interface Game {
  id: string
  home_team_id: string
  away_team_id: string
  start_time: string
  field: string
  status: GameStatus
  home_score?: number | null
  away_score?: number | null
  home_team_name?: string
  away_team_name?: string
}

export interface Announcement {
  id: string
  title: string
  body: string
  created_at: string
  created_by_email: string
}

export interface StandingsRow {
  team_id: string
  team_name: string
  wins: number
  losses: number
  games_played: number
  runs_for: number
  runs_against: number
}

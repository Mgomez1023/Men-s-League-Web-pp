import { FormEvent, useEffect, useState } from 'react'
import { apiGet, apiPost, supabase } from '../api/client'
import type { Team } from '../types'

export function AdminDashboardPage() {
  const [token, setToken] = useState<string>('')
  const [teams, setTeams] = useState<Team[]>([])
  const [message, setMessage] = useState('')

  useEffect(() => {
    void supabase.auth.getSession().then(({ data }) => setToken(data.session?.access_token ?? ''))
    void apiGet<Team[]>('/teams').then(setTeams)
  }, [])

  const onCreateGame = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = new FormData(e.currentTarget)
    await apiPost('/admin/games', {
      home_team_id: form.get('home_team_id'),
      away_team_id: form.get('away_team_id'),
      start_time: form.get('start_time'),
      field: form.get('field'),
      status: 'SCHEDULED',
    }, token)
    setMessage('Game created')
    e.currentTarget.reset()
  }

  const onAnnouncement = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault()
    const form = new FormData(e.currentTarget)
    await apiPost('/admin/announcements', {
      title: form.get('title'),
      body: form.get('body'),
    }, token)
    setMessage('Announcement posted')
    e.currentTarget.reset()
  }

  return (
    <div>
      <h2>Admin Dashboard</h2>
      {!token && <p>You must be logged in.</p>}
      <form onSubmit={onCreateGame} className="card">
        <h3>Create Game</h3>
        <select name="home_team_id" required>{teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select>
        <select name="away_team_id" required>{teams.map((t) => <option key={t.id} value={t.id}>{t.name}</option>)}</select>
        <input type="datetime-local" name="start_time" required />
        <input name="field" placeholder="Field" required />
        <button type="submit">Create Game</button>
      </form>

      <form onSubmit={onAnnouncement} className="card">
        <h3>Post Announcement</h3>
        <input name="title" placeholder="Title" required />
        <textarea name="body" placeholder="Body" required />
        <button type="submit">Post</button>
      </form>

      {message && <p>{message}</p>}
    </div>
  )
}

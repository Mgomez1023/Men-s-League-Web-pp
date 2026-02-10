import { useEffect, useState } from 'react'
import { apiGet } from '../api/client'
import type { Announcement } from '../types'

export function AnnouncementsPage() {
  const [items, setItems] = useState<Announcement[]>([])

  useEffect(() => {
    void apiGet<Announcement[]>('/announcements').then(setItems)
  }, [])

  return (
    <div>
      <h2>Announcements</h2>
      {items.map((a) => (
        <article key={a.id} className="card">
          <h3>{a.title}</h3>
          <small>{new Date(a.created_at).toLocaleString()}</small>
          <p>{a.body}</p>
        </article>
      ))}
    </div>
  )
}

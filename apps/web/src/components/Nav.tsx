import { Link } from 'react-router-dom'

export function Nav() {
  return (
    <nav className="nav">
      <Link to="/">Home</Link>
      <Link to="/schedule">Schedule</Link>
      <Link to="/standings">Standings</Link>
      <Link to="/teams">Teams</Link>
      <Link to="/announcements">Announcements</Link>
      <Link to="/admin/login">Admin</Link>
    </nav>
  )
}

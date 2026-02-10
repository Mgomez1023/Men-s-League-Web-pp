import { Route, Routes } from 'react-router-dom'
import { Nav } from './components/Nav'
import { AdminDashboardPage } from './pages/AdminDashboardPage'
import { AdminLoginPage } from './pages/AdminLoginPage'
import { AnnouncementsPage } from './pages/AnnouncementsPage'
import { HomePage } from './pages/HomePage'
import { SchedulePage } from './pages/SchedulePage'
import { StandingsPage } from './pages/StandingsPage'
import { TeamDetailPage } from './pages/TeamDetailPage'
import { TeamsPage } from './pages/TeamsPage'

export default function App() {
  return (
    <div className="container">
      <h1>Men's Baseball League</h1>
      <Nav />
      <Routes>
        <Route path="/" element={<HomePage />} />
        <Route path="/schedule" element={<SchedulePage />} />
        <Route path="/standings" element={<StandingsPage />} />
        <Route path="/teams" element={<TeamsPage />} />
        <Route path="/teams/:teamId" element={<TeamDetailPage />} />
        <Route path="/announcements" element={<AnnouncementsPage />} />
        <Route path="/admin/login" element={<AdminLoginPage />} />
        <Route path="/admin/dashboard" element={<AdminDashboardPage />} />
      </Routes>
    </div>
  )
}

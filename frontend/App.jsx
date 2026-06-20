import { BrowserRouter, Navigate, Route, Routes } from 'react-router-dom'
import { Toaster } from 'react-hot-toast'
import Navbar from './components/layout/Navbar'
import HQDashboard from './pages/HQDashboard'
import LandingPage from './pages/LandingPage'
import MSLAgent from './pages/MSLAgent'
import PatientCompanion from './pages/PatientCompanion'

function PageShell({ children }) {
  return (
    <div className="min-h-screen bg-slate-50">
      <Navbar />
      {children}
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Toaster
        position="top-right"
        toastOptions={{
          duration: 4000,
          style: { background: '#1e293b', color: '#fff' },
        }}
      />
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route
          path="/msl"
          element={
            <PageShell>
              <MSLAgent />
            </PageShell>
          }
        />
        <Route
          path="/patient"
          element={
            <PageShell>
              <PatientCompanion />
            </PageShell>
          }
        />
        <Route
          path="/dashboard"
          element={
            <PageShell>
              <HQDashboard />
            </PageShell>
          }
        />
        <Route path="*" element={<Navigate to="/" />} />
      </Routes>
    </BrowserRouter>
  )
}

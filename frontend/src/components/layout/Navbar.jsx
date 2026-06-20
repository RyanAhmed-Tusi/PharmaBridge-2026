import { Link, useLocation } from 'react-router-dom'

const navItems = [
  { path: '/msl', label: 'MSL Intelligence', icon: '🎤' },
  { path: '/patient', label: 'Patient Companion', icon: '❤️' },
  { path: '/dashboard', label: 'HQ Dashboard', icon: '📊' },
]

export default function Navbar() {
  const location = useLocation()

  return (
    <nav className="bg-white border-b border-slate-200 shadow-sm sticky top-0 z-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6">
        <div className="flex items-center justify-between h-16">
          <Link to="/" className="flex items-center gap-2">
            <div className="w-8 h-8 bg-blue-900 rounded-lg flex items-center justify-center">
              <span className="text-white font-bold text-sm">PB</span>
            </div>
            <span className="font-bold text-blue-900 text-lg">PharmaBridge</span>
          </Link>

          <div className="flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  location.pathname === item.path
                    ? 'bg-blue-900 text-white'
                    : 'text-slate-600 hover:bg-slate-100'
                }`}
              >
                <span>{item.icon}</span>
                <span className="hidden sm:block">{item.label}</span>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </nav>
  )
}

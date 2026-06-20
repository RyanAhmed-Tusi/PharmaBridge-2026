import { useNavigate } from 'react-router-dom'

const STATS = [
  { value: '$300B', label: 'Lost annually to medication non-adherence' },
  { value: '70%', label: 'of KOL field insights never formally recorded' },
  { value: '2 min', label: 'is all it takes for an MSL to debrief' },
]

const MODULE_CARDS = [
  {
    icon: '🎤',
    title: 'MSL Field Intelligence',
    desc: 'Voice-first debrief. AI-extracted insights. Auto-routed to the right team in minutes.',
  },
  {
    icon: '❤️',
    title: 'Patient Companion',
    desc: 'Daily check-ins that detect the real reason patients stop. Adapts to each person.',
  },
  {
    icon: '🔗',
    title: 'Bridge Layer',
    desc: 'When field and patient data confirm the same signal — automatically surfaced to HQ.',
  },
]

export default function LandingPage() {
  const navigate = useNavigate()

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-950 via-blue-900 to-indigo-900 text-white">
      <div className="flex items-center justify-between px-8 py-6">
        <div className="flex items-center gap-3">
          <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center">
            <span className="text-blue-900 font-black text-lg">PB</span>
          </div>
          <span className="font-bold text-xl">PharmaBridge</span>
        </div>
        <button
          onClick={() => navigate('/dashboard')}
          className="bg-white text-blue-900 px-5 py-2 rounded-lg font-semibold text-sm hover:bg-blue-50 transition-colors"
        >
          HQ Dashboard →
        </button>
      </div>

      <div className="max-w-5xl mx-auto px-8 pt-16 pb-20 text-center">
        <div className="inline-block bg-white/10 backdrop-blur border border-white/20 rounded-full px-4 py-1 text-sm mb-8">
          Autonomous Pharma Intelligence Platform
        </div>

        <h1 className="text-5xl font-black mb-6 leading-tight">
          The answers exist.
          <br />
          They just live in{' '}
          <span className="bg-gradient-to-r from-amber-300 to-orange-400 bg-clip-text text-transparent">
            two separate places.
          </span>
        </h1>

        <p className="text-xl text-blue-200 mb-12 max-w-2xl mx-auto leading-relaxed">
          What doctors tell MSLs in the field. What patients experience at home.
          PharmaBridge connects both streams in real time — automatically.
        </p>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-14">
          {STATS.map((stat) => (
            <div
              key={stat.value}
              className="bg-white/10 backdrop-blur border border-white/20 rounded-2xl p-6"
            >
              <div className="text-4xl font-black text-amber-300 mb-2">
                {stat.value}
              </div>
              <div className="text-sm text-blue-200">{stat.label}</div>
            </div>
          ))}
        </div>

        <div className="flex flex-col sm:flex-row gap-4 justify-center">
          <button
            onClick={() => navigate('/msl')}
            className="bg-white text-blue-900 px-8 py-4 rounded-xl font-bold text-lg hover:bg-blue-50 transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            🎤 MSL Field Intelligence Agent
          </button>
          <button
            onClick={() => navigate('/patient')}
            className="bg-red-800 text-white px-8 py-4 rounded-xl font-bold text-lg hover:bg-red-700 transition-all hover:shadow-xl hover:-translate-y-0.5"
          >
            ❤️ Patient Adherence Companion
          </button>
        </div>
      </div>

      <div className="max-w-5xl mx-auto px-8 pb-20">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
          {MODULE_CARDS.map((card) => (
            <div
              key={card.title}
              className="bg-white/10 backdrop-blur border border-white/20 rounded-2xl p-6"
            >
              <div className="text-3xl mb-4">{card.icon}</div>
              <h3 className="font-bold text-lg mb-2">{card.title}</h3>
              <p className="text-blue-200 text-sm leading-relaxed">{card.desc}</p>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

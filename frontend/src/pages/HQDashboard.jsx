import { useEffect, useState } from 'react'
import {
  CartesianGrid,
  Cell,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from 'recharts'
import toast from 'react-hot-toast'
import InsightCard from '../components/msl/InsightCard'
import {
  useRealtimeAlerts,
  useRealtimeInsights,
  useRealtimeSignals,
} from '../hooks/useSupabaseRealtime'
import { bridgeAPI, patientAPI } from '../services/api'

const BARRIER_COLORS_CHART = [
  '#ef4444',
  '#f97316',
  '#3b82f6',
  '#8b5cf6',
  '#6366f1',
  '#14b8a6',
]
const BARRIER_LABELS = [
  'Side Effect',
  'Cost',
  'Forgetfulness',
  'Belief',
  'Complexity',
  'Access',
]

function buildAdherenceTrend() {
  return Array.from({ length: 12 }, (_, i) => ({
    week: `W${i + 1}`,
    traditional: Math.max(55, 85 - i * 2),
    pharmabridge: Math.max(80, 85 - i * 0.4),
  }))
}

export default function HQDashboard() {
  const { insights, loading: insightsLoading } = useRealtimeInsights()
  const { signals } = useRealtimeSignals()
  const { alerts } = useRealtimeAlerts()
  const [isScanning, setIsScanning] = useState(false)
  const [patients, setPatients] = useState([])

  useEffect(() => {
    patientAPI
      .getPatients()
      .then((res) => setPatients(res.patients || []))
      .catch(() => setPatients([]))
  }, [signals.length, alerts.length])

  const runBridgeScan = async () => {
    setIsScanning(true)
    try {
      const result = await bridgeAPI.runScan()
      if (result.new_signals_detected > 0) {
        toast.success(
          `🔗 ${result.new_signals_detected} new convergent signal(s) detected!`
        )
      } else {
        toast(`Bridge scan complete. No new signals.`, { icon: '🔍' })
      }
    } catch {
      toast.error('Bridge scan failed')
    } finally {
      setIsScanning(false)
    }
  }

  const barrierCounts = BARRIER_LABELS.reduce((acc, l) => {
    acc[l] = 0
    return acc
  }, {})
  patients.forEach((p) => {
    if (barrierCounts[p.primary_barrier] !== undefined) {
      barrierCounts[p.primary_barrier] += 1
    }
  })
  const totalBarriers = Object.values(barrierCounts).reduce((a, b) => a + b, 0)
  const barrierData = BARRIER_LABELS.map((label) => ({
    name: label,
    value: barrierCounts[label] || 0,
  }))
  const hasBarrierData = totalBarriers > 0

  const adherenceTrend = buildAdherenceTrend()

  return (
    <div className="max-w-7xl mx-auto px-4 py-8">
      <div className="flex items-center justify-between mb-8">
        <div>
          <h1 className="text-3xl font-black text-slate-900 mb-2">
            HQ Intelligence Dashboard
          </h1>
          <p className="text-slate-500">
            Real-time view of field intelligence and patient adherence signals.
          </p>
        </div>
        <button
          onClick={runBridgeScan}
          disabled={isScanning}
          className="bg-indigo-900 text-white px-6 py-3 rounded-xl font-bold hover:bg-indigo-800 disabled:opacity-50 flex items-center gap-2"
        >
          {isScanning ? (
            <>
              <span className="w-4 h-4 border-2 border-white border-t-transparent rounded-full animate-spin"></span>
              Scanning...
            </>
          ) : (
            '🔗 Run Bridge Scan'
          )}
        </button>
      </div>

      <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-8">
        {[
          {
            label: 'MSL Insights Today',
            value: insights.length,
            icon: '🎤',
          },
          {
            label: 'Active Signals',
            value: signals.length,
            icon: '🔗',
          },
          {
            label: 'Care Team Alerts',
            value: alerts.length,
            icon: '📋',
          },
          {
            label: 'Urgent Items',
            value: insights.filter((i) => i.urgency === 'Urgent').length,
            icon: '🚨',
          },
        ].map((stat) => (
          <div
            key={stat.label}
            className="bg-white rounded-2xl border border-slate-200 p-5"
          >
            <div className="text-2xl mb-2">{stat.icon}</div>
            <div className="text-3xl font-black text-slate-900">
              {stat.value}
            </div>
            <div className="text-sm text-slate-500 mt-1">{stat.label}</div>
          </div>
        ))}
      </div>

      {signals.length > 0 && (
        <div className="mb-8">
          <h2 className="text-lg font-bold text-slate-800 mb-4 flex items-center gap-2">
            🔗 Convergent Signals
            <span className="bg-red-100 text-red-700 text-xs px-2 py-0.5 rounded-full font-bold">
              {signals.length} Active
            </span>
          </h2>
          <div className="space-y-4">
            {signals.map((signal) => (
              <div
                key={signal.id}
                className="bg-gradient-to-r from-indigo-900 to-blue-900 text-white rounded-2xl p-6 signal-alert"
              >
                <div className="flex items-start justify-between mb-4 flex-wrap gap-2">
                  <div>
                    <div className="flex items-center gap-3 mb-1 flex-wrap">
                      <span className="text-amber-300 font-mono text-sm bg-white/10 px-2 py-0.5 rounded">
                        💊 {signal.drug_name}
                      </span>
                      <span className="bg-white/20 text-xs px-2 py-0.5 rounded font-medium">
                        {signal.signal_type}
                      </span>
                      <span
                        className={`text-xs px-2 py-0.5 rounded font-bold ${
                          signal.confidence === 'High'
                            ? 'bg-green-400 text-green-900'
                            : signal.confidence === 'Medium'
                              ? 'bg-yellow-400 text-yellow-900'
                              : 'bg-slate-400 text-slate-900'
                        }`}
                      >
                        {signal.confidence} Confidence
                      </span>
                    </div>
                    <p className="text-blue-100 text-sm">
                      {signal.signal_summary}
                    </p>
                  </div>
                  {signal.velocity === 'Accelerating' && (
                    <span className="text-red-300 text-sm font-bold animate-pulse">
                      ⬆ Accelerating
                    </span>
                  )}
                </div>

                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                  <div className="bg-white/10 rounded-xl p-3">
                    <div className="text-xs text-blue-200 font-medium mb-1">
                      🎤 MSL Intelligence
                    </div>
                    <p className="text-sm text-white/90">
                      {signal.msl_evidence?.substring(0, 180)}
                      {signal.msl_evidence?.length > 180 ? '...' : ''}
                    </p>
                  </div>
                  <div className="bg-white/10 rounded-xl p-3">
                    <div className="text-xs text-red-200 font-medium mb-1">
                      ❤️ Patient Data
                    </div>
                    <p className="text-sm text-white/90">
                      {signal.patient_evidence?.substring(0, 180)}
                      {signal.patient_evidence?.length > 180 ? '...' : ''}
                    </p>
                  </div>
                </div>

                {signal.recommended_actions && (
                  <div>
                    <div className="text-xs text-blue-200 font-medium mb-2">
                      Recommended Actions:
                    </div>
                    <div className="flex flex-wrap gap-2">
                      {(Array.isArray(signal.recommended_actions)
                        ? signal.recommended_actions
                        : Object.values(signal.recommended_actions || {})
                      ).map((action, i) => (
                        <span
                          key={i}
                          className="bg-white/15 text-xs px-3 py-1 rounded-full"
                        >
                          {i + 1}. {action}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      )}

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 p-6">
          <h3 className="font-bold text-slate-800 mb-4">
            Adherence Trend — Traditional vs PharmaBridge
          </h3>
          <ResponsiveContainer width="100%" height={220}>
            <LineChart data={adherenceTrend}>
              <CartesianGrid strokeDasharray="3 3" stroke="#f1f5f9" />
              <XAxis dataKey="week" tick={{ fontSize: 11 }} />
              <YAxis domain={[50, 100]} tick={{ fontSize: 11 }} />
              <Tooltip />
              <Line
                type="monotone"
                dataKey="traditional"
                stroke="#94a3b8"
                strokeDasharray="5 5"
                name="Traditional App"
                strokeWidth={2}
                dot={false}
              />
              <Line
                type="monotone"
                dataKey="pharmabridge"
                stroke="#1e3a8a"
                name="PharmaBridge"
                strokeWidth={3}
                dot={false}
              />
            </LineChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-2xl border border-slate-200 p-6">
          <h3 className="font-bold text-slate-800 mb-4">Patient Barriers</h3>
          {hasBarrierData ? (
            <>
              <ResponsiveContainer width="100%" height={160}>
                <PieChart>
                  <Pie
                    data={barrierData}
                    cx="50%"
                    cy="50%"
                    innerRadius={40}
                    outerRadius={70}
                    dataKey="value"
                  >
                    {barrierData.map((entry, index) => (
                      <Cell
                        key={index}
                        fill={
                          BARRIER_COLORS_CHART[
                            index % BARRIER_COLORS_CHART.length
                          ]
                        }
                      />
                    ))}
                  </Pie>
                  <Tooltip />
                </PieChart>
              </ResponsiveContainer>
              <div className="space-y-1 mt-2">
                {barrierData.slice(0, 4).map((d, i) => (
                  <div
                    key={d.name}
                    className="flex items-center justify-between text-xs"
                  >
                    <div className="flex items-center gap-2">
                      <div
                        className="w-2 h-2 rounded-full"
                        style={{ background: BARRIER_COLORS_CHART[i] }}
                      ></div>
                      <span className="text-slate-600">{d.name}</span>
                    </div>
                    <span className="font-medium text-slate-700">
                      {d.value}
                    </span>
                  </div>
                ))}
              </div>
            </>
          ) : (
            <div className="text-center text-slate-400 py-12 text-sm">
              No patient barrier data yet
            </div>
          )}
        </div>
      </div>

      <div className="mt-6">
        <h2 className="text-lg font-bold text-slate-800 mb-4">
          Live MSL Intelligence Feed
        </h2>
        {insightsLoading ? (
          <div className="text-center py-8 text-slate-400">Loading...</div>
        ) : insights.length === 0 ? (
          <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
            <p>No insights yet.</p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {insights.slice(0, 6).map((insight) => (
              <InsightCard key={insight.id} insight={insight} />
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

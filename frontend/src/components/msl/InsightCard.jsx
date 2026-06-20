import {
  ConfidenceBadge,
  InsightTypeBadge,
  UrgencyBadge,
} from '../shared/StatusBadge'

const ROUTING_BORDER = {
  Pharmacovigilance: 'border-l-red-500',
  'Medical Affairs': 'border-l-blue-500',
  Commercial: 'border-l-orange-500',
  'R&D': 'border-l-purple-500',
  Regulatory: 'border-l-yellow-500',
}

function timeAgo(dateString) {
  const seconds = Math.floor((new Date() - new Date(dateString)) / 1000)
  if (seconds < 60) return 'just now'
  if (seconds < 3600) return `${Math.floor(seconds / 60)}m ago`
  if (seconds < 86400) return `${Math.floor(seconds / 3600)}h ago`
  return new Date(dateString).toLocaleDateString()
}

export default function InsightCard({ insight }) {
  const routingClass =
    ROUTING_BORDER[insight.routing_target] || 'border-l-slate-400'

  return (
    <div
      className={`bg-white rounded-xl border border-slate-200 border-l-4 ${routingClass} p-5 hover:shadow-md transition-shadow`}
    >
      <div className="flex items-start justify-between gap-3 mb-3">
        <InsightTypeBadge type={insight.insight_type} />
        <div className="flex items-center gap-2">
          <UrgencyBadge urgency={insight.urgency} />
          <ConfidenceBadge confidence={insight.confidence} />
        </div>
      </div>

      <p className="text-slate-800 font-medium mb-3">{insight.description}</p>

      <div className="flex items-center justify-between text-xs text-slate-500 flex-wrap gap-2">
        <div className="flex items-center gap-3 flex-wrap">
          {insight.kol_name && insight.kol_name !== 'Unknown' && (
            <span className="flex items-center gap-1">
              👨‍⚕️ {insight.kol_name}
              {insight.kol_institution && ` · ${insight.kol_institution}`}
            </span>
          )}
          {insight.drug_name && (
            <span className="bg-slate-100 px-2 py-0.5 rounded font-mono">
              💊 {insight.drug_name}
            </span>
          )}
        </div>
        <div className="flex items-center gap-3">
          {insight.routing_target && (
            <span className="text-xs font-medium text-slate-600">
              → {insight.routing_target}
            </span>
          )}
          <span>{timeAgo(insight.created_at)}</span>
        </div>
      </div>
    </div>
  )
}

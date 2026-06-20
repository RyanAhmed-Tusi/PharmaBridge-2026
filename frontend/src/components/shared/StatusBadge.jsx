const CONFIDENCE_STYLES = {
  High: 'bg-green-100 text-green-800 border-green-200',
  Medium: 'bg-yellow-100 text-yellow-800 border-yellow-200',
  Low: 'bg-slate-100 text-slate-600 border-slate-200',
}

const URGENCY_STYLES = {
  Urgent: 'bg-red-100 text-red-800 border-red-200',
  Normal: 'bg-blue-100 text-blue-800 border-blue-200',
  Low: 'bg-slate-100 text-slate-600 border-slate-200',
}

const INSIGHT_TYPE_STYLES = {
  'Safety Observation': 'bg-red-50 text-red-700 border-red-200',
  'Label Question': 'bg-purple-50 text-purple-700 border-purple-200',
  'Competitive Intel': 'bg-orange-50 text-orange-700 border-orange-200',
  'Unmet Need': 'bg-teal-50 text-teal-700 border-teal-200',
  'Evidence Gap': 'bg-indigo-50 text-indigo-700 border-indigo-200',
  Advocacy: 'bg-green-50 text-green-700 border-green-200',
}

export function ConfidenceBadge({ confidence }) {
  const style = CONFIDENCE_STYLES[confidence] || CONFIDENCE_STYLES.Low
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${style}`}
    >
      {confidence} Confidence
    </span>
  )
}

export function UrgencyBadge({ urgency }) {
  const style = URGENCY_STYLES[urgency] || URGENCY_STYLES.Normal
  const icon = urgency === 'Urgent' ? '🚨' : urgency === 'Normal' ? '📋' : '📌'
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium border ${style}`}
    >
      {icon} {urgency}
    </span>
  )
}

export function InsightTypeBadge({ type }) {
  const style =
    INSIGHT_TYPE_STYLES[type] || 'bg-slate-100 text-slate-600 border-slate-200'
  return (
    <span
      className={`inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-semibold border ${style}`}
    >
      {type}
    </span>
  )
}

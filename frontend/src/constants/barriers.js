export const BARRIER_TYPES = [
  {
    key: 'Cost',
    label: 'Cost',
    description: 'Co-pay, affordability, splitting pills',
    color: 'bg-amber-100 text-amber-800',
  },
  {
    key: 'Side Effect',
    label: 'Side Effect',
    description: 'Fatigue, nausea, headache, physical symptoms',
    color: 'bg-red-100 text-red-800',
  },
  {
    key: 'Forgetfulness',
    label: 'Forgetfulness',
    description: 'Missing doses, irregular schedule',
    color: 'bg-blue-100 text-blue-800',
  },
  {
    key: 'Belief',
    label: 'Belief',
    description: 'Feels fine, skeptical of medication',
    color: 'bg-purple-100 text-purple-800',
  },
  {
    key: 'Complexity',
    label: 'Complexity',
    description: 'Multiple pills, confusing schedule',
    color: 'bg-indigo-100 text-indigo-800',
  },
  {
    key: 'Access',
    label: 'Access',
    description: 'Pharmacy distance, transportation, refills',
    color: 'bg-teal-100 text-teal-800',
  },
]

export const BARRIER_COLOR_MAP = BARRIER_TYPES.reduce((acc, b) => {
  acc[b.key] = b.color
  return acc
}, {})
BARRIER_COLOR_MAP['Unknown'] = 'bg-slate-100 text-slate-600'

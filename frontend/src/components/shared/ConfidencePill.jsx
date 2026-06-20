const STYLES = {
  High: 'bg-green-500 text-white',
  Medium: 'bg-yellow-400 text-yellow-900',
  Low: 'bg-slate-300 text-slate-800',
}

export default function ConfidencePill({ confidence }) {
  const style = STYLES[confidence] || STYLES.Low
  return (
    <span
      className={`inline-flex items-center px-2 py-0.5 rounded-full text-xs font-bold ${style}`}
    >
      {confidence}
    </span>
  )
}

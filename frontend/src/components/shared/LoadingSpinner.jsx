export default function LoadingSpinner({ size = 'md', className = '' }) {
  const sizes = {
    sm: 'w-4 h-4 border-2',
    md: 'w-6 h-6 border-2',
    lg: 'w-10 h-10 border-4',
  }
  return (
    <span
      className={`inline-block ${sizes[size] || sizes.md} border-slate-300 border-t-blue-700 rounded-full animate-spin ${className}`}
      role="status"
      aria-label="loading"
    />
  )
}

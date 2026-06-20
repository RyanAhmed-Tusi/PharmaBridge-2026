import { useEffect, useRef, useState } from 'react'

export default function AudioPlayer({ base64Audio, contentType = 'audio/mpeg', autoPlay = true }) {
  const audioRef = useRef(null)
  const [isPlaying, setIsPlaying] = useState(false)

  useEffect(() => {
    if (!base64Audio || !audioRef.current) return
    if (autoPlay) {
      audioRef.current.play().catch(() => {})
    }
  }, [base64Audio, autoPlay])

  if (!base64Audio) return null

  const src = `data:${contentType};base64,${base64Audio}`

  return (
    <audio
      ref={audioRef}
      src={src}
      controls
      onPlay={() => setIsPlaying(true)}
      onPause={() => setIsPlaying(false)}
      className="w-full h-8"
      aria-label={isPlaying ? 'Playing audio' : 'Audio player'}
    />
  )
}

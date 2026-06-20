import { useAudioRecorder } from '../../hooks/useAudioRecorder'

function formatDuration(seconds) {
  const mins = Math.floor(seconds / 60)
  const secs = seconds % 60
  return `${mins}:${secs.toString().padStart(2, '0')}`
}

export default function VoiceRecorder({ onRecordingComplete }) {
  const {
    isRecording,
    audioBlob,
    recordingDuration,
    error,
    startRecording,
    stopRecording,
    resetRecording,
  } = useAudioRecorder()

  const handleSubmit = () => {
    if (audioBlob) {
      onRecordingComplete(audioBlob)
      resetRecording()
    }
  }

  return (
    <div className="bg-white rounded-2xl border border-slate-200 p-8 text-center">
      <h3 className="text-lg font-semibold text-slate-800 mb-2">
        Voice Debrief
      </h3>
      <p className="text-slate-500 text-sm mb-8">
        Speak naturally about your KOL meeting. PharmaBridge will extract and
        classify everything.
      </p>

      {error && (
        <div className="bg-red-50 border border-red-200 text-red-700 rounded-lg p-3 mb-6 text-sm">
          {error}
        </div>
      )}

      <div className="flex flex-col items-center gap-4 mb-8">
        <button
          onClick={isRecording ? stopRecording : startRecording}
          disabled={!!audioBlob}
          className={`w-24 h-24 rounded-full text-white font-bold text-4xl transition-all shadow-lg
            ${
              isRecording
                ? 'bg-red-500 recording-pulse hover:bg-red-600'
                : audioBlob
                  ? 'bg-slate-300 cursor-not-allowed'
                  : 'bg-blue-900 hover:bg-blue-800 hover:shadow-xl hover:-translate-y-0.5'
            }`}
        >
          {isRecording ? '⏹' : audioBlob ? '✓' : '🎤'}
        </button>

        <div className="text-sm font-medium text-slate-600">
          {isRecording ? (
            <span className="text-red-500 animate-pulse">
              ● Recording {formatDuration(recordingDuration)}
            </span>
          ) : audioBlob ? (
            <span className="text-green-600">
              ✓ Recording captured ({formatDuration(recordingDuration)})
            </span>
          ) : (
            'Click to start recording'
          )}
        </div>
      </div>

      {audioBlob && (
        <div className="flex gap-3 justify-center">
          <button
            onClick={resetRecording}
            className="px-5 py-2 rounded-lg border border-slate-300 text-slate-600 hover:bg-slate-50 text-sm font-medium"
          >
            Re-record
          </button>
          <button
            onClick={handleSubmit}
            className="px-6 py-2 rounded-lg bg-blue-900 text-white hover:bg-blue-800 text-sm font-bold"
          >
            Submit Debrief →
          </button>
        </div>
      )}
    </div>
  )
}

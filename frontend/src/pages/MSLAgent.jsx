import { useState } from 'react'
import toast from 'react-hot-toast'
import InsightCard from '../components/msl/InsightCard'
import VoiceRecorder from '../components/msl/VoiceRecorder'
import { useRealtimeInsights } from '../hooks/useSupabaseRealtime'
import { mslAPI } from '../services/api'

export default function MSLAgent() {
  const [mslName, setMslName] = useState('')
  const [mslRegion, setMslRegion] = useState('')
  const [isProcessing, setIsProcessing] = useState(false)
  const [processingStep, setProcessingStep] = useState('')
  const [lastResult, setLastResult] = useState(null)
  const [textTranscript, setTextTranscript] = useState('')
  const [inputMode, setInputMode] = useState('voice')

  const { insights, loading: insightsLoading } = useRealtimeInsights()

  const handleRecordingComplete = async (audioBlob) => {
    if (!mslName.trim()) {
      toast.error('Please enter your name before submitting')
      return
    }

    setIsProcessing(true)
    setLastResult(null)

    try {
      setProcessingStep('Transcribing your voice...')
      const result = await mslAPI.submitDebrief(
        audioBlob,
        mslName,
        mslRegion || 'Unspecified'
      )
      setLastResult(result)
      toast.success(`✅ ${result.insights_extracted} insights extracted!`)
    } catch (err) {
      toast.error(`Error: ${err.message}`)
    } finally {
      setIsProcessing(false)
      setProcessingStep('')
    }
  }

  const handleTextDebrief = async () => {
    if (!mslName.trim()) return toast.error('Please enter your name')
    if (!textTranscript.trim()) return toast.error('Please enter a transcript')

    setIsProcessing(true)
    setLastResult(null)
    try {
      setProcessingStep('Extracting insights with AI...')
      const result = await mslAPI.submitTextDebrief(
        textTranscript,
        mslName,
        mslRegion || 'Unspecified'
      )
      setLastResult(result)
      toast.success(`✅ ${result.insights_extracted} insights extracted!`)
      setTextTranscript('')
    } catch (err) {
      toast.error(`Error: ${err.message}`)
    } finally {
      setIsProcessing(false)
      setProcessingStep('')
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 mb-2">
          MSL Field Intelligence Agent
        </h1>
        <p className="text-slate-500">
          Turn your KOL meeting insights into structured intelligence in 2
          minutes.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        <div className="space-y-6">
          <div className="bg-white rounded-2xl border border-slate-200 p-6">
            <h3 className="font-semibold text-slate-800 mb-4">
              Your Information
            </h3>
            <div className="space-y-3">
              <input
                type="text"
                placeholder="Your name (e.g., James Chen)"
                value={mslName}
                onChange={(e) => setMslName(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
              <input
                type="text"
                placeholder="Your region (e.g., Southeast Asia)"
                value={mslRegion}
                onChange={(e) => setMslRegion(e.target.value)}
                className="w-full border border-slate-200 rounded-lg px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500"
              />
            </div>
          </div>

          <div className="flex gap-2 bg-slate-100 rounded-xl p-1">
            <button
              onClick={() => setInputMode('voice')}
              className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                inputMode === 'voice'
                  ? 'bg-white shadow text-blue-900'
                  : 'text-slate-600'
              }`}
            >
              🎤 Voice Debrief
            </button>
            <button
              onClick={() => setInputMode('text')}
              className={`flex-1 py-2 rounded-lg text-sm font-medium transition-colors ${
                inputMode === 'text'
                  ? 'bg-white shadow text-blue-900'
                  : 'text-slate-600'
              }`}
            >
              📝 Type Transcript
            </button>
          </div>

          {inputMode === 'voice' ? (
            <VoiceRecorder onRecordingComplete={handleRecordingComplete} />
          ) : (
            <div className="bg-white rounded-2xl border border-slate-200 p-6">
              <textarea
                placeholder="Paste or type the meeting transcript here... e.g., 'Dr. Sharma mentioned that two of her patients developed fatigue after starting Drug X. She also asked about the dosing in elderly patients with renal impairment...'"
                value={textTranscript}
                onChange={(e) => setTextTranscript(e.target.value)}
                rows={8}
                className="w-full border border-slate-200 rounded-lg px-4 py-3 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 resize-none"
              />
              <button
                onClick={handleTextDebrief}
                disabled={isProcessing}
                className="mt-3 w-full bg-blue-900 text-white py-3 rounded-lg font-bold hover:bg-blue-800 disabled:opacity-50"
              >
                {isProcessing ? processingStep : 'Extract Insights →'}
              </button>
            </div>
          )}

          {isProcessing && (
            <div className="bg-blue-50 border border-blue-200 rounded-xl p-4 text-center">
              <div className="text-blue-600 font-medium">
                {processingStep || 'Processing...'}
              </div>
              <div className="text-blue-400 text-sm mt-1">
                PharmaBridge AI is working
              </div>
            </div>
          )}

          {lastResult && (
            <div className="bg-green-50 border border-green-200 rounded-xl p-5">
              <div className="flex items-center gap-2 mb-3">
                <span className="text-2xl">✅</span>
                <span className="font-bold text-green-800">
                  Debrief Processed
                </span>
              </div>
              {lastResult.debrief_summary && (
                <p className="text-green-700 text-sm mb-3">
                  {lastResult.debrief_summary}
                </p>
              )}
              <div className="text-green-600 text-sm font-medium">
                {lastResult.insights_extracted} insights extracted and routed →
              </div>
            </div>
          )}
        </div>

        <div>
          <div className="flex items-center justify-between mb-4">
            <h2 className="text-lg font-bold text-slate-800">
              Live Intelligence Feed
            </h2>
            <span className="flex items-center gap-1.5 text-xs text-green-600 font-medium">
              <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
              Real-time
            </span>
          </div>

          {insightsLoading ? (
            <div className="text-center py-12 text-slate-400">
              Loading insights...
            </div>
          ) : insights.length === 0 ? (
            <div className="bg-white rounded-2xl border border-slate-200 p-12 text-center text-slate-400">
              <div className="text-4xl mb-3">📭</div>
              <p>No insights yet. Submit your first debrief to get started.</p>
            </div>
          ) : (
            <div className="space-y-3 max-h-[600px] overflow-y-auto pr-1">
              {insights.map((insight) => (
                <InsightCard key={insight.id} insight={insight} />
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

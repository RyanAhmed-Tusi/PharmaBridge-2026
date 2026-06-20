import { useEffect, useRef, useState } from 'react'
import toast from 'react-hot-toast'
import { patientAPI } from '../services/api'
import { BARRIER_COLOR_MAP } from '../constants/barriers'

function playAudio(base64Audio) {
  try {
    const audio = new Audio(`data:audio/mpeg;base64,${base64Audio}`)
    audio.play().catch(() => {})
  } catch {
    /* autoplay blocked or invalid data — silently ignore */
  }
}

export default function PatientCompanion() {
  const [patients, setPatients] = useState([])
  const [selectedPatient, setSelectedPatient] = useState(null)
  const [messages, setMessages] = useState([])
  const [inputText, setInputText] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [sessionStarted, setSessionStarted] = useState(false)
  const chatEndRef = useRef(null)

  useEffect(() => {
    loadPatients()
  }, [])

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages])

  const loadPatients = async () => {
    try {
      const result = await patientAPI.getPatients()
      setPatients(result.patients || [])
    } catch {
      toast.error('Could not load patients')
    }
  }

  const startSession = async (patient) => {
    setSelectedPatient(patient)
    setMessages([])
    setSessionStarted(false)
    setIsLoading(true)

    try {
      const result = await patientAPI.startSession(patient.id)

      const openingMsg = {
        role: 'companion',
        content: result.opening_message,
        audio: result.audio,
        timestamp: new Date(),
      }
      setMessages([openingMsg])
      setSessionStarted(true)

      if (result.audio?.audio_base64) {
        playAudio(result.audio.audio_base64)
      }
    } catch {
      toast.error('Could not start session')
    } finally {
      setIsLoading(false)
    }
  }

  const sendMessage = async () => {
    if (!inputText.trim() || !selectedPatient || isLoading) return

    const userMsg = {
      role: 'patient',
      content: inputText,
      timestamp: new Date(),
    }
    setMessages((prev) => [...prev, userMsg])

    const userInput = inputText
    setInputText('')
    setIsLoading(true)

    try {
      const history = messages.map((m) => ({
        role: m.role === 'companion' ? 'assistant' : 'user',
        content: m.content,
      }))

      const result = await patientAPI.chat(
        selectedPatient.id,
        userInput,
        history
      )

      const companionMsg = {
        role: 'companion',
        content: result.response_text,
        audio: result.audio,
        barrier: result.detected_barrier,
        alertTriggered: result.alert_triggered,
        timestamp: new Date(),
      }
      setMessages((prev) => [...prev, companionMsg])

      if (result.audio?.audio_base64) {
        playAudio(result.audio.audio_base64)
      }

      if (result.alert_triggered) {
        toast.success('📋 Care team has been notified')
        loadPatients()
      }
    } catch {
      toast.error('Message failed. Try again.')
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <div className="max-w-6xl mx-auto px-4 py-8">
      <div className="mb-8">
        <h1 className="text-3xl font-black text-slate-900 mb-2">
          Patient Adherence Companion
        </h1>
        <p className="text-slate-500">
          Adaptive daily check-ins that detect why patients struggle and adjust
          accordingly.
        </p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        <div className="space-y-3">
          <h2 className="font-bold text-slate-700 text-sm uppercase tracking-wide">
            Enrolled Patients
          </h2>
          {patients.map((patient) => (
            <button
              key={patient.id}
              onClick={() => startSession(patient)}
              className={`w-full text-left bg-white rounded-xl border p-4 hover:shadow-md transition-all ${
                selectedPatient?.id === patient.id
                  ? 'border-blue-500 shadow-md'
                  : 'border-slate-200'
              }`}
            >
              <div className="flex items-start justify-between">
                <div>
                  <div className="font-semibold text-slate-800">
                    {patient.patient_name}
                  </div>
                  <div className="text-xs text-slate-400">
                    {patient.patient_code} · {patient.condition}
                  </div>
                  <div className="text-xs text-slate-500 mt-1">
                    💊 {patient.drug_name}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-sm font-bold text-slate-700">
                    {patient.adherence_rate}%
                  </div>
                  <div className="text-xs text-slate-400">adherence</div>
                </div>
              </div>
              {patient.primary_barrier &&
                patient.primary_barrier !== 'Unknown' && (
                  <div
                    className={`mt-2 inline-block text-xs px-2 py-0.5 rounded-full ${
                      BARRIER_COLOR_MAP[patient.primary_barrier] ||
                      'bg-slate-100 text-slate-600'
                    }`}
                  >
                    {patient.primary_barrier} barrier
                  </div>
                )}
            </button>
          ))}

          {patients.length === 0 && (
            <div className="text-center py-8 text-slate-400 text-sm">
              No patients enrolled yet. Run the demo seed script first.
            </div>
          )}
        </div>

        <div
          className="lg:col-span-2 bg-white rounded-2xl border border-slate-200 flex flex-col"
          style={{ height: '600px' }}
        >
          {!selectedPatient ? (
            <div className="flex-1 flex items-center justify-center text-slate-400">
              <div className="text-center">
                <div className="text-4xl mb-3">❤️</div>
                <p>Select a patient to start their daily check-in</p>
              </div>
            </div>
          ) : (
            <>
              <div className="border-b border-slate-100 px-6 py-4 flex items-center justify-between">
                <div>
                  <div className="font-bold text-slate-800">
                    {selectedPatient.patient_name}
                  </div>
                  <div className="text-xs text-slate-400">
                    {selectedPatient.condition} · {selectedPatient.drug_name}
                  </div>
                </div>
                <div className="text-right">
                  <div className="text-lg font-bold text-slate-700">
                    {selectedPatient.adherence_rate}%
                  </div>
                  <div className="text-xs text-slate-400">adherence</div>
                </div>
              </div>

              <div className="flex-1 overflow-y-auto p-6 space-y-4">
                {messages.map((msg, idx) => (
                  <div
                    key={idx}
                    className={`flex ${
                      msg.role === 'patient' ? 'justify-end' : 'justify-start'
                    }`}
                  >
                    <div
                      className={`max-w-sm rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                        msg.role === 'patient'
                          ? 'bg-blue-600 text-white rounded-br-sm'
                          : 'bg-slate-100 text-slate-800 rounded-bl-sm'
                      }`}
                    >
                      {msg.role === 'companion' && (
                        <div className="text-xs font-semibold text-slate-500 mb-1">
                          Aria · PharmaBridge
                        </div>
                      )}
                      {msg.content}
                      {msg.alertTriggered && (
                        <div className="text-xs text-amber-600 mt-1 font-medium">
                          📋 Care team notified
                        </div>
                      )}
                    </div>
                  </div>
                ))}

                {isLoading && (
                  <div className="flex justify-start">
                    <div className="bg-slate-100 rounded-2xl rounded-bl-sm px-4 py-3">
                      <div className="flex gap-1">
                        <span
                          className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                          style={{ animationDelay: '0ms' }}
                        ></span>
                        <span
                          className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                          style={{ animationDelay: '150ms' }}
                        ></span>
                        <span
                          className="w-2 h-2 bg-slate-400 rounded-full animate-bounce"
                          style={{ animationDelay: '300ms' }}
                        ></span>
                      </div>
                    </div>
                  </div>
                )}
                <div ref={chatEndRef} />
              </div>

              <div className="border-t border-slate-100 p-4 flex gap-3">
                <input
                  type="text"
                  value={inputText}
                  onChange={(e) => setInputText(e.target.value)}
                  onKeyDown={(e) => e.key === 'Enter' && sendMessage()}
                  placeholder="Type your response..."
                  disabled={isLoading || !sessionStarted}
                  className="flex-1 border border-slate-200 rounded-xl px-4 py-2.5 text-sm focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:opacity-50"
                />
                <button
                  onClick={sendMessage}
                  disabled={isLoading || !sessionStarted || !inputText.trim()}
                  className="bg-blue-900 text-white px-5 py-2.5 rounded-xl font-medium text-sm hover:bg-blue-800 disabled:opacity-50"
                >
                  Send
                </button>
              </div>
            </>
          )}
        </div>
      </div>
    </div>
  )
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000'

async function apiCall(endpoint, options = {}) {
  const response = await fetch(`${BASE_URL}${endpoint}`, {
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
    ...options,
  })

  if (!response.ok) {
    const error = await response
      .json()
      .catch(() => ({ detail: 'Unknown error' }))
    throw new Error(error.detail || `API error: ${response.status}`)
  }

  return response.json()
}

export const mslAPI = {
  submitDebrief: async (audioBlob, mslName, mslRegion) => {
    const formData = new FormData()
    formData.append('audio', audioBlob, 'debrief.webm')
    formData.append('msl_name', mslName)
    formData.append('msl_region', mslRegion)

    const response = await fetch(`${BASE_URL}/api/msl/debrief`, {
      method: 'POST',
      body: formData,
    })

    if (!response.ok) {
      const error = await response
        .json()
        .catch(() => ({ detail: 'Debrief submission failed' }))
      throw new Error(error.detail || 'Debrief submission failed')
    }
    return response.json()
  },

  submitTextDebrief: async (transcript, mslName, mslRegion) => {
    return apiCall('/api/msl/debrief/text', {
      method: 'POST',
      body: JSON.stringify({
        transcript,
        msl_name: mslName,
        msl_region: mslRegion,
      }),
    })
  },

  getInsights: async (filters = {}) => {
    const params = new URLSearchParams(filters)
    return apiCall(`/api/msl/insights?${params}`)
  },
}

export const patientAPI = {
  startSession: async (patientId) => {
    return apiCall('/api/patient/start-session', {
      method: 'POST',
      body: JSON.stringify({ patient_id: patientId }),
    })
  },

  chat: async (patientId, message, conversationHistory) => {
    return apiCall('/api/patient/chat', {
      method: 'POST',
      body: JSON.stringify({
        patient_id: patientId,
        message,
        conversation_history: conversationHistory,
        include_audio: true,
      }),
    })
  },

  getPatients: async () => {
    return apiCall('/api/patient/patients')
  },

  getPatientHistory: async (patientId) => {
    return apiCall(`/api/patient/patients/${patientId}/history`)
  },
}

export const bridgeAPI = {
  runScan: async () => {
    return apiCall('/api/bridge/scan', { method: 'POST' })
  },

  getSignals: async () => {
    return apiCall('/api/bridge/signals')
  },

  getAlerts: async () => {
    return apiCall('/api/bridge/alerts')
  },
}

export const transcribeAudio = async (audioBlob) => {
  const formData = new FormData()
  formData.append('audio', audioBlob, 'audio.webm')

  const response = await fetch(`${BASE_URL}/api/transcribe`, {
    method: 'POST',
    body: formData,
  })

  if (!response.ok) throw new Error('Transcription failed')
  return response.json()
}

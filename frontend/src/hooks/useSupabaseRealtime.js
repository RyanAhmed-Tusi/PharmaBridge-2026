import { useEffect, useState } from 'react'
import { supabase } from '../services/supabase'

export function useRealtimeInsights() {
  const [insights, setInsights] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await supabase
        .from('msl_insights')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(20)
      setInsights(data || [])
      setLoading(false)
    }
    fetchInitial()

    const channel = supabase
      .channel('msl-insights-channel')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'msl_insights',
        },
        (payload) => {
          setInsights((prev) => [payload.new, ...prev])
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [])

  return { insights, loading }
}

export function useRealtimeSignals() {
  const [signals, setSignals] = useState([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await supabase
        .from('convergent_signals')
        .select('*')
        .eq('status', 'Active')
        .order('created_at', { ascending: false })
      setSignals(data || [])
      setLoading(false)
    }
    fetchInitial()

    const channel = supabase
      .channel('signals-channel')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'convergent_signals',
        },
        (payload) => {
          setSignals((prev) => [payload.new, ...prev])
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [])

  return { signals, loading }
}

export function useRealtimeAlerts() {
  const [alerts, setAlerts] = useState([])

  useEffect(() => {
    const fetchInitial = async () => {
      const { data } = await supabase
        .from('care_team_alerts')
        .select('*')
        .order('created_at', { ascending: false })
        .limit(10)
      setAlerts(data || [])
    }
    fetchInitial()

    const channel = supabase
      .channel('alerts-channel')
      .on(
        'postgres_changes',
        {
          event: 'INSERT',
          schema: 'public',
          table: 'care_team_alerts',
        },
        (payload) => {
          setAlerts((prev) => [payload.new, ...prev])
        }
      )
      .subscribe()

    return () => {
      supabase.removeChannel(channel)
    }
  }, [])

  return { alerts }
}

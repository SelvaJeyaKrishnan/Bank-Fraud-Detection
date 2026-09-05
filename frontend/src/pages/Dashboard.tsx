import React, { useEffect, useState } from 'react'
import Sidebar from '@/components/Sidebar'
import StatusCard from '@/components/StatusCard'
import RiskScore from '@/components/RiskScore'
import FindingCard from '@/components/FindingCard'
import { useDispatch, useSelector } from 'react-redux'
import { RootState, AppDispatch } from '@/store'
import { uploadTransactions, analyzeHistory, getReport } from '@/services/api'

interface DashboardProps {
  match: { reportId: string }
}

export default function Dashboard({ match }: DashboardProps) {
  const dispatch = useDispatch()
  const [reportId, setReportId] = useState<string>('')
  const [status, setStatus] = useState<'no_activity' | 'investigation' | 'pending'>('pending')
  const [riskScore, setRiskScore] = useState(0)
  const [findings, setFindings] = useState<Array<any>>([])
  const [behavior, setBehavior] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  // Load report data
  useEffect(() => {
    const loadReport = async () => {
      setLoading(true)
      try {
        const response = await fetch(`/api/report/${match.reportId}`)
        const data = await response.json()
        
        setReportId(data.report_id || match.reportId)
        setStatus(data.overall_finding === '⚠️ Activity Requiring Investigation' ? 'investigation' : 'no_activity')
        setRiskScore(data.risk_score || 0)
        setFindings(data.investigation_findings || [])
        setBehavior(data.behavior_profile || null)
      } catch (error) {
        console.error('Failed to load report:', error)
      } finally {
        setLoading(false)
      }
    }
    
    if (match.reportId) {
      loadReport()
    }
  }, [match.reportId, dispatch])

  // Upload transactions
  const handleUpload = async (file: File) => {
    setLoading(true)
    try {
      const formData = new FormData()
      formData.append('file', file)
      
      const response = await fetch('/api/upload', {
        method: 'POST',
        body: formData,
      })
      
      const result = await response.json()
      
      if (result.status === 'success') {
        // Auto-analyze after upload
        await analyzeHistoryDispatched(result.data)
      }
    } catch (error) {
      console.error('Upload failed:', error)
    } finally {
      setLoading(false)
    }
  }

  const analyzeHistoryDispatched = async (data: any) => {
    setLoading(true)
    try {
      const response = await fetch('/api/initialize-analysis', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ transactions: data.transactions }),
      })
      
      const result = await response.json()
      
      setReportId(result.report_id || '')
      setStatus(result.overall_finding === '⚠️ Activity Requiring Investigation' ? 'investigation' : 'no_activity')
      setRiskScore(result.risk_score || 0)
      setFindings(result.findings || [])
      setBehavior(result.behavior_profile || null)
    } catch (error) {
      console.error('Analysis failed:', error)
    } finally {
      setLoading(false)
    }
  }

  if (!reportId && !behavior) {
    return (
      <div className="min-h-screen bg-[#0a0a0f]">
        <Sidebar />
        <div className="p-6">
          <h1 className="text-3xl font-bold text-white mb-4">Sentinel AI</h1>
          <p className="text-[#6b6b80] mb-8">Transaction Investigation Assistant</p>
          
          <UploadPanel onUpload={handleUpload} />
        </div>
      </div>
    )
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <Sidebar />
      <main className="flex-1 p-6">
        <StatusCard 
          finding={status} 
          riskScore={riskScore} 
        />
        
        <RiskScore 
          score={riskScore} 
          level={riskScore > 60 ? 'High' : riskScore > 30 ? 'Medium' : 'Low'} 
          contributions={[
            { name: 'Large Transfer', score: 30 },
            { name: 'New Payee Burst', score: 25 },
            { name: 'Odd Hours', score: 20 },
          ]} 
        />
        
        {status === 'investigation' && findings.length > 0 && (
          <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
            {findings.slice(0, 4).map((finding: any) => (
              <FindingCard key={finding.finding_number} finding={finding} />
            ))}
          </div>
        )}
        
        {status === 'no_activity' && (
          <div className="mt-8 p-6 bg-[#1e1e2a] rounded-2xl">
            <h3 className="text-xl font-medium mb-3">No Activity Requiring Attention</h3>
            <p className="text-[#6b6b80]">
              No activity requiring attention was identified based on the configured risk rules 
              and the customer's established transaction behavior.
            </p>
            <p className="text-sm text-[#6b6b80] mt-2">
              Investigation Priority Score: {riskScore}/100
            </p>
          </div>
        )}
      </main>
    </div>
  )
}
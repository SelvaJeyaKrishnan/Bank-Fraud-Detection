import React from 'react'
import Sidebar from '@/components/Sidebar'
import { useParams } from 'react-router-dom'
import FindingCard from '@/components/FindingCard'

export default function Investigation() {
  const { reportId } = useParams<{ reportId: string }>()

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <Sidebar />
      <main className="flex-1 p-6">
        <h2 className="text-2xl font-bold text-white mb-6">Investigation Report</h2>
        
        {reportId && (
          <div className="bg-[#12121a] rounded-2xl border border-[#1e1e2a] p-6">
            <h3 className="text-lg font-medium mb-4">Report ID: {reportId}</h3>
            
            {/* Overall finding summary would go here */}
            
            {reportId === 'REPORT-20240101-120000' && (
              <FindingCard finding={{
                finding_number: 1,
                rule_triggered: 'Unusually Large Transfer',
                risk_level: 'High',
                priority_score: 75,
                transactions: [
                  { transaction_id: 'TXN-2', date: '2024-01-15', time: '14:00', description: 'Large transfer', payee: 'Unknown Payee', amount: 50000, channel: 'Bank Transfer' }
                ],
                why_flagged: "Transaction TXN-1024 for ₹250,000 is significantly above the customer's typical transaction range of ₹2,000–₹15,000.",
                normal_behaviour: 'Previous transfers typically ranged between ₹2,000 and ₹15,000.',
                connected_activity: [],
                investigator_questions: [
                  'Was the transaction authorized?',
                  'Is the payee known to the customer?',
                  'Was the device or login behavior unusual?',
                  'Were there other transactions immediately before or after the activity?'
                ]
              }} />
            )}
          </div>
        )}
      </main>
    </div>
  )
}
import React from 'react'

interface StatusCardProps {
  finding: 'no_activity' | 'investigation' | 'pending'
  riskScore: number
}

const StatusCard: React.FC<StatusCardProps> = ({ finding, riskScore }) => {
  const isInvestigation = finding === 'investigation'
  
  return (
    <div className="bg-[#12121a] rounded-2xl border border-[#1e1e2a] p-6 mb-6">
      <div className="flex items-center justify-between">
        <div>
          <h3 className="text-lg font-medium text-[#aaa] mb-2">Overall Status</h3>
          <div className="flex items-center gap-3">
            <span className={`text-3xl font-bold ${
              isInvestigation ? 'text-[#ff4756]' : 'text-[#00d4aa]'
            }`}>
              {isInvestigation ? '🔴' : '🟢'}
            </span>
            <span>
              {isInvestigation 
                ? 'Activity Requiring Investigation' 
                : 'No Activity Requiring Attention'}
            </span>
          </div>
        </div>
        <div className="text-right">
          <p className="text-sm text-[#6b6b80] mb-1">Investigation Priority Score</p>
          <p className="text-2xl font-bold ${
            riskScore > 60 ? 'text-[#ff4756]' : riskScore > 30 ? 'text-[#ffa502]' : 'text-[#00d4aa]'
          }">{riskScore}/100</p>
        </div>
      </div>
    </div>
  )
}

export default StatusCard
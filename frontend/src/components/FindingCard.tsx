import React from 'react'

interface Transaction {
  transaction_id: string
  date: string
  time: string | null
  description: string
  payee: string
  amount: number
  channel: string
}

interface FindingCardProps {
  finding: {
    finding_number: number
    rule_triggered: string
    risk_level: string
    priority_score: number
    transactions: Transaction[]
    why_flagged: string
    normal_behaviour: string
    connected_activity: Transaction[]
    investigator_questions: string[]
  }
}

const FindingCard: React.FC<FindingCardProps> = ({ finding }) => {
  const handleViewDetails = () => {
    // Navigate to transaction details
  }
  
  return (
    <div className="bg-[#12121a] rounded-2xl border border-[#1e1e2a] mb-4 overflow-hidden">
      <div className="px-5 py-3 border-b border-[#1e1e2a] flex items-center justify-between">
        <div>
          <h4 className="font-medium text-lg">{finding.rule_triggered}</h4>
          <p className="text-sm text-[#6b6b80]">{finding.normal_behaviour}</p>
        </div>
        
        <span className={`px-3 py-1 rounded text-xs font-semibold ${
          finding.risk_level === 'High' ? 'bg-[#ff4756] text-white' :
          finding.risk_level === 'Medium' ? 'bg-[#ffa502] text-black' :
          'bg-[#00d4aa] text-black'
        }`}>
          {finding.risk_level} PRIORITY
        </span>
      </div>
      
      <div className="px-5 py-4">
        <div className="grid grid-cols-2 gap-3 mb-4">
          {finding.transactions.map((txn, idx) => (
            <div key={idx} className="bg-[#1e1e2a] rounded-xl p-3">
              <p className="text-xs text-[#6b6b80] mb-1">{txn.description}</p>
              <p className="font-medium">{'₹' + txn.amount.toLocaleString()}</p>
              <p className="text-caption text-xs">{txn.channel}</p>
            </div>
          ))}
        </div>
        
        <p className="text-sm text-[#aaa] mb-3">{finding.why_flagged}</p>
        
        <div>
          <h5 className="text-xs font-medium text-[#6b6b80] mb-2">Investigator Questions</h5>
          <ul className="text-xs text-[#aaa] space-y-1">
            {finding.investigator_questions.map((question, i) => (
              <li key={i}>{question}</li>
            ))}
          </ul>
        </div>
      </div>
      
      <div className="px-5 py-3 border-t border-[#1e1e2a] flex items-center justify-between">
        <small className="text-xs text-[#6b6b80]">
          Transactions {finding.finding_number} of {finding.transactions.length}+
        </small>
        <button className="text-[#00d4aa] text-sm hover:underline">
          View Investigation Details
        </button>
      </div>
    </div>
  )
}

export default FindingCard
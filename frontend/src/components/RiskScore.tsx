import React from 'react'

interface RiskScoreProps {
  score: number
  level: 'Low' | 'Medium' | 'High'
  contributions: Array<{ name: string; score: number }>
}

const RiskScore: React.FC<RiskScoreProps> = ({ score, level, contributions }) => {
  const levelColors = {
    Low: 'text-[#00d4aa]',
    Medium: 'text-[#ffa502]', 
    High: 'text-[#ff4756]'
  }

  return (
    <div className="bg-[#12121a] rounded-2xl border border-[#1e1e2a] p-6">
      <div className="flex items-center gap-3 mb-4">
        <div className="w-12 h-12 rounded-xl bg-opacity-50 bg-[#1e1e2a] flex items-center justify-center">
          <span className={`text-3xl font-bold ${levelColors[level]}`}>
            {score}
          </span>
        </div>
        <div>
          <p className="text-lg font-medium">{level}</p>
          <p className="text-sm text-[#6b6b80]">Investigation Priority</p>
        </div>
      </div>
      
      <div className="space-y-2">
        {contributions.map((contrib, index) => (
          <div key={index} className="flex justify-between text-sm">
            <span className="text-[#aaa]">{contrib.name}</span>
            <span className="text-[#00d4aa]">{contrib.score}</span>
          </div>
        ))}
      </div>
      
      <div className="mt-4 pt-3 border-t border-[#1e1e2a]">
        <small className="text-[#6b6b80]">
          Score components contribute to Investigation Priority. Final decision with human investigator.
        </small>
      </div>
    </div>
  )
}

export default RiskScore
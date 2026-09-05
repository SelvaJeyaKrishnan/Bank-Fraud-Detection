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

interface TransactionTableProps {
  transactions: Transaction[]
  filteredTransactions: Transaction[]
  onTransactionSelect: (txn: Transaction) => void
}

const TransactionTable: React.FC<TransactionTableProps> = ({ 
  transactions, 
  filteredTransactions, 
  onTransactionSelect 
}) => {
  return (
    <div className="bg-[#12121a] rounded-2xl border border-[#1e1e2a] overflow-hidden">
      <div className="px-5 py-4 border-b border-[#1e1e2a]">
        <h3 className="font-medium text-lg">Transaction History</h3>
        <span className="text-sm text-[#6b6b80]">{filteredTransactions.length} of {transactions.length} transactions</span>
      </div>
      
      <div className="px-5 pb-5">
        <table className="w-full">
          <thead>
            <tr className="text-xs text-[#6b6b80] border-b border-[#1e1e2a]">
              <th style={{ width: '15%' }}>Date</th>
              <th style={{ width: '10%' }}>Time</th>
              <th style={{ width: '30%' }}>Description</th>
              <th style={{ width: '15%' }}>Payee</th>
              <th style={{ width: '10%' }}>Amount</th>
              <th style={{ width: '15%' }}>Channel</th>
              <th style={{ width: '5%' }}></th>
            </tr>
          </thead>
          <tbody>
            {filteredTransactions.map((txn, idx) => {
              const txnData = transactions.find(t => t.transaction_id === txn.transaction_id)
              return (
                <tr 
                  key={idx}
                  className="hover:bg-[#1e1e2a]"
                  onClick={() => onTransactionSelect(txnData || txn)}
                >
                  <td>{txn.date.split('T')[0]}</td>
                  <td>{txn.time || '-'}</td>
                  <td className="font-medium">{txn.description}</td>
                  <td>{txn.payee}</td>
                  <td>{'₹' + txn.amount.toLocaleString()}</td>
                  <td>{txn.channel}</td>
                  <td>
                    <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                      <path d="M10 9L9 20H5v-5a5 5 0 015-5h2z"/>
                      <line x1="9" y1="20" x2="15" y2="20"/>
                      <line x1="15" y1="9" x2="21" y2="9"/>
                    </svg>
                  </td>
                </tr>
              )
            })}
          </tbody>
        </table>
      </div>
    </div>
  )
}

export default TransactionTable
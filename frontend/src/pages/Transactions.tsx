import React, { useState, useEffect } from 'react'
import { useSelector } from 'react-redux'
import Sidebar from '@/components/Sidebar'
import TransactionTable from '@/components/TransactionTable'
import { RootState } from '@/store'

interface Transaction {
  transaction_id: string
  date: string
  time: string | null
  description: string
  payee: string
  amount: number
  channel: string
}

export default function Transactions() {
  const [transactions, setTransactions] = useState<Transaction[]>([])
  const [filteredTransactions, setFilteredTransactions] = useState<Transaction[]>([])
  const [searchTerm, setSearchTerm] = useState('')
  const [selectedTxn, setSelectedTxn] = useState<Transaction | null>(null)
  useSelector((state: RootState) => state.transactions)

  // Load transactions from backend or store
  useEffect(() => {
    const loadTransactions = async () => {
      try {
        const response = await fetch('/api/transactions')
        const data = await response.json()
        setTransactions(data.transactions || [])
        setFilteredTransactions(data.transactions || [])
      } catch (error) {
        console.error('Failed to load transactions:', error)
      }
    }
    
    loadTransactions()
  }, [])

  const handleSearch = (e: React.ChangeEvent<HTMLInputElement>) => {
    const term = e.target.value.toLowerCase()
    setSearchTerm(term)
    
    const filtered = transactions.filter((txn) =>
      txn.description.toLowerCase().includes(term) ||
      txn.payee.toLowerCase().includes(term) ||
      txn.channel.toLowerCase().includes(term) ||
      txn.amount.toString().includes(term)
    )
    setFilteredTransactions(filtered)
  }

  const handleFilterByChannel = (channel: string) => {
    if (channel === 'All') {
      setFilteredTransactions(transactions)
    } else {
      setFilteredTransactions(transactions.filter((txn) => txn.channel === channel))
    }
  }

  const handleSelectTransaction = (txn: Transaction) => {
    setSelectedTxn(txn)
    // Navigate to details or show modal
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <Sidebar />
      <main className="flex-1 p-6">
        <div className="mb-6">
          <h2 className="text-2xl font-bold text-white mb-4">Transaction Explorer</h2>
          
          <div className="grid grid-cols-1 gap-3 md:grid-cols-4">
            <input
              type="text"
              placeholder="Search transactions..."
              value={searchTerm}
              onChange={handleSearch}
              className="bg-[#1e1e2a] border border-[#1e1e2a] rounded-lg px-3 py-2 text-white focus:outline-none focus:border-[#00d4aa]"
            />
            <select
              onChange={(e) => handleFilterByChannel(e.target.value)}
              className="bg-[#1e1e2a] border border-[#1e1e2a] rounded-lg px-3 py-2 text-white"
            >
              <option value="All">Filter by Channel</option>
              <option value="Card">Card</option>
              <option value="UPI">UPI</option>
              <option value="Bank Transfer">Bank Transfer</option>
              <option value="ATM">ATM</option>
              <option value="Online Banking">Online Banking</option>
              <option value="Mobile Banking">Mobile Banking</option>
            </select>
          </div>
        </div>
        
        <TransactionTable
          transactions={transactions}
          filteredTransactions={filteredTransactions}
          onTransactionSelect={handleSelectTransaction}
        />
        
        {selectedTxn && (
          <div className="mt-6 p-4 bg-[#1e1e2a] rounded-xl">
            <h3 className="text-xl font-bold mb-3">Transaction Details</h3>
            <div className="grid grid-cols-2 gap-4">
              <div>
                <p className="text-sm text-[#6b6b80] mb-1">Transaction ID</p>
                <p className="font-medium">{selectedTxn.transaction_id}</p>
              </div>
              <div>
                <p className="text-sm text-[#6b6b80] mb-1">Amount</p>
                <p className="font-medium">{'₹' + selectedTxn.amount.toLocaleString()}</p>
              </div>
              <div>
                <p className="text-sm text-[#6b6b80] mb-1">Date</p>
                <p className="font-medium">{selectedTxn.date}</p>
              </div>
              <div>
                <p className="text-sm text-[#6b6b80] mb-1">Time</p>
                <p className="font-medium">{selectedTxn.time || 'Not specified'}</p>
              </div>
              <div>
                <p className="text-sm text-[#6b6b80] mb-1">Payee</p>
                <p className="font-medium">{selectedTxn.payee}</p>
              </div>
              <div>
                <p className="text-sm text-[#6b6b80] mb-1">Channel</p>
                <p className="font-medium">{selectedTxn.channel}</p>
              </div>
            </div>
          </div>
        )}
      </main>
    </div>
  )
}
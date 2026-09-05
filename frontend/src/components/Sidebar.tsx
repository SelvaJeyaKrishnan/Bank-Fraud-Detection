import React from 'react'
import { Link } from 'react-router-dom'

const Sidebar: React.FC = () => {
  return (
    <nav className="bg-[#12121a] min-h-screen border-right border-[#1e1e2a]">
      <div className="p-6">
        <h2 className="text-2xl font-bold text-[#00d4aa] mb-6">Sentinel AI</h2>
        <p className="text-[#6b6b80] text-sm mb-8">Transaction Investigation Assistant</p>
        
        <ul className="space-y-2">
          <li>
            <Link to="/" className="flex items-center px-4 py-3 rounded-lg hover:bg-[#1e1e2a] text-white font-medium transition-colors">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <rect x="3" y="3" width="18" height="18" rx="2"/>
                <line x1="3" y1="9" x2="21" y2="9"/>
                <line x1="9" y1="21" x2="9" y2="21"/>
              </svg>
              Dashboard
            </Link>
          </li>
          <li>
            <Link to="/upload" className="flex items-center px-4 py-3 rounded-lg hover:bg-[#1e1e2a] text-[#6b6b80] transition-colors">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
                <polyline points="17 3 21 3 21 7"/>
                <polyline points="7 21 3 21 3 17"/>
                <line x1="3" y1="7" x2="21" y2="7"/>
              </svg>
              Upload History
            </Link>
          </li>
          <li>
            <Link to="/investigation" className="flex items-center px-4 py-3 rounded-lg hover:bg-[#1e1e2a] text-[#6b6b80] transition-colors">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <path d="M10 2a1 1 0 011 1v2a1 1 0 11-2 0V3a1 1 0 011-1zm4 6a3 3 0 013 3h2a3 3 0 010 6h-2a3 3 0 01-3-3v-2zm-4 0a3 3 0 003 3h2a3 3 0 000 6h-2a3 3 0 00-3-3v-2zm4-17a3 3 0 013 3h2a3 3 0 010 6h-2a3 3 0 01-3-3v-2zm-4 0a3 3 0 003 3h2a3 3 0 000 6h-2a3 3 0 00-3-3v-2z"/>
              </svg>
              Investigation
            </Link>
          </li>
          <li>
            <Link to="/transactions" className="flex items-center px-4 py-3 rounded-lg hover:bg-[#1e1e2a] text-[#6b6b80] transition-colors">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
                <circle cx="9" cy="21" r="1"/>
                <circle cx="20" cy="21" r="1"/>
                <path d="M1 1l4 1l9-5l9 5l5-9L21 4l-5 9L3 22l5-9z"/>
              </svg>
              Transactions
            </Link>
          </li>
        </ul>
      </div>
    </nav>
  )
}

export default Sidebar
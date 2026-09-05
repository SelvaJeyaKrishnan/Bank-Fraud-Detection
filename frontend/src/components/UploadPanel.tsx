import React, { useState } from 'react'
import { useNavigate } from 'react-router-dom'

interface UploadPanelProps {
  onUpload: (file: File) => void
}

const UploadPanel: React.FC<UploadPanelProps> = ({ onUpload }) => {
  const navigate = useNavigate()
  const [fileName, setFileName] = useState<string>('')

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setFileName(file.name)
      onUpload(file)
    }
  }

  return (
    <div className="bg-[#12121a] rounded-2xl border border-[#1e1e2a] p-6 max-w-md">
      <h3 className="text-lg font-medium mb-4">Upload Transaction History</h3>
      
      <div className="border-2 dashed border-[#1e1e2a] rounded-xl p-12 text-center mb-6 cursor-pointer hover:border-[#00d4aa] transition-colors"
          onClick="document.getElementById('file-input').click()">
        <svg width="40" height="40" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M21 15v4a2 2 0 01-2 2H5a2 2 0 01-2-2v-4"/>
          <polyline points="17 3 21 3 21 7"/>
          <polyline points="7 21 3 21 3 17"/>
          <line x1="3" y1="7" x2="21" y2="7"/>
        </svg>
        <p className="mt-2 text-[#6b6b80]">Drag and drop or browse files</p>
        <p className="text-xs text-[#aaa]">CSV or Excel (.xlsx) format</p>
      </div>
      
      <input type="file" id="file-input" accept=".csv,.xlsx" style={{ display: 'none' }} onChange={handleFileChange} />
      
      {fileName && (
        <div className="mt-4 p-3 bg-[#1e1e2a] rounded-xl">
          <p className="text-[#00d4aa] mb-1">Selected: {fileName}</p>
          <p className="text-xs text-[#6b6b80]">CSV: Date, Description, Payee, Amount, Channel</p>
          <p className="text-xs text-[#6b6b80]">Optional: Transaction ID, Time</p>
        </div>
      )}
    </div>
  )
}

export default UploadPanel
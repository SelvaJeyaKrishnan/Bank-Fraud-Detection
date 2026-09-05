import React, { useState } from 'react'
import Sidebar from '@/components/Sidebar'
import UploadPanel from '@/components/UploadPanel'

export default function Upload() {
  const [file, setFile] = useState<File | null>(null)

  const handleUpload = async (file: File) => {
    setFile(file)
    // Will be processed by backend
    const formData = new FormData()
    formData.append('file', file)
    
    // TODO: Call API to upload and analyze
  }

  return (
    <div className="min-h-screen bg-[#0a0a0f]">
      <Sidebar />
      <main className="flex-1 p-6 max-w-2xl mx-auto">
        <h1 className="text-3xl font-bold text-white mb-4">Upload Transaction History</h1>
        <p className="text-[#6b6b80] mb-6">Upload a CSV or Excel file containing the customer's transaction history.</p>
        
        <UploadPanel onUpload={handleUpload} />
      </main>
    </div>
  )
}
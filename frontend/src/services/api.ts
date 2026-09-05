import axios from 'axios'

const API_BASE = 'http://localhost:8000/api'

export const uploadTransactions = async (file: File) => {
  const formData = new FormData()
  formData.append('file', file)
  
  const response = await axios.post(`${API_BASE}/upload`, formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  })
  
  return response.data
}

export const analyzeHistory = async (reportId: string) => {
  const response = await axios.get(`${API_BASE}/analyze`, {
    params: { report_id: reportId },
  })
  
  return response.data
}

export const getReport = async (reportId: string) => {
  const response = await axios.get(`${API_BASE}/report/${reportId}`)
  
  return response.data
}

export const getTransactions = async () => {
  const response = await axios.get(`${API_BASE}/transactions`)
  
  return response.data
}

export const getCustomerProfile = async () => {
  const response = await axios.get(`${API_BASE}/customer-profile`)
  
  return response.data
}

export const initializeAnalysis = async (transactions: any[]) => {
  const response = await axios.post(`${API_BASE}/initialize-analysis`, { transactions })
  
  return response.data
}

export default {
  uploadTransactions,
  analyzeHistory,
  getReport,
  getTransactions,
  getCustomerProfile,
  initializeAnalysis,
}
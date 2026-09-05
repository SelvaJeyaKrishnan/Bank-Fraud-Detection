import React from 'react'
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom'
import { Provider } from 'react-redux'
import { store } from './store'
import Dashboard from './pages/Dashboard'
import Upload from './pages/Upload'
import Investigation from './pages/Investigation'
import Transactions from './pages/Transactions'

function Root() {
  return (
    <Router>
      <Provider store={store}>
        <Routes>
          <Route path="/" element={<Dashboard />} />
          <Route path="/upload" element={<Upload />} />
          <Route path="/investigation/:reportId" element={<Investigation />} />
          <Route path="/transactions" element={<Transactions />} />
        </Routes>
      </Provider>
    </Router>
  )
}

export default Root
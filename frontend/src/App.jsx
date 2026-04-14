
import { BrowserRouter as Router, Routes, Route } from "react-router-dom"
import ProtectedRoute from "./components/ProtectedRoute"
import Navbar from "./components/Navbar"
import MainLayout from "./components/MainLayout"

import Dashboard from "./pages/Dashboard"
import Login from "./pages/Login"
import Register from "./pages/Register"
import LoginSuccess from "./pages/LoginSuccess"
import GoogleSuccess from "./pages/GoogleSuccess"

import FingerprintPrediction from "./pages/FingerprintPrediction"
import MedicalReportAI from "./pages/MedicalReportAI"
import HealthRiskPrediction from "./pages/HealthRiskPrediction"
import BloodDonation from "./pages/BloodDonation"

import AdminAnalytics from "./pages/AdminAnalytics"
import RetinaScan from "./pages/RetinaScan"

import Welcome from "./pages/Welcome"   // ✅ ADD THIS

function App() {

  return (

    <Router>

      <Routes>

        {/* 🔥 WITHOUT SIDEBAR (Auth + Welcome Page) */}
        <Route path="/" element={<Welcome />} />   {/* ✅ NEW */}
        <Route path="/login" element={<><Navbar /><Login /></>} />
        <Route path="/register" element={<><Navbar /><Register /></>} />
        <Route path="/login-success" element={<LoginSuccess />} />
        <Route path="/google-success" element={<GoogleSuccess />} />

        {/* 🔥 WITH SIDEBAR (Main App) */}
        <Route element={<MainLayout />}>

          {/* ❌ REMOVE Dashboard from "/" */}
         <Route 
  path="/dashboard" 
  element={
    <ProtectedRoute>
      <Dashboard />
    </ProtectedRoute>
  } 
/>

          <Route path="/fingerprint" element={<FingerprintPrediction />} />
          <Route path="/medical-report-ai" element={<MedicalReportAI />} />
          <Route path="/health-risk" element={<HealthRiskPrediction />} />
          <Route path="/blood-donation" element={<BloodDonation />} />
          <Route path="/retina-scan" element={<RetinaScan />} />
          <Route path="/admin-analytics" element={<AdminAnalytics />} />

        </Route>

      </Routes>

    </Router>

  )
}

export default App
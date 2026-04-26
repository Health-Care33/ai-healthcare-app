import { useEffect, useState } from "react"
import axios from "axios"
import { Users, Fingerprint, FileText, HeartPulse, Eye } from "lucide-react"

import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid
} from "recharts"

export default function AdminAnalytics() {

  const [data, setData] = useState({
    total_users: 0,
    fingerprint_predictions: 0,
    medical_reports: 0,
    blood_checks: 0,
    retinal_scans: 0
  })

  useEffect(() => {

    const fetchAnalytics = async () => {

      try {

       const res = await axios.get("https://ai-healthcare-backend-psnj.onrender.com/api/admin/analytics")


        setData(res.data)

      } catch (error) {

        console.log(error)

      }

    }

    fetchAnalytics()

  }, [])

  // 🔥 CHART DATA
  const chartData = [
    { name: "Fingerprint", value: data.fingerprint_predictions },
    { name: "Medical", value: data.medical_reports },
    { name: "Blood", value: data.blood_checks },
    { name: "Retinal", value: data.retinal_scans }
  ]

  return (

    <div className="min-h-screen bg-slate-950 text-white">

      {/* HEADER */}

      <div className="bg-gradient-to-r from-indigo-600 to-purple-700 p-10 shadow-xl">

        <h1 className="text-4xl font-bold mb-2">
          Admin Analytics Dashboard
        </h1>

        <p className="text-indigo-100">
          Monitor AI Healthcare System Activity
        </p>

      </div>

      {/* STATS GRID */}

      <div className="p-10 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">

        <div className="bg-slate-900 rounded-xl p-8 shadow-lg hover:scale-105 transition">
          <div className="flex items-center justify-between mb-4">
            <Users size={35} className="text-indigo-400"/>
            <span className="text-sm text-gray-400">Registered Users</span>
          </div>
          <h2 className="text-4xl font-bold text-indigo-400">
            {data.total_users}
          </h2>
        </div>

        <div className="bg-slate-900 rounded-xl p-8 shadow-lg hover:scale-105 transition">
          <div className="flex items-center justify-between mb-4">
            <Fingerprint size={35} className="text-purple-400"/>
            <span className="text-sm text-gray-400">Fingerprint Predictions</span>
          </div>
          <h2 className="text-4xl font-bold text-purple-400">
            {data.fingerprint_predictions}
          </h2>
        </div>

        <div className="bg-slate-900 rounded-xl p-8 shadow-lg hover:scale-105 transition">
          <div className="flex items-center justify-between mb-4">
            <FileText size={35} className="text-green-400"/>
            <span className="text-sm text-gray-400">Medical Reports</span>
          </div>
          <h2 className="text-4xl font-bold text-green-400">
            {data.medical_reports}
          </h2>
        </div>

        <div className="bg-slate-900 rounded-xl p-8 shadow-lg hover:scale-105 transition">
          <div className="flex items-center justify-between mb-4">
            <HeartPulse size={35} className="text-red-400"/>
            <span className="text-sm text-gray-400">Blood Compatibility Checks</span>
          </div>
          <h2 className="text-4xl font-bold text-red-400">
            {data.blood_checks}
          </h2>
        </div>

        <div className="bg-slate-900 rounded-xl p-8 shadow-lg hover:scale-105 transition">
          <div className="flex items-center justify-between mb-4">
            <Eye size={35} className="text-cyan-400"/>
            <span className="text-sm text-gray-400">Retinal Scans</span>
          </div>
          <h2 className="text-4xl font-bold text-cyan-400">
            {data.retinal_scans}
          </h2>
        </div>

        <div className="bg-slate-900 rounded-xl p-8 shadow-lg hover:scale-105 transition">
          <div className="flex items-center justify-between mb-4">
            <span className="text-lg text-gray-300">System Status</span>
            <span className="bg-green-500 text-black px-3 py-1 rounded-lg text-sm">
              ONLINE
            </span>
          </div>
          <p className="text-gray-400">
            All AI services running successfully.
          </p>
        </div>

      </div>

      {/* 🔥 CHART SECTION */}

      <div className="p-10 pt-0">

        <div className="bg-slate-900 p-8 rounded-xl shadow">

          <h2 className="text-2xl font-bold mb-6">
            AI Modules Activity Chart
          </h2>

          <div className="w-full h-[300px]">

            <ResponsiveContainer>

              <BarChart data={chartData}>

                <CartesianGrid strokeDasharray="3 3" />

                <XAxis dataKey="name" stroke="#ccc"/>

                <YAxis stroke="#ccc"/>

                <Tooltip />

                <Bar dataKey="value" radius={[10,10,0,0]} />

              </BarChart>

            </ResponsiveContainer>

          </div>

        </div>

      </div>

      {/* FOOTER ANALYTICS SECTION */}

      <div className="p-10 grid grid-cols-1 lg:grid-cols-2 gap-10">

        <div className="bg-slate-900 p-8 rounded-xl shadow">

          <h2 className="text-2xl font-bold mb-6">
            System Overview
          </h2>

          <p className="text-gray-400 leading-relaxed">

            This dashboard provides real-time analytics for the AI Healthcare System.
            It tracks system activity across multiple AI modules including fingerprint
            blood group prediction, medical report OCR, AI medical chat, health risk
            prediction, and blood donation compatibility engine.

          </p>

        </div>

        <div className="bg-slate-900 p-8 rounded-xl shadow">

          <h2 className="text-2xl font-bold mb-6">
            AI Modules Running
          </h2>

          <ul className="space-y-3 text-gray-300">

            <li>🧬 Fingerprint Blood Group Prediction</li>
            <li>📄 Medical Report OCR + AI Analysis</li>
            <li>🤖 Medical AI Chat Assistant</li>
            <li>❤️ Health Risk Prediction</li>
            <li>🩸 Blood Donation Compatibility</li>
            <li>👁 Retinal Disease Detection</li>

          </ul>

        </div>

      </div>

    </div>

  )

}
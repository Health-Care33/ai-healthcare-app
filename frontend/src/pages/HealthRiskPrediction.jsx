import { useState } from "react"
import axios from "axios"
import jsPDF from "jspdf"
import { motion } from "framer-motion"

export default function HealthRiskPrediction(){

  const [form,setForm] = useState({
    name:"",
    email:"",
    age:0,
    gender:"",
    bmi:0,
    blood_pressure:0,
    cholesterol:0,
    glucose:0,
    heart_rate:0,
    smoking:0,
    activity:0
  })

  const [result,setResult] = useState(null)
  const [loading,setLoading] = useState(false)

  const handleChange = (e)=>{
    setForm({
      ...form,
      [e.target.name]: e.target.type === "number"
        ? Number(e.target.value)
        : e.target.value
    })
  }

  const handleGender = (e)=>{
    setForm({
      ...form,
      gender:Number(e.target.value)
    })
  }

  const predictRisk = async()=>{

    setLoading(true)

    try{

      const res = await axios.post(
        "http://127.0.0.1:8000/api/health-risk/predict",
        form
      )

      setResult(res.data.prediction)

    }catch(err){

      console.error(err)
      alert("Prediction Failed")

    }

    setLoading(false)

  }

  const downloadPDF = ()=>{

    const doc = new jsPDF()
    const now = new Date()

    doc.setFontSize(22)
    doc.text("AI Healthcare Risk Report",20,20)

    doc.setFontSize(12)
    doc.text(`User: ${form.name || "N/A"}`,20,30)
    doc.text(`Email: ${form.email || "N/A"}`,20,36)
    doc.text(`Date: ${now.toLocaleDateString()}`,150,30)
    doc.text(`Time: ${now.toLocaleTimeString()}`,150,36)

    doc.setFontSize(14)

    doc.text(`Age: ${form.age}`,20,50)
    doc.text(`Gender: ${form.gender === 1 ? "Male" : "Female"}`,20,60)
    doc.text(`BMI: ${form.bmi}`,20,70)
    doc.text(`Blood Pressure: ${form.blood_pressure}`,20,80)
    doc.text(`Cholesterol: ${form.cholesterol}`,20,90)
    doc.text(`Glucose: ${form.glucose}`,20,100)
    doc.text(`Heart Rate: ${form.heart_rate}`,20,110)
    doc.text(`Smoking: ${form.smoking}`,20,120)
    doc.text(`Activity Level: ${form.activity}`,20,130)

    doc.setFontSize(18)
    doc.text("Prediction Result",20,150)

    doc.setFontSize(14)
    doc.text(`Risk Level: ${result.risk_level}`,20,165)
    doc.text(`Probability: ${result.probability}`,20,175)

    doc.save("health_risk_report.pdf")

  }

  return(

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-950 via-purple-900 to-black p-10">

      <motion.div
        initial={{opacity:0,scale:0.9}}
        animate={{opacity:1,scale:1}}
        transition={{duration:0.6}}
        className="w-full max-w-4xl"
      >

        <div className="bg-white/10 backdrop-blur-xl border border-white/20 p-10 rounded-3xl shadow-2xl">

          <h1 className="text-4xl font-bold text-white mb-8 text-center">
            AI Health Risk Prediction
          </h1>

          <div className="grid grid-cols-2 gap-4">

            <input type="text" name="name" placeholder="Full Name"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="email" name="email" placeholder="Email Address"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="age" placeholder="Age"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <select name="gender" onChange={handleGender}
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg appearance-none">
              <option value="" className="text-black">Select Gender</option>
              <option value="1" className="text-black">Male</option>
              <option value="0" className="text-black">Female</option>
            </select>

            <input type="number" name="bmi" placeholder="BMI"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="blood_pressure" placeholder="Blood Pressure"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="cholesterol" placeholder="Cholesterol"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="glucose" placeholder="Glucose Level"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="heart_rate" placeholder="Heart Rate"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="smoking" placeholder="Smoking (0 No / 1 Yes)"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

            <input type="number" name="activity" placeholder="Activity Level (0-10)"
              className="border border-white/20 bg-white/20 text-white p-3 rounded-lg"
              onChange={handleChange}
            />

          </div>

          <button
            onClick={predictRisk}
            disabled={loading}
            className="w-full mt-6 bg-gradient-to-r from-purple-600 to-blue-600 text-white p-3 rounded-xl font-semibold hover:scale-105 transition"
          >
            {loading ? "AI Analyzing..." : "Predict Health Risk"}
          </button>

          {loading &&(
            <div className="flex justify-center mt-6">
              <motion.div
                animate={{rotate:360}}
                transition={{repeat:Infinity,duration:1}}
                className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full"
              />
            </div>
          )}

          {result &&(

            <motion.div
              initial={{opacity:0,y:20}}
              animate={{opacity:1,y:0}}
              className="mt-8 p-6 bg-white/10 border border-white/20 rounded-xl text-white"
            >

              {/* ✅ PREMIUM FIXED CHART */}
              {(() => {
                const percentage = result.probability <= 1
                  ? result.probability * 100
                  : result.probability

                const radius = 50
                const circumference = 2 * Math.PI * radius
                const offset = circumference - (percentage / 100) * circumference

                return (
                  <div className="flex justify-center mb-8">

                    <svg width="160" height="160"
                      className="drop-shadow-[0_0_25px_rgba(168,85,247,0.6)]">

                      <defs>
                        <linearGradient id="riskGradient" x1="0%" y1="0%" x2="100%" y2="100%">
                          <stop offset="0%" stopColor={
                            percentage < 30 ? "#22c55e" :
                            percentage < 70 ? "#eab308" :
                            "#ef4444"
                          }/>
                          <stop offset="100%" stopColor={
                            percentage < 30 ? "#4ade80" :
                            percentage < 70 ? "#facc15" :
                            "#f87171"
                          }/>
                        </linearGradient>
                      </defs>

                      <circle
                        cx="80"
                        cy="80"
                        r={radius}
                        stroke="rgba(255,255,255,0.1)"
                        strokeWidth="12"
                        fill="none"
                      />

                      <motion.circle
                        cx="80"
                        cy="80"
                        r={radius}
                        stroke="url(#riskGradient)"
                        strokeWidth="12"
                        fill="none"
                        strokeDasharray={circumference}
                        strokeDashoffset={circumference}
                        strokeLinecap="round"
                        initial={{ strokeDashoffset: circumference }}
                        animate={{ strokeDashoffset: offset }}
                        transition={{ duration: 1.5 }}
                      />

                      <text
                        x="50%"
                        y="50%"
                        textAnchor="middle"
                        dy=".3em"
                        className="fill-white text-xl font-bold"
                      >
                        {percentage.toFixed(0)}%
                      </text>

                    </svg>

                  </div>
                )
              })()}

              <h3 className="text-2xl font-bold mb-3">
                Risk Level:
                <span className="text-purple-400 ml-2">
                  {result.risk_level}
                </span>
              </h3>

              <p className="mb-3">
                Probability: {result.probability}
              </p>

              <div className="w-full bg-white/20 rounded-full h-4 mb-6">
                <motion.div
                  initial={{width:0}}
                  animate={{width:`${
                    result.probability <= 1
                      ? result.probability * 100
                      : result.probability
                  }%`}}
                  transition={{duration:1}}
                  className="bg-gradient-to-r from-purple-500 to-blue-500 h-4 rounded-full"
                />
              </div>

              <button
                onClick={downloadPDF}
                className="bg-green-600 text-white px-6 py-2 rounded hover:bg-green-700 transition"
              >
                Download PDF Report
              </button>

            </motion.div>

          )}

        </div>

      </motion.div>

    </div>

  )

}
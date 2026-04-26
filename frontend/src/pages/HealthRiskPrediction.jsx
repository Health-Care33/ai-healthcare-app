import { useState } from "react"
import axios from "axios"
import jsPDF from "jspdf"
import { motion } from "framer-motion"

export default function HealthRiskPrediction() {

  const [form, setForm] = useState({
    name: "",
    email: "",
    age: "",
    bmi: "",
    blood_pressure: "",
    cholesterol: "",
    glucose: "",
    smoking: "",
    physical_activity: "",
    alcohol: "",
    gender: ""
  })

  const [result, setResult] = useState(null)
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState("")

  const handleChange = (e) => {
    setForm({
      ...form,
      [e.target.name]:
        e.target.type === "number"
          ? e.target.value === ""
            ? ""
            : Number(e.target.value)
          : e.target.value
    })
  }

  const handleGender = (e) => {
    setForm({
      ...form,
      gender: e.target.value
    })
  }

  // ✅ VALIDATION FUNCTION
  const isFormValid = () => {
    return Object.values(form).every(
      (val) => val !== "" && val !== null && val !== undefined
    )
  }

  const predictRisk = async () => {

    if (!isFormValid()) {
      setError("⚠ Please fill all fields before prediction")
      return
    }

    setError("")
    setLoading(true)

    try {
      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/health-risk/predict",
        form
      )

      setResult(res.data.data)

    } catch (err) {
      console.error(err)
      setError("Prediction Failed")
    }

    setLoading(false)
  }

  const downloadPDF = () => {

    const doc = new jsPDF()
    const now = new Date()

    doc.setFontSize(22)
    doc.text("AI Healthcare Risk Report", 20, 20)

    doc.setFontSize(12)
    doc.text(`User: ${form.name}`, 20, 30)
    doc.text(`Email: ${form.email}`, 20, 36)
    doc.text(`Date: ${now.toLocaleDateString()}`, 150, 30)
    doc.text(`Time: ${now.toLocaleTimeString()}`, 150, 36)

    doc.text(`Age: ${form.age}`, 20, 50)
    doc.text(`BMI: ${form.bmi}`, 20, 60)
    doc.text(`BP: ${form.blood_pressure}`, 20, 70)
    doc.text(`Cholesterol: ${form.cholesterol}`, 20, 80)
    doc.text(`Glucose: ${form.glucose}`, 20, 90)
    doc.text(`Smoking: ${form.smoking}`, 20, 100)
    doc.text(`Activity: ${form.physical_activity}`, 20, 110)
    doc.text(`Alcohol: ${form.alcohol}`, 20, 120)

    doc.text("Prediction Result", 20, 140)
    doc.text(`Risk: ${result.risk_level}`, 20, 150)
    doc.text(`Confidence: ${result.confidence}`, 20, 160)

    doc.save("health_risk_report.pdf")
  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-950 via-purple-900 to-black p-10">

      <motion.div className="w-full max-w-4xl">

        <div className="bg-white/10 p-10 rounded-3xl text-white">

          <h1 className="text-3xl font-bold text-center mb-6">
            AI Health Risk Prediction
          </h1>

          {/* ❌ ERROR MESSAGE */}
          {error && (
            <p className="text-red-400 text-center mb-4">{error}</p>
          )}

          <div className="grid grid-cols-2 gap-4">

            <input name="name" placeholder="Name" onChange={handleChange} className="p-2 text-black" />
            <input name="email" placeholder="Email" onChange={handleChange} className="p-2 text-black" />

            <input type="number" name="age" placeholder="Age" onChange={handleChange} className="p-2 text-black" />
            <input type="number" name="bmi" placeholder="BMI" onChange={handleChange} className="p-2 text-black" />

            <select onChange={handleGender} className="p-2 text-black">
              <option value="">Select Gender</option>
              <option value="1">Male</option>
              <option value="0">Female</option>
            </select>

            <input type="number" name="blood_pressure" placeholder="BP" onChange={handleChange} className="p-2 text-black" />
            <input type="number" name="cholesterol" placeholder="Cholesterol" onChange={handleChange} className="p-2 text-black" />
            <input type="number" name="glucose" placeholder="Glucose" onChange={handleChange} className="p-2 text-black" />

            <input type="number" name="smoking" placeholder="Smoking (0/1)" onChange={handleChange} className="p-2 text-black" />
            <input type="number" name="physical_activity" placeholder="Activity" onChange={handleChange} className="p-2 text-black" />
            <input type="number" name="alcohol" placeholder="Alcohol (0/1)" onChange={handleChange} className="p-2 text-black" />

          </div>

          {/* ✅ BUTTON BLOCKED IF INVALID */}
          <button
            onClick={predictRisk}
            disabled={loading || !isFormValid()}
            className="w-full mt-6 bg-purple-600 p-3 rounded-xl disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Predict"}
          </button>

          {/* RESULT */}
          {result && (
            <div className="mt-6">
              <h2>Risk: {result.risk_level}</h2>
              <p>Confidence: {result.confidence}</p>

              <button
                onClick={downloadPDF}
                className="mt-4 bg-green-600 px-4 py-2 rounded"
              >
                Download PDF
              </button>
            </div>
          )}

        </div>

      </motion.div>

    </div>
  )
}
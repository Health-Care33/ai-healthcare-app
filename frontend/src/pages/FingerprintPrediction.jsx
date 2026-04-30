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
    const { name, value, type } = e.target

    let finalValue = value

    if (type === "number") {
      finalValue = value === "" ? "" : Number(value)
    }

    if (["gender", "smoking", "alcohol"].includes(name)) {
      finalValue = value === "" ? "" : Number(value)
    }

    setForm({
      ...form,
      [name]: finalValue
    })
  }

  const handleGender = (e) => {
    setForm({
      ...form,
      gender: Number(e.target.value)
    })
  }

  const isFormValid = () => {

    const {
      name, email, age, bmi,
      blood_pressure, cholesterol, glucose,
      smoking, physical_activity, alcohol, gender
    } = form

    if (
      !name || !email || !age || !bmi ||
      !blood_pressure || !cholesterol || !glucose ||
      smoking === "" || physical_activity === "" || alcohol === "" || gender === ""
    ) {
      setError("⚠ All fields are required")
      return false
    }

    setError("")
    return true
  }

  const predictRisk = async () => {

    if (!isFormValid()) return

    setLoading(true)
    setResult(null)
    setError("")

    try {
      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/health-risk/predict",
        form
      )

      console.log("API RESPONSE 👉", res.data)

      // ✅ IMPORTANT FIX
      setResult(res.data)

    } catch (err) {
      console.error(err)

      if (err.response?.status === 422) {
        setError("⚠ Invalid input format")
      } else {
        setError("Prediction Failed")
      }
    }

    setLoading(false)
  }

  return (

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-950 via-purple-900 to-black p-10">

      <motion.div className="w-full max-w-4xl">

        <div className="bg-white/10 p-10 rounded-3xl text-white">

          <h1 className="text-3xl font-bold text-center mb-6">
            AI Health Risk Prediction
          </h1>

          {error && (
            <p className="text-red-400 text-center mb-4">{error}</p>
          )}

          <div className="grid grid-cols-2 gap-4">

            <input name="name" placeholder="Name" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input name="email" placeholder="Email" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input type="number" name="age" placeholder="Age" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input type="number" name="bmi" placeholder="BMI" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <select
              name="gender"
              onChange={handleGender}
              className="p-2 text-white bg-white/10 border border-white/20"
            >
              <option value="" style={{ color: "black" }}>Select Gender</option>
              <option value="1" style={{ color: "black" }}>Male</option>
              <option value="0" style={{ color: "black" }}>Female</option>
            </select>

            <input type="number" name="blood_pressure" placeholder="BP" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input type="number" name="cholesterol" placeholder="Cholesterol" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input type="number" name="glucose" placeholder="Glucose" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <select
              name="smoking"
              onChange={handleChange}
              className="p-2 text-white bg-white/10 border border-white/20"
            >
              <option value="">Smoking?</option>
              <option value="1" style={{ color: "black" }}>Yes</option>
              <option value="0" style={{ color: "black" }}>No</option>
            </select>

            <input type="number" name="physical_activity" placeholder="Activity" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <select
              name="alcohol"
              onChange={handleChange}
              className="p-2 text-white bg-white/10 border border-white/20"
            >
              <option value="">Alcohol?</option>
              <option value="1" style={{ color: "black" }}>Yes</option>
              <option value="0" style={{ color: "black" }}>No</option>
            </select>

          </div>

          <button
            onClick={predictRisk}
            disabled={loading}
            className="w-full mt-6 bg-purple-600 p-3 rounded-xl disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Predict"}
          </button>

          {/* ✅ FINAL RESULT FIX (UI SAME, ONLY CONDITION FIXED) */}
          {result && result.prediction && (

            <motion.div
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="mt-6 bg-white/10 p-6 rounded-xl text-white border border-white/20"
            >

              <h2 className="text-xl font-bold mb-2 text-center">
                Prediction Result
              </h2>

              <p className="text-center text-3xl font-bold text-purple-400">
                {result.prediction}
              </p>

              <p className="text-center mt-2">
                Confidence: {Number(result.confidence || 0).toFixed(2)}%
              </p>

              <div className="mt-4 text-sm text-gray-200 whitespace-pre-line">
                {result.possible_diseases}
              </div>

            </motion.div>

          )}

        </div>
      </motion.div>
    </div>
  )
}

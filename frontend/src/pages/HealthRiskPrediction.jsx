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
      !name || !email || age === "" || bmi === "" ||
      blood_pressure === "" || cholesterol === "" || glucose === "" ||
      smoking === "" || physical_activity === "" || alcohol === "" || gender === ""
    ) {
      setError("⚠ All fields are required")
      return false
    }

    if (!/^[A-Za-z ]+$/.test(name)) {
      setError("⚠ Name should contain only letters")
      return false
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setError("⚠ Invalid email format")
      return false
    }

    if (age < 1 || age > 120) return setError("⚠ Age must be between 1 - 120"), false
    if (bmi < 10 || bmi > 60) return setError("⚠ BMI must be between 10 - 60"), false
    if (blood_pressure < 50 || blood_pressure > 200) return setError("⚠ BP must be between 50 - 200"), false
    if (cholesterol < 100 || cholesterol > 400) return setError("⚠ Cholesterol must be between 100 - 400"), false
    if (glucose < 50 || glucose > 300) return setError("⚠ Glucose must be between 50 - 300"), false

    if (![0,1].includes(physical_activity)) return setError("⚠ Activity must be Yes/No"), false
    if (![0,1].includes(smoking)) return setError("⚠ Smoking must be Yes/No"), false
    if (![0,1].includes(alcohol)) return setError("⚠ Alcohol must be Yes/No"), false

    setError("")
    return true
  }

  const predictRisk = async () => {

    if (!isFormValid()) return

    setLoading(true)

    try {
      const payload = {
        age: form.age,
        bmi: form.bmi,
        blood_pressure: form.blood_pressure,
        cholesterol: form.cholesterol,
        glucose: form.glucose,
        smoking: form.smoking,
        alcohol: form.alcohol,
        physical_activity: form.physical_activity,
        gender: form.gender
      }

      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/health-risk/predict",
        payload
      )

      setResult(res.data)

    } catch (err) {
      console.error(err)
      setError(err?.response?.data?.detail || "Prediction Failed")
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

            <input type="number" name="physical_activity" placeholder="Activity (0 or 1)" onChange={handleChange}
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

          {/* 🔥 RESULT UI (ONLY ADDED PART) */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 50, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.5 }}
              className="mt-8 bg-white/10 backdrop-blur-lg border border-white/20 p-6 rounded-3xl text-center shadow-lg"
            >
              <h2 className="text-2xl font-bold mb-3">
                Prediction:
                <span
                  className={`ml-2 ${
                    result.prediction === "High"
                      ? "text-red-400"
                      : "text-green-400"
                  }`}
                >
                  {result.prediction}
                </span>
              </h2>

              <p className="text-lg mb-2">
                Confidence: <span className="font-semibold">{result.confidence}%</span>
              </p>

              <div className="w-full bg-white/20 rounded-full h-3 mb-4 overflow-hidden">
                <motion.div
                  initial={{ width: 0 }}
                  animate={{ width: `${result.confidence}%` }}
                  transition={{ duration: 0.8 }}
                  className={`h-3 ${
                    result.prediction === "High"
                      ? "bg-red-500"
                      : "bg-green-500"
                  }`}
                />
              </div>

              <p className="text-sm text-gray-300 leading-relaxed">
                {result.possible_diseases}
              </p>
            </motion.div>
          )}

        </div>
      </motion.div>
    </div>
  )
}
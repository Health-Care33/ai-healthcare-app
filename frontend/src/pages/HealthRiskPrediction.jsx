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

  // ✅ VALIDATION (same as yours)
  const isFormValid = () => {

    const {
      name, email, age, bmi,
      blood_pressure, cholesterol, glucose,
      smoking, physical_activity, alcohol, gender
    } = form

    if (
      !name || !email || !age || !bmi ||
      !blood_pressure || !cholesterol || !glucose ||
      smoking === "" || physical_activity === "" || alcohol === "" || !gender
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
    if (physical_activity < 0 || physical_activity > 10) return setError("⚠ Activity must be between 0 - 10"), false
    if (![0, 1].includes(smoking)) return setError("⚠ Smoking must be 0 or 1"), false
    if (![0, 1].includes(alcohol)) return setError("⚠ Alcohol must be 0 or 1"), false

    setError("")
    return true
  }

  const predictRisk = async () => {

    if (!isFormValid()) return

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

            <select onChange={handleGender} className="p-2 text-white bg-white/20">
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

            <input type="number" name="smoking" placeholder="Smoking (0/1)" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input type="number" name="physical_activity" placeholder="Activity" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

            <input type="number" name="alcohol" placeholder="Alcohol (0/1)" onChange={handleChange}
              className="p-2 text-white bg-white/20 placeholder-gray-300" />

          </div>

          <button
            onClick={predictRisk}
            disabled={loading}
            className="w-full mt-6 bg-purple-600 p-3 rounded-xl disabled:opacity-50"
          >
            {loading ? "Analyzing..." : "Predict"}
          </button>

          {/* 🔥 FINAL ANIMATED RESULT */}
          {result && (
            <motion.div
              initial={{ opacity: 0, y: 40, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              transition={{ duration: 0.6 }}
              className="mt-6 p-6 bg-white/10 rounded-2xl border border-white/20"
            >
              <h2 className="text-2xl font-bold text-center mb-2">
                Prediction Result
              </h2>

              <p className={`text-center text-xl font-semibold ${
                result.risk_level === "High" ? "text-red-400" : "text-green-400"
              }`}>
                Risk: {result.risk_level}
              </p>

              <p className="text-center mb-4">
                Confidence: {result.confidence ? `${result.confidence}%` : "N/A"}
              </p>

              {result.possible_diseases && (
                <div>
                  <h3 className="font-semibold mb-2">
                    Possible Future Diseases:
                  </h3>

                  <ul className="list-disc pl-5 text-gray-200">
                    {result.possible_diseases
                      .split("\n")
                      .filter(i => i.trim())
                      .map((item, i) => (
                        <li key={i}>{item.replace("-", "").trim()}</li>
                      ))}
                  </ul>
                </div>
              )}

              <button
                onClick={downloadPDF}
                className="mt-6 w-full bg-green-600 px-4 py-2 rounded-xl"
              >
                Download PDF
              </button>
            </motion.div>
          )}

        </div>
      </motion.div>
    </div>
  )
}
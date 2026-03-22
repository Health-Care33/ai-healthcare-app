import { useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"
import { Upload, Brain, Stethoscope } from "lucide-react"
import jsPDF from "jspdf"

export default function MedicalReportAI(){

  const [file,setFile] = useState(null)
  const [reportText,setReportText] = useState("")
  const [question,setQuestion] = useState("")
  const [answer,setAnswer] = useState("")
  const [diagnosis,setDiagnosis] = useState("")
  const [loading,setLoading] = useState(false)

  // Upload PDF
  const uploadReport = async () => {

    if(!file){
      alert("Please select a file")
      return
    }

    const formData = new FormData()
    formData.append("file",file)

    try{
      const res = await axios.post(
        "http://127.0.0.1:8000/api/medical-report/upload",
        formData
      )
      setReportText(res.data.data.extracted_text)
    }catch(err){
      console.log(err)
      alert("Upload failed")
    }
  }

  // Ask AI
  const askAI = async () => {

    if(!reportText){
      alert("Upload report first")
      return
    }

    setLoading(true)

    try{
      const res = await axios.post(
        "http://127.0.0.1:8000/api/medical-chat/ask",
        {
          report_text:reportText,
          question:question
        }
      )
      setAnswer(res.data.answer)
    }catch(err){
      console.log(err)
    }

    setLoading(false)
  }

  // Diagnosis
  const runDiagnosis = async () => {

    if(!reportText){
      alert("Upload report first")
      return
    }

    setLoading(true)

    try{
      const res = await axios.post(
        "http://127.0.0.1:8000/api/medical-chat/diagnose",
        {
          report_text:reportText
        }
      )
      setDiagnosis(res.data.diagnosis)
    }catch(err){
      console.log(err)
    }

    setLoading(false)
  }

  // ✅ NEW: Download PDF
  const downloadPDF = () => {

    const doc = new jsPDF()

    doc.setFont("Helvetica", "bold")
    doc.setFontSize(18)
    doc.text("Medical AI Report", 20, 20)

    doc.setFontSize(12)
    doc.setFont("Helvetica", "normal")

    let y = 40

    if(answer){
      doc.setFont("Helvetica", "bold")
      doc.text("AI Response:", 20, y)
      y += 10

      doc.setFont("Helvetica", "normal")
      const splitAnswer = doc.splitTextToSize(answer, 170)
      doc.text(splitAnswer, 20, y)
      y += splitAnswer.length * 7 + 10
    }

    if(diagnosis){
      doc.setFont("Helvetica", "bold")
      doc.text("AI Diagnosis:", 20, y)
      y += 10

      doc.setFont("Helvetica", "normal")
      const splitDiagnosis = doc.splitTextToSize(diagnosis, 170)
      doc.text(splitDiagnosis, 20, y)
    }

    doc.save("Medical_Report_AI.pdf")
  }

  return(

    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-blue-900 to-slate-800 flex items-center justify-center p-6">

      <motion.div 
        initial={{opacity:0, y:40}}
        animate={{opacity:1, y:0}}
        transition={{duration:0.6}}
        className="w-full max-w-4xl backdrop-blur-xl bg-white/10 border border-white/20 rounded-3xl shadow-2xl p-8"
      >

        <h1 className="text-4xl font-bold text-white mb-6 text-center tracking-wide">
          🧠 Medical Report AI
        </h1>

        <div className="mb-6">

          <label className="block text-white/80 mb-2">
            Upload Medical Report (PDF/Image)
          </label>

          <input
            type="file"
            onChange={(e)=>setFile(e.target.files[0])}
            className="w-full bg-white/20 text-white p-3 rounded-xl border border-white/30"
          />

          <motion.button
            whileHover={{scale:1.05}}
            whileTap={{scale:0.95}}
            onClick={uploadReport}
            className="mt-4 flex items-center gap-2 bg-blue-600 hover:bg-blue-700 text-white px-6 py-3 rounded-xl shadow-lg"
          >
            <Upload size={18}/> Upload Report
          </motion.button>

        </div>

        <textarea
          value={reportText}
          onChange={(e)=>setReportText(e.target.value)}
          rows="6"
          className="w-full bg-white/20 text-white placeholder-white/60 border border-white/30 p-4 rounded-xl mb-6 focus:outline-none focus:ring-2 focus:ring-blue-400"
          placeholder="Extracted report text will appear here..."
        />

        <input
          type="text"
          placeholder="Ask anything about the report..."
          value={question}
          onChange={(e)=>setQuestion(e.target.value)}
          className="w-full bg-white/20 text-white placeholder-white/60 border border-white/30 p-4 rounded-xl mb-6 focus:outline-none focus:ring-2 focus:ring-purple-400"
        />

        <div className="flex gap-4 flex-wrap">

          <motion.button
            whileHover={{scale:1.05}}
            whileTap={{scale:0.95}}
            onClick={askAI}
            className="flex items-center gap-2 bg-purple-600 hover:bg-purple-700 text-white px-6 py-3 rounded-xl shadow-lg"
          >
            <Brain size={18}/> Ask AI
          </motion.button>

          <motion.button
            whileHover={{scale:1.05}}
            whileTap={{scale:0.95}}
            onClick={runDiagnosis}
            className="flex items-center gap-2 bg-green-600 hover:bg-green-700 text-white px-6 py-3 rounded-xl shadow-lg"
          >
            <Stethoscope size={18}/> AI Diagnosis
          </motion.button>

        </div>

        {loading && (
          <div className="mt-6 flex items-center gap-3 text-white">
            <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            AI analyzing report...
          </div>
        )}

        {answer && (
          <motion.div 
            initial={{opacity:0}}
            animate={{opacity:1}}
            className="mt-6 bg-white/20 p-5 rounded-xl border border-white/30 text-white"
          >
            <h2 className="font-bold mb-2 text-lg">
              🤖 AI Response
            </h2>
            <p className="leading-relaxed">{answer}</p>
          </motion.div>
        )}

        {diagnosis && (
          <motion.div 
            initial={{opacity:0}}
            animate={{opacity:1}}
            className="mt-6 bg-green-500/20 p-5 rounded-xl border border-green-400/30 text-white"
          >
            <h2 className="font-bold mb-2 text-lg">
              🩺 AI Diagnosis
            </h2>
            <p className="leading-relaxed">{diagnosis}</p>
          </motion.div>
        )}

        {/* ✅ NEW BUTTON */}
        {(answer || diagnosis) && (
          <button
            onClick={downloadPDF}
            className="mt-6 bg-yellow-500 hover:bg-yellow-600 text-white px-6 py-3 rounded-xl shadow-lg"
          >
            📄 Download PDF Report
          </button>
        )}

      </motion.div>

    </div>

  )
}
import { useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"
import { Upload, Brain, Stethoscope } from "lucide-react"
import jsPDF from "jspdf"
import html2pdf from "html2pdf.js"   // ✅ ADDED

export default function MedicalReportAI(){

  const [file,setFile] = useState(null)
  const [reportText,setReportText] = useState("")
  const [question,setQuestion] = useState("")
  const [answer,setAnswer] = useState("")
  const [diagnosis,setDiagnosis] = useState("")
  const [loading,setLoading] = useState(false)

  const uploadReport = async () => {

    if(!file){
      alert("Please select a file")
      return
    }

    const formData = new FormData()
    formData.append("file",file)

    try{
      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/medical-report/upload",
        formData
      )

      setReportText(res?.data?.data?.extracted_text || "")

    }catch(err){
      console.log(err)
      alert("Upload failed")
    }
  }

  const askAI = async () => {

    if(!reportText){
      alert("Upload report first")
      return
    }

    if(!question.trim()){
      alert("Please enter a question")
      return
    }

    setLoading(true)

    try{
      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/medical-chat/ask",
        {
          report_text:reportText,
          question:question
        }
      )

      const data = res.data

      if(typeof data === "string"){
        setAnswer(data)
      }else{
        setAnswer(data?.answer || "No response from AI")
      }

    }catch(err){
      console.log(err)
      alert("Something went wrong")
    }finally{
      setLoading(false)
    }
  }

  const runDiagnosis = async () => {

    if(!reportText){
      alert("Upload report first")
      return
    }

    setLoading(true)

    try{
      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/medical-chat/diagnose",
        {
          report_text:reportText
        }
      )

      const data = res.data

      if(typeof data === "string"){
        setDiagnosis(data)
      }else{
        setDiagnosis(data?.diagnosis || "No diagnosis available")
      }

    }catch(err){
      console.log(err)
      alert("Something went wrong")
    }finally{
      setLoading(false)
    }
  }

  // ✅ REPLACED FUNCTION (MAIN FIX)
  const downloadPDF = () => {

    const element = document.getElementById("pdf-content")

    const opt = {
      margin: 0.5,
      filename: "Medical_Report_AI.pdf",
      image: { type: "jpeg", quality: 1 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: "in", format: "a4", orientation: "portrait" }
    }

    html2pdf().set(opt).from(element).save()
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

        {/* ✅ SAME UI, JUST WRAPPED */}
        <div id="pdf-content">

          {answer && (
            <motion.div 
              initial={{opacity:0}}
              animate={{opacity:1}}
              className="mt-6 bg-white/20 p-5 rounded-xl border border-white/30 text-white"
            >
              <h2 className="font-bold mb-2 text-lg">
                🤖 AI Response
              </h2>
              <p 
                className="leading-relaxed" 
                dangerouslySetInnerHTML={{ __html: answer }} 
              />
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

        </div>

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
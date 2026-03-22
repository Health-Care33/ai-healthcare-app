import { useState, useEffect, useRef } from "react"
import axios from "axios"
import {
  PieChart,
  Pie,
  Cell,
  Tooltip,
  ResponsiveContainer
} from "recharts"

export default function RetinaScan(){

const [image,setImage] = useState(null)
const [preview,setPreview] = useState(null)
const [loading,setLoading] = useState(false)
const [result,setResult] = useState(null)

const [aiReport,setAiReport] = useState("")
const [showAI,setShowAI] = useState(false)
const [typedAI,setTypedAI] = useState("")

const [progress,setProgress] = useState(0)
const [animatedConfidence,setAnimatedConfidence] = useState(0)
const [flash,setFlash] = useState(false)

const audioRef = useRef(null)
const fileInputRef = useRef(null)

// 🔊 AUDIO LOAD
useEffect(()=>{
 audioRef.current = new Audio("/scan.wav")
 audioRef.current.volume = 0.5
},[])

// IMAGE
const handleImage = (e)=>{
const file = e.target.files[0]
if(!file) return

setImage(file)
setPreview(URL.createObjectURL(file))
setResult(null)
setAiReport("")
setShowAI(false)
setTypedAI("")
}

// 🔥 SCAN WITH SOUND
const scanRetina = async ()=>{

if(!image){
alert("Upload Retina Image First")
return
}

try{

if(audioRef.current){
  audioRef.current.currentTime = 0
  audioRef.current.play().catch(()=>{})
}

setLoading(true)
setProgress(0)

let interval = setInterval(()=>{
  setProgress(prev => (prev < 95 ? prev + 2 : prev))
},100)

const formData = new FormData()
formData.append("file",image)

const token = localStorage.getItem("token")

const resPromise = axios.post(
"http://127.0.0.1:8000/api/retinal-detection",
formData,
{
headers:{ Authorization:`Bearer ${token}` }
}
)

const [res] = await Promise.all([
  resPromise,
  new Promise(resolve => setTimeout(resolve, 5000))
])

clearInterval(interval)
setProgress(100)

setTimeout(()=>{
  setResult(res.data.prediction)
  setAiReport(res.data.ai_report || "")
  setFlash(true)
  setTimeout(()=>setFlash(false),500)
},500)

}catch(err){
console.log(err)
alert("Scan Failed")
}

setLoading(false)
}

// 🔥 CONFIDENCE ANIMATION
useEffect(()=>{
if(result){
let count = 0
let interval = setInterval(()=>{
  count += 1
  if(count >= result.confidence){
    count = result.confidence
    clearInterval(interval)
  }
  setAnimatedConfidence(count)
},20)
}
},[result])

// 🔥 AI TYPE EFFECT
useEffect(()=>{
if(showAI && aiReport){
  setTypedAI("")
  let i = 0

  const interval = setInterval(()=>{
    if(i < aiReport.length){
      setTypedAI(prev => prev + aiReport.charAt(i))
      i++
    } else {
      clearInterval(interval)
    }
  },15)

  return ()=>clearInterval(interval)
}
},[showAI, aiReport])

// RESET
const resetScan = ()=>{
setImage(null)
setPreview(null)
setResult(null)
setAiReport("")
setShowAI(false)
setTypedAI("")
setProgress(0)
setAnimatedConfidence(0)

if(fileInputRef.current){
  fileInputRef.current.value = ""
  fileInputRef.current.click()
}
}

// 📄 DOWNLOAD PDF
const downloadPDF = ()=>{
const content = `
AI RETINA REPORT

Disease: ${result.disease}
Confidence: ${result.confidence}%

-------------------------

AI ANALYSIS:

${aiReport}

Generated on: ${new Date().toLocaleString()}
`
const blob = new Blob([content], { type: "text/plain" })
const link = document.createElement("a")
link.href = URL.createObjectURL(blob)
link.download = "retina-report.txt"
link.click()
}

// COLOR
const getColor = ()=>{
if(!result) return "green"
if(result.confidence > 75) return "red"
if(result.confidence > 40) return "yellow"
return "green"
}

// 🔥 CHART DATA
const chartData = result ? [
  { name: "Risk", value: animatedConfidence },
  { name: "Safe", value: 100 - animatedConfidence }
] : []

return(

<div className="min-h-screen bg-gradient-to-br from-blue-900 via-indigo-900 to-purple-900 text-white">

<div className="max-w-6xl mx-auto p-10">

<h1 className="text-4xl font-bold mb-10 text-center">
🧠 AI Retinal Disease Detection
</h1>

<div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl shadow-2xl p-10">

<div className="grid grid-cols-1 md:grid-cols-2 gap-12">

{/* Upload */}
<div>

<h2 className="text-2xl font-semibold mb-6">
Upload Retina Scan
</h2>

<label className="relative flex flex-col items-center justify-center border-2 border-dashed border-white/30 rounded-xl cursor-pointer hover:border-cyan-400 transition overflow-hidden min-h-[260px]">

<input
ref={fileInputRef}
type="file"
accept="image/*"
onChange={handleImage}
className="hidden"
/>

{!preview && (
<p className="text-white/70 text-lg">
Click or Drag Retina Image Here
</p>
)}

{preview && (
<img
src={preview}
alt="retina"
className="w-full h-full object-contain p-4 rounded-xl"
/>
)}

</label>

{loading && (
<p className="mt-4 text-center text-cyan-300">
Analyzing Retina... {progress}%
</p>
)}

</div>

{/* AI */}
<div>

<h2 className="text-2xl font-semibold mb-6">
AI Analysis
</h2>

{!loading && !result && (
<button
onClick={scanRetina}
className="bg-gradient-to-r from-cyan-500 to-purple-600 px-8 py-3 rounded-xl font-semibold hover:scale-105 transition shadow-lg">
Start AI Scan
</button>
)}

{result && (
<div className="bg-white/10 p-8 rounded-xl border border-white/20 shadow-lg">

<h3 className="text-2xl font-bold mb-6 text-cyan-300">
Prediction Result
</h3>

<div className="mb-4 text-lg">
Disease:
<span className="ml-3 text-red-400 font-bold text-xl">
{result.disease}
</span>
</div>

<div className="mb-4 text-lg">
Confidence:
<span className="ml-3 text-green-400 text-xl">
{animatedConfidence}%
</span>
</div>

<div className="w-full bg-white/20 rounded-full h-4 mb-4">
<div
className={`h-4 rounded-full transition-all duration-700 ${
getColor()==="red" ? "bg-red-400" :
getColor()==="yellow" ? "bg-yellow-400" :
"bg-green-400"
}`}
style={{width:`${animatedConfidence}%`}}
></div>
</div>

{/* 🔥 ANIMATED CHART */}
<div className="mt-6 h-64">
  <ResponsiveContainer width="100%" height="100%">
    <PieChart>
      <Pie
        data={chartData}
        cx="50%"
        cy="50%"
        innerRadius={60}
        outerRadius={90}
        dataKey="value"
        isAnimationActive={true}
        animationDuration={800}
      >
        <Cell fill={getColor()==="red" ? "#f87171" : getColor()==="yellow" ? "#facc15" : "#4ade80"} />
        <Cell fill="#1f2937" />
      </Pie>
      <Tooltip />
    </PieChart>
  </ResponsiveContainer>
</div>

{/* 🔥 CLEAN BUTTONS */}
<div className="mt-6 flex flex-wrap gap-4">

<button
onClick={()=>setShowAI(true)}
className="flex-1 min-w-[180px] bg-purple-600 px-6 py-3 rounded-lg hover:scale-105 transition shadow-lg">
Generate AI Report
</button>

<button
onClick={resetScan}
className="flex-1 min-w-[180px] bg-red-500 px-6 py-3 rounded-lg hover:bg-red-600 transition shadow-lg">
Scan Another Image
</button>

<button
onClick={downloadPDF}
className="flex-1 min-w-[180px] bg-cyan-500 px-6 py-3 rounded-lg hover:bg-cyan-600 transition shadow-lg">
Download Report
</button>

</div>

{/* AI REPORT */}
{showAI && (
<div className="mt-6 p-4 bg-purple-900/40 rounded-xl border border-purple-400 animate-pulse">
<p className="whitespace-pre-line text-sm">
{typedAI}
</p>
</div>
)}

</div>
)}

</div>

</div>

</div>

</div>

</div>

)
}
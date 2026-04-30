import { useState } from "react"
import axios from "axios"
import { motion } from "framer-motion"

export default function FingerprintPrediction(){

  const [file,setFile] = useState(null)
  const [preview,setPreview] = useState(null)
  const [result,setResult] = useState(null)
  const [loading,setLoading] = useState(false)
  const [dragging,setDragging] = useState(false)

  const handleFile = (selectedFile)=>{
    if(!selectedFile) return

    setFile(selectedFile)
    setPreview(URL.createObjectURL(selectedFile))
    setResult(null)
  }

  const handleDrop = (e)=>{
    e.preventDefault()
    setDragging(false)

    const droppedFile = e.dataTransfer.files?.[0]
    if(droppedFile) handleFile(droppedFile)
  }

  const handlePredict = async (e)=>{
    e.preventDefault()

    if(!file){
      alert("Please upload fingerprint image")
      return
    }

    const formData = new FormData()
    formData.append("file",file)

    setLoading(true)
    setResult(null)

    try{
      const res = await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/fingerprint/predict-blood-group",
        formData
      )

      setResult(res?.data || {})

    }catch(err){
      console.log(err)
      setResult({
        success:false,
        error:"Prediction failed"
      })
    }

    setLoading(false)
  }

  return(

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-950 via-purple-900 to-black p-10">

      <motion.div
        initial={{opacity:0,scale:0.9}}
        animate={{opacity:1,scale:1}}
        transition={{duration:0.6}}
        className="w-full max-w-xl"
      >

        <form
          onSubmit={handlePredict}
          className="bg-white/10 backdrop-blur-xl border border-white/20 rounded-3xl shadow-2xl p-10"
        >

          <h1 className="text-4xl font-bold text-center text-white mb-8">
            Fingerprint Blood Group AI
          </h1>

          {/* Drag & Drop */}

          <div
            onDragOver={(e)=>{e.preventDefault();setDragging(true)}}
            onDragLeave={()=>setDragging(false)}
            onDrop={handleDrop}
            className={`border-2 border-dashed rounded-xl p-8 text-center transition 
            ${dragging ? "border-purple-400 bg-purple-500/10" : "border-white/30"}`}
          >

            <input
              type="file"
              accept="image/*"
              onChange={(e)=>handleFile(e.target.files?.[0])}
              className="hidden"
              id="fileUpload"
            />

            <label
              htmlFor="fileUpload"
              className="cursor-pointer text-white"
            >

              <p className="text-lg font-semibold mb-2">
                Drag & Drop Fingerprint Image
              </p>

              <p className="text-sm text-gray-300">
                or click to upload
              </p>

            </label>

          </div>

          {/* Preview */}

          {preview && (

            <motion.div
              initial={{opacity:0}}
              animate={{opacity:1}}
              className="mt-6 flex justify-center"
            >

              <img
                src={preview}
                alt="preview"
                className="w-40 h-40 object-cover rounded-xl border border-white/30"
              />

            </motion.div>

          )}

          {/* Predict Button */}

          <button
            disabled={loading}
            className="w-full mt-6 bg-gradient-to-r from-purple-600 to-blue-600 text-white p-3 rounded-xl font-semibold hover:scale-105 transition"
          >

            {loading ? "AI Analyzing..." : "Predict Blood Group"}

          </button>

          {/* Loader */}

          {loading && (

            <div className="flex justify-center mt-6">

              <motion.div
                animate={{rotate:360}}
                transition={{repeat:Infinity,duration:1}}
                className="w-10 h-10 border-4 border-purple-500 border-t-transparent rounded-full"
              />

            </div>

          )}

          {/* SUCCESS RESULT */}

          {result && result.success && (

            <motion.div
              initial={{opacity:0,y:20}}
              animate={{opacity:1,y:0}}
              className="mt-8 bg-white/10 p-6 rounded-xl text-center text-white border border-white/20"
            >

              <h2 className="text-2xl font-bold mb-2">
                Blood Group Detected
              </h2>

              <p className="text-4xl font-bold text-purple-400 mb-3">
                {result.blood_group}
              </p>

              <p className="mb-3">
                Confidence: {(Number(result?.confidence ?? 0)).toFixed(2)}%
              </p>

              <div className="w-full bg-white/20 rounded-full h-4">

                <motion.div
                  initial={{width:0}}
                  animate={{ width: `${Math.min(Number(result?.confidence ?? 0), 100)}%` }}
                  transition={{duration:1}}
                  className="bg-gradient-to-r from-purple-500 to-blue-500 h-4 rounded-full"
                />

              </div>

            </motion.div>

          )}

          {/* ERROR RESULT */}

          {result && result.success === false && (
            <div className="mt-6 text-red-400 text-center">
              ❌ {result.error || "Prediction failed"}
            </div>
          )}

        </form>

      </motion.div>

    </div>

  )

}
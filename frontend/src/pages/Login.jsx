import { useState, useContext } from "react"
import axios from "axios"
import { useNavigate, useSearchParams } from "react-router-dom"
import { AuthContext } from "../context/AuthContext"
import { motion } from "framer-motion"
import { Mail, Lock } from "lucide-react"

export default function Login(){

  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const { setUser } = useContext(AuthContext)

  const redirect = searchParams.get("redirect") || "/dashboard"
  const showMessage = searchParams.get("redirect")

  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")
  const [loading,setLoading] = useState(false)
  const [error,setError] = useState("")

  const handleLogin = async (e)=>{
    e.preventDefault()
    setLoading(true)
    setError("")

    try{
      const res = await axios.post(
        "http://127.0.0.1:8000/api/auth/login",
        { email, password }
      )

      const token = res.data.access_token
      localStorage.setItem("token", token)

      const profile = await axios.get(
        "http://127.0.0.1:8000/api/auth/profile",
        {
          headers:{ Authorization:`Bearer ${token}` }
        }
      )

      setUser(profile.data)
      navigate(redirect)

    }catch{
      setError("Invalid email or password")
    }

    setLoading(false)
  }

  const handleGoogleLogin = ()=>{
    window.location.href =
      "http://127.0.0.1:8000/api/auth/google/login"
  }

  return(

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-indigo-200 via-blue-100 to-purple-200 relative overflow-hidden">

      {/* Animated background blobs */}
      <div className="absolute w-72 h-72 bg-purple-400 rounded-full blur-3xl opacity-30 top-10 left-10 animate-pulse"></div>
      <div className="absolute w-72 h-72 bg-blue-400 rounded-full blur-3xl opacity-30 bottom-10 right-10 animate-pulse"></div>

      <div className="z-10">

        {showMessage && (
          <motion.div
            initial={{opacity:0,y:-40}}
            animate={{opacity:1,y:0}}
            className="mb-6 bg-yellow-400 text-black p-3 rounded-lg text-center shadow-lg font-medium"
          >
            Please login or register first to access this feature
          </motion.div>
        )}

        <motion.form
          onSubmit={handleLogin}
          initial={{opacity:0, scale:0.9}}
          animate={{opacity:1, scale:1}}
          transition={{duration:0.4}}
          className="backdrop-blur-xl bg-white/30 border border-white/40 p-10 rounded-3xl shadow-2xl w-96"
        >

          <h2 className="text-3xl font-bold mb-6 text-center text-gray-800">
            Welcome Back 👋
          </h2>

          {error && (
            <div className="bg-red-500 text-white p-2 rounded mb-4 text-center">
              {error}
            </div>
          )}

          {/* Email */}
          <div className="relative mb-5">
            <Mail className="absolute left-3 top-3 text-gray-500" size={18}/>
            <input
              type="email"
              required
              value={email}
              onChange={(e)=>setEmail(e.target.value)}
              className="w-full pl-10 p-3 bg-white/70 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none peer"
            />
            <label className="absolute left-10 top-3 text-gray-500 text-sm transition-all 
              peer-focus:-top-2 peer-focus:text-xs peer-focus:text-indigo-600 
              peer-valid:-top-2 peer-valid:text-xs bg-white px-1">
              Email
            </label>
          </div>

          {/* Password */}
          <div className="relative mb-6">
            <Lock className="absolute left-3 top-3 text-gray-500" size={18}/>
            <input
              type="password"
              required
              value={password}
              onChange={(e)=>setPassword(e.target.value)}
              className="w-full pl-10 p-3 bg-white/70 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 outline-none peer"
            />
            <label className="absolute left-10 top-3 text-gray-500 text-sm transition-all 
              peer-focus:-top-2 peer-focus:text-xs peer-focus:text-indigo-600 
              peer-valid:-top-2 peer-valid:text-xs bg-white px-1">
              Password
            </label>
          </div>

          {/* Button */}
          <button
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-500 to-purple-500 text-white p-3 rounded-lg hover:scale-105 transition flex items-center justify-center shadow-lg"
          >
            {loading ? (
              <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin"></div>
            ) : (
              "Login"
            )}
          </button>

          {/* Divider */}
          <div className="flex items-center my-5">
            <hr className="flex-grow border-gray-300"/>
            <span className="mx-2 text-gray-500 text-sm">OR</span>
            <hr className="flex-grow border-gray-300"/>
          </div>

          {/* Google */}
          <button
            type="button"
            onClick={handleGoogleLogin}
            className="w-full bg-white/80 border border-gray-300 p-3 rounded-lg hover:bg-white transition flex items-center justify-center gap-2 shadow"
          >
            <img
              src="https://www.svgrepo.com/show/475656/google-color.svg"
              alt="google"
              className="w-5 h-5"
            />
            Continue with Google
          </button>

        </motion.form>

      </div>

    </div>
  )
}
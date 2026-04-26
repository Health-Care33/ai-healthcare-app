import { useState } from "react"
import axios from "axios"
import { useNavigate, Link } from "react-router-dom"
import { motion } from "framer-motion"

export default function Register(){

  const navigate = useNavigate()

  const [name,setName] = useState("")
  const [email,setEmail] = useState("")
  const [password,setPassword] = useState("")
  const [loading,setLoading] = useState(false)
  const [error,setError] = useState("")

  const handleRegister = async (e)=>{
    e.preventDefault()
    setLoading(true)
    setError("")

    try{
      await axios.post(
        "https://ai-healthcare-backend-psnj.onrender.com/api/auth/register",
        { name, email, password }
      )
      navigate("/login")
    }catch(err){
      setError("Registration failed. Try another email.")
    }

    setLoading(false)
  }

  const handleGoogleLogin = () => {
    window.location.href =
      "https://ai-healthcare-backend-psnj.onrender.com/api/auth/google/login"
  }

  return(

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 relative overflow-hidden">

      {/* 🔥 BACKGROUND GLOW EFFECT */}
      <div className="absolute w-[500px] h-[500px] bg-purple-600 opacity-20 blur-3xl rounded-full top-[-100px] left-[-100px]"></div>
      <div className="absolute w-[400px] h-[400px] bg-blue-500 opacity-20 blur-3xl rounded-full bottom-[-100px] right-[-100px]"></div>

      {/* 🔥 FORM CARD */}
      <motion.form
        initial={{opacity:0, scale:0.9}}
        animate={{opacity:1, scale:1}}
        transition={{duration:0.4}}
        onSubmit={handleRegister}
        className="relative z-10 bg-white/10 backdrop-blur-2xl border border-white/20 p-10 rounded-3xl shadow-2xl w-[380px]"
      >

        {/* TITLE */}
        <h2 className="text-3xl font-bold mb-2 text-center text-white">
          Create Account
        </h2>

        <p className="text-center text-gray-300 mb-6 text-sm">
          Join AI Healthcare Platform 🚀
        </p>

        {/* ERROR */}
        {error && (
          <div className="bg-red-500/80 text-white p-2 rounded-lg mb-4 text-center text-sm">
            {error}
          </div>
        )}

        {/* INPUTS */}
        <input
          type="text"
          placeholder="Full Name"
          required
          className="w-full p-3 mb-4 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-purple-400 outline-none transition"
          onChange={(e)=>setName(e.target.value)}
        />

        <input
          type="email"
          placeholder="Email Address"
          required
          className="w-full p-3 mb-4 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-purple-400 outline-none transition"
          onChange={(e)=>setEmail(e.target.value)}
        />

        <input
          type="password"
          placeholder="Password"
          required
          className="w-full p-3 mb-6 rounded-xl bg-white/20 text-white placeholder-gray-300 focus:ring-2 focus:ring-purple-400 outline-none transition"
          onChange={(e)=>setPassword(e.target.value)}
        />

        {/* REGISTER BUTTON */}
        <motion.button
          whileTap={{scale:0.95}}
          disabled={loading}
          className="w-full bg-gradient-to-r from-purple-600 to-indigo-600 text-white p-3 rounded-xl font-semibold hover:opacity-90 transition shadow-lg"
        >
          {loading ? "Creating Account..." : "Register"}
        </motion.button>

        {/* DIVIDER */}
        <div className="flex items-center my-6">
          <hr className="flex-grow border-white/30"/>
          <span className="mx-2 text-gray-300 text-sm">OR</span>
          <hr className="flex-grow border-white/30"/>
        </div>

        {/* GOOGLE BUTTON */}
        <motion.button
          whileHover={{scale:1.02}}
          type="button"
          onClick={handleGoogleLogin}
          className="w-full bg-white text-black p-3 rounded-xl font-medium hover:bg-gray-200 transition shadow"
        >
          Continue with Google
        </motion.button>

        {/* LOGIN LINK */}
        <p className="text-center mt-6 text-gray-300 text-sm">
          Already have an account?
          <Link
            to="/login"
            className="ml-1 text-purple-400 hover:underline"
          >
            Login
          </Link>
        </p>

      </motion.form>

    </div>

  )
}
import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export default function LoginSuccess(){

  const navigate = useNavigate()

  useEffect(()=>{

    setTimeout(()=>{

      navigate("/dashboard")

    },2000)

  },[])

  return(

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-blue-600 to-purple-700">

      <div className="bg-white p-10 rounded-2xl shadow-xl text-center">

        <div className="text-5xl mb-4">
          ✅
        </div>

        <h2 className="text-2xl font-bold mb-2">
          Login Successful
        </h2>

        <p className="text-gray-600">
          Redirecting to dashboard...
        </p>

      </div>

    </div>

  )

}
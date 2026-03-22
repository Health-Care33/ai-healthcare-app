import { useEffect } from "react"
import { useNavigate } from "react-router-dom"

export default function GoogleSuccess(){

  const navigate = useNavigate()

  useEffect(()=>{

    const params = new URLSearchParams(window.location.search)

    const token = params.get("token")

    if(token){

      localStorage.setItem("token",token)

      setTimeout(()=>{

        navigate("/dashboard")

      },2000)

    }

  },[])

  return(

    <div className="min-h-screen flex items-center justify-center bg-gradient-to-r from-red-500 to-yellow-500">

      <div className="bg-white p-10 rounded-2xl shadow-xl text-center">

        <div className="w-10 h-10 border-4 border-blue-500 border-t-transparent rounded-full animate-spin mx-auto mb-4"></div>

        <h2 className="text-xl font-semibold">
          Signing in with Google...
        </h2>

      </div>

    </div>

  )

}
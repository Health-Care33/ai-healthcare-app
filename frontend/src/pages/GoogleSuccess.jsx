import { useEffect, useContext } from "react"
import { useNavigate } from "react-router-dom"
import { AuthContext } from "../context/AuthContext"

export default function GoogleSuccess(){

  const navigate = useNavigate()
  const { loadUser } = useContext(AuthContext)

  useEffect(()=>{

    const params = new URLSearchParams(window.location.search)
    const token = params.get("token")

    const handleAuth = async () => {

      if(token){
        localStorage.setItem("token", token)

        await loadUser()   // ✅ IMPORTANT FIX

        navigate("/dashboard")
      }

    }

    handleAuth()

  },[])

  return(
    <div>Signing in...</div>
  )
}
import { createContext, useEffect, useState } from "react"
import { getProfile } from "../services/authService"

export const AuthContext = createContext()

export const AuthProvider = ({ children }) => {

  const [user, setUser] = useState(null)
  const [loading, setLoading] = useState(true)

  const loadUser = async () => {

    const token = localStorage.getItem("token")

    if (!token) {
      setLoading(false)
      return
    }

    try {

      const data = await getProfile()
      setUser(data)

    } catch {

      localStorage.removeItem("token")

    }

    setLoading(false)
  }

  useEffect(() => {
    loadUser()
  }, [])

  return (
    <AuthContext.Provider value={{ user, setUser, loadUser, loading }}>
      {children}
    </AuthContext.Provider>
  )

}
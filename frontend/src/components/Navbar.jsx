import { Link, useNavigate } from "react-router-dom"
import { useContext } from "react"
import { AuthContext } from "../context/AuthContext"

export default function Navbar(){

  const navigate = useNavigate()

  const { user, setUser } = useContext(AuthContext)

  const logout = () => {

    localStorage.removeItem("token")

    setUser(null)

    navigate("/login")

  }

  return (

    <nav className="bg-slate-900 text-white px-8 py-4 flex justify-between items-center">

      <h1
        className="text-xl font-bold cursor-pointer"
        onClick={() => navigate("/")}
      >
        AI Healthcare
      </h1>

      <div className="space-x-6">

        {!user && (
          <>
            <Link to="/login" className="hover:text-blue-400">Login</Link>
            <Link to="/register" className="hover:text-blue-400">Register</Link>
          </>
        )}

        {user && (
          <>
            <Link to="/dashboard" className="hover:text-blue-400">Dashboard</Link>

            <button
              onClick={logout}
              className="bg-red-500 px-3 py-1 rounded"
            >
              Logout
            </button>
          </>
        )}

      </div>

    </nav>

  )

}
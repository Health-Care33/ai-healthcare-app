import { useState, useContext } from "react"
import { Outlet, useNavigate, useLocation } from "react-router-dom"
import { AuthContext } from "../context/AuthContext"
import { MessageCircle } from "lucide-react"
import {
  Fingerprint,
  Brain,
  Activity,
  Droplet,
  Eye,
  BarChart3,
  LogOut,
  Menu,
  Home,
  User
} from "lucide-react"

export default function MainLayout(){

  const [open,setOpen] = useState(true)
  const { user, logout } = useContext(AuthContext)
  const navigate = useNavigate()
  const location = useLocation()

  const modules = [

   { name:"Home", icon:<Home size={20}/>, path:"/dashboard" },

    { name:"Fingerprint", icon:<Fingerprint size={20}/>, path:"/fingerprint" },
    { name:"Medical AI", icon:<Brain size={20}/>, path:"/medical-report-ai" },
    { name:"Retina Scan", icon:<Eye size={20}/>, path:"/retina-scan" },
    { name:"Health Risk", icon:<Activity size={20}/>, path:"/health-risk" },
    { name:"Blood Donation", icon:<Droplet size={20}/>, path:"/blood-donation" },
    { name:"Analytics", icon:<BarChart3 size={20}/>, path:"/admin-analytics" }

  ]

  // 🔥 FIXED LOGOUT
  const handleLogout = ()=>{
    localStorage.removeItem("token")
    logout && logout()
    navigate("/login")
  }

  return(

    <div className="flex min-h-screen bg-slate-900 text-white">

      {/* SIDEBAR */}
      <div className={`${open ? "w-64" : "w-20"} transition-all duration-300 bg-white/5 backdrop-blur-xl border-r border-white/10 flex flex-col justify-between`}>

        {/* TOP */}
        <div>

          <div className="flex items-center justify-between p-4">
            {open && <h1 className="font-bold">AI Health</h1>}
            <Menu onClick={()=>setOpen(!open)} className="cursor-pointer"/>
          </div>

          <div className="space-y-2 px-3 mt-4">

            {modules.map((m,i)=>(

              <div
                key={i}
                onClick={()=>navigate(m.path)}
                className={`flex items-center gap-3 p-3 rounded-xl cursor-pointer transition
                ${location.pathname === m.path ? "bg-white/20" : "hover:bg-white/10"}`}
              >
                {m.icon}
                {open && <span>{m.name}</span>}
              </div>

            ))}

          </div>

        </div>

        {/* 🔥 BOTTOM */}
        <div className="p-4 border-t border-white/10 space-y-4">
        {/* 🔥 WHATSAPP SUPPORT */}
<div
  onClick={()=>{
    window.open("https://wa.me/917020056690", "_blank")
  }}
  className="flex items-center gap-3 p-3 rounded-xl cursor-pointer hover:bg-green-500/20 transition"
>
  <MessageCircle size={20}/>
  {open && <span>WhatsApp Support</span>}
</div>

         {/* 👤 USER INFO */}
{user && open && (
  <div className="flex items-start gap-3 bg-white/10 p-3 rounded-xl overflow-hidden">

    <User size={20} className="mt-1 shrink-0"/>

    <div className="min-w-0">
      <p className="text-sm font-semibold truncate">
        {user.name}
      </p>

      <p className="text-xs text-gray-300 truncate">
        {user.email}
      </p>
    </div>

  </div>
)}

          {/* 🔥 LOGOUT */}
          {user ? (
            <div
              onClick={handleLogout}
              className="flex items-center gap-3 p-3 rounded-xl cursor-pointer hover:bg-red-500/20"
            >
              <LogOut size={20}/>
              {open && <span>Logout</span>}
            </div>
          ) : (
            <div
              onClick={()=>navigate("/login")}
              className="p-3 rounded-xl cursor-pointer hover:bg-white/10"
            >
              {open && "Login"}
            </div>
          )}

        </div>

      </div>

      {/* PAGE CONTENT */}
      <div className="flex-1 p-10">
        <Outlet/>
      </div>

    </div>

  )

}
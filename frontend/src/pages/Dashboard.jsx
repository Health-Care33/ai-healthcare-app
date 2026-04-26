import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"

import {
  Fingerprint,
  Brain,
  Activity,
  Droplet,
  Eye,
  BarChart3
} from "lucide-react"

export default function Dashboard(){

  const navigate = useNavigate()

  const cards = [

    {
      title:"Fingerprint Blood Group Detection",
      icon:<Fingerprint size={40}/>,
      route:"/fingerprint",
      color:"from-indigo-500 to-purple-500",
      desc:"AI predicts blood group using fingerprint patterns.",
      steps:["Upload fingerprint image","Click predict","Get blood group result"]
    },

    {
      title:"Medical Report AI",
      icon:<Brain size={40}/>,
      route:"/medical-report-ai",
      color:"from-pink-500 to-red-500",
      desc:"Upload reports and ask AI medical questions.",
      steps:["Upload medical report","Ask AI questions","Get smart answers"]
    },

    {
      title:"Retinal Disease Detection",
      icon:<Eye size={40}/>,
      route:"/retina-scan",
      color:"from-blue-500 to-cyan-500",
      desc:"Deep learning model detects retinal diseases.",
      steps:["Upload eye scan","Run detection","View disease + risk"]
    },

    {
      title:"Health Risk Prediction",
      icon:<Activity size={40}/>,
      route:"/health-risk",
      color:"from-green-500 to-emerald-500",
      desc:"Predict diabetes, heart risk and health score.",
      steps:["Enter health data","Submit form","View risk chart"]
    },

    {
      title:"Blood Donation Compatibility",
      icon:<Droplet size={40}/>,
      route:"/blood-donation",
      color:"from-red-500 to-rose-500",
      desc:"Find compatible blood donors instantly.",
      steps:["Enter blood group","Check compatibility","View results"]
    },

    {
      title:"Admin Analytics Dashboard",
      icon:<BarChart3 size={40}/>,
      route:"/admin-analytics",
      color:"from-orange-500 to-yellow-500",
      desc:"View AI system usage and healthcare analytics.",
      steps:["Open dashboard","View charts","Analyze data"]
    }

  ]

  const handleModuleClick = (route)=>{
    const token = localStorage.getItem("token")

    if(!token){
      navigate("/login?redirect=" + route)
    }else{
      navigate(route)
    }
  }

  return(

    <div className="text-white">

      {/* 🔥 HEADER */}
      <div className="mb-12">
        <h1 className="text-4xl font-bold mb-2">
          AI Healthcare Dashboard
        </h1>
        <p className="text-gray-400">
          Advanced Artificial Intelligence Healthcare System
        </p>
      </div>

      {/* 🔥 CARDS */}
      <div className="grid md:grid-cols-3 sm:grid-cols-2 grid-cols-1 gap-8">

        {cards.map((m,index)=>(

          <motion.div
            key={index}
            initial={{opacity:0,y:40}}
            animate={{opacity:1,y:0}}
            transition={{delay:index*0.1}}
            whileHover={{scale:1.05}}
            onClick={()=>handleModuleClick(m.route)}
            className={`cursor-pointer rounded-2xl p-8 bg-gradient-to-br ${m.color} shadow-xl hover:shadow-2xl`}
          >

            <div className="mb-6">
              {m.icon}
            </div>

            <h2 className="text-xl font-bold mb-3">
              {m.title}
            </h2>

            <p className="text-white/80 text-sm">
              {m.desc}
            </p>

          </motion.div>

        ))}

      </div>

      {/* 🔥 PAGE 2 (NEW SECTION) */}
      <div className="mt-24">

        <h2 className="text-3xl font-bold mb-10 text-center">
          How to Use Each Feature
        </h2>

        <div className="grid md:grid-cols-2 gap-8">

          {cards.map((m,index)=>(

            <motion.div
              key={index}
              initial={{opacity:0,y:40}}
              whileInView={{opacity:1,y:0}}
              transition={{delay:index*0.1}}
              className="bg-white/5 backdrop-blur-lg border border-white/10 p-6 rounded-2xl"
            >

              <h3 className="text-xl font-semibold mb-4">
                {m.title}
              </h3>

              <ul className="space-y-2 text-gray-300 text-sm">

                {m.steps.map((step,i)=>(
                  <li key={i}>
                    👉 {step}
                  </li>
                ))}

              </ul>

            </motion.div>

          ))}

        </div>

      </div>

      {/* 🔥 BOTTOM SECTION (SAME AS YOURS) */}
      <motion.div
        initial={{opacity:0}}
        animate={{opacity:1}}
        transition={{delay:0.6}}
        className="mt-20 bg-gradient-to-r from-indigo-600 to-purple-600 rounded-2xl p-10 shadow-xl"
      >

        <h2 className="text-2xl font-bold mb-3">
          AI Powered Healthcare Platform
        </h2>

        <p className="text-white/90 max-w-xl">
          This system integrates multiple AI models including fingerprint
          biometrics, retinal disease detection, OCR medical report analysis,
          and health risk prediction to assist doctors and patients with
          faster and smarter diagnosis.
        </p>

      </motion.div>

    </div>

  )

}
import { useNavigate } from "react-router-dom"
import { motion } from "framer-motion"

export default function Welcome() {

  const navigate = useNavigate()

  const features = [
    {
      title: "Fingerprint Blood Group Detection",
      desc: "AI predicts blood group using fingerprint patterns.",
      img: "https://cdn-icons-png.flaticon.com/512/3063/3063822.png"
    },
    {
      title: "Medical Report AI",
      desc: "Upload reports and ask AI medical questions.",
      img: "https://cdn-icons-png.flaticon.com/512/4712/4712109.png"
    },
    {
      title: "Retinal Disease Detection",
      desc: "Deep learning model detects retinal diseases.",
      img: "https://cdn-icons-png.flaticon.com/512/2966/2966488.png"
    },
    {
      title: "Health Risk Prediction",
      desc: "Predict diabetes, heart risk & health score.",
      img: "https://cdn-icons-png.flaticon.com/512/2966/2966327.png"
    },
    {
      title: "Blood Donation Compatibility",
      desc: "Find compatible blood donors instantly.",
      img: "https://cdn-icons-png.flaticon.com/512/4320/4320337.png"
    },
    {
      title: "Admin Analytics Dashboard",
      desc: "View AI system usage and analytics.",
      img: "https://cdn-icons-png.flaticon.com/512/1828/1828919.png"
    }
  ]

  return (
    <div className="w-full h-screen overflow-y-scroll snap-y snap-mandatory scroll-smooth">

      {/* PAGE 1 */}
      <section className="h-screen snap-start flex flex-col justify-center items-center bg-gradient-to-r from-blue-50 to-white px-10">

        <motion.h1
          initial={{ opacity: 0, y: 50 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 1 }}
          className="text-5xl font-bold text-center"
        >
          AI Healthcare Platform
        </motion.h1>

        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.5 }}
          className="mt-6 text-lg text-gray-600 text-center max-w-xl"
        >
          Advanced AI system with multiple healthcare solutions in one platform.
        </motion.p>

        <motion.img
          src="https://cdn-icons-png.flaticon.com/512/4149/4149670.png"
          className="w-72 mt-10"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.8 }}
        />
      </section>

      {/* PAGE 2 */}
      <section className="h-screen snap-start flex flex-col justify-center items-center bg-white px-10">

        <h2 className="text-4xl font-bold mb-10 text-center">
          Powerful AI Features
        </h2>

        <div className="grid grid-cols-3 gap-8">
          {features.map((f, i) => (
            <motion.div
              key={i}
              whileHover={{ scale: 1.1 }}
              initial={{ opacity: 0, y: 40 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: i * 0.1 }}
              className="bg-white shadow-xl rounded-2xl p-6 text-center"
            >
              <img src={f.img} className="w-16 mx-auto mb-4" />
              <h3 className="font-bold text-lg">{f.title}</h3>
              <p className="text-gray-500 text-sm mt-2">{f.desc}</p>
            </motion.div>
          ))}
        </div>
      </section>

      {/* PAGE 3 */}
      <section className="h-screen snap-start flex flex-col justify-center items-center bg-gradient-to-r from-indigo-50 to-white px-10">

        <motion.h2
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold text-center"
        >
          Build Your AI Healthcare System
        </motion.h2>

        <motion.p
          initial={{ opacity: 0 }}
          whileInView={{ opacity: 1 }}
          transition={{ delay: 0.3 }}
          className="mt-6 text-lg text-gray-600 text-center max-w-xl"
        >
          All-in-one AI platform for detection, prediction and analytics.
        </motion.p>

        <motion.button
          whileHover={{ scale: 1.1 }}
          whileTap={{ scale: 0.95 }}
          onClick={() => navigate("/dashboard")}
          className="mt-10 bg-blue-600 text-white px-8 py-4 rounded-full text-lg shadow-lg"
        >
          Get Started →
        </motion.button>
      </section>

    </div>
  )
}
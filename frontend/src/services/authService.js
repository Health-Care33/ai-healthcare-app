import axios from "axios"

const API = "http://127.0.0.1:8000/api/auth"

export const getProfile = async () => {

  const token = localStorage.getItem("token")

  const res = await axios.get(
    `${API}/profile`,
    {
      headers: {
        Authorization: `Bearer ${token}`
      }
    }
  )

  return res.data
}
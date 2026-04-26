import API from "./api"

export const getProfile = async () => {

  const res = await API.get("/auth/profile")

  return res.data
}
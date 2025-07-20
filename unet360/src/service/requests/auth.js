import axios from "axios";

const url = import.meta.env.VITE_API_BASE_URL;

export async function isAuthenticated() {
  const response = await axios.get(url + "auth/status/");
  return response.data;
}

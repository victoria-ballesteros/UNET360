import axios from "axios";

const url = "http://localhost:8000/";

export async function isAuthenticated() {
  const response = await axios.get(url + "auth/status/");
  return response.data;
}

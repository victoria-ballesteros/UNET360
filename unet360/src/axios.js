import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

const match = document.cookie.match(/(^|;)\s*auth=([^;]*)/);
const token = match ? match[2] : null;
api.defaults.headers.common['Authorization'] = `Bearer ${token}`;

export default api;

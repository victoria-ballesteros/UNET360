import api from "@/axios";

const url = import.meta.env.VITE_API_BASE_URL;

export async function fetchShortestPath(source, target) {
  try {
    const response = await api.get(`${url}/graph/shortest-path/${encodeURIComponent(source)}/${encodeURIComponent(target)}`);
    return response.data;
  } catch (error) {
    console.error('Error fetching shortest path:', error);
    throw error;
  }
}
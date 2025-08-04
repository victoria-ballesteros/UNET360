import api from "@/axios";
import { useAuthStore } from "@/service/stores/auth.js";

// NODES
export async function getNodes() {
  try {
    const authStore = useAuthStore();
    const token = authStore.token;
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    //
    const response = await api.get("nodes/", { headers });
    //
    return response.data;
  } catch (error) {
    //
    return null;
  }
}

export async function createNode(data) {
  try {
    const response = await api.post("nodes/", data);
    return response.data;
  } catch (error) {
    return null;
  }
}

// TAGS
export async function getTags() {
  try {
    const response = await api.get("tags/");
    return response.data;
  } catch (error) {
    return null;
  }
}

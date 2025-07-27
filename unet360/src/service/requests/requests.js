import api from "@/axios";

// NODES
export async function getNodes() {
  try {
    const response = await api.get("nodes/");
    return response.data;
  } catch (error) {
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

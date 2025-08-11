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

export async function getNodeStatuses() {
  try {
    const response = await api.get("nodes/statuses");
    return response.data;
  } catch (error) {
    return null;
  }
}

export async function deleteNode(name) {
  try {
    const authStore = useAuthStore();
    const token = authStore.token;
    const headers = token ? { Authorization: `Bearer ${token}` } : {};
    const response = await api.delete(`nodes/${encodeURIComponent(name)}`, { headers });
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

// SUPABASE
export async function uploadImageToServer(file) {
  try {
    const formData = new FormData();
    formData.append("file", file);
    const response = await api.post("upload/image", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    return null;
  }
}

// DELETE IMAGE
export async function deleteImageFromServer(fileUrl) {
  try {
    const authStore = useAuthStore();
    const token = authStore.token;
    const headers = token ? { Authorization: `Bearer ${token}` } : {};

    const cleanUrl = (val) => {
      if (typeof val === 'string') {
        const base = val.split('?')[0];
        return base.endsWith('?') ? base.slice(0, -1) : base;
      } else {
        return '';
      }
    };

    const cleaned = cleanUrl(fileUrl);

    const resp2 = await api.delete("upload/image", {
      params: { file_url: cleaned },
      headers,
    });
    return resp2.data;

  } catch (error) {
    return null;
  }
}

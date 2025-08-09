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
  console.log("Entra")
  try {
    const response = await api.post("nodes/", data);
    console.log(response.data)
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
    const response = await api.post("upload/image/", formData, {
      headers: {
        "Content-Type": "multipart/form-data",
      },
    });
    return response.data;
  } catch (error) {
    return null;
  }
}

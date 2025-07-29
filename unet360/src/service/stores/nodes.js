import { defineStore } from "pinia";
import { ref } from "vue";

import { getNodes } from "../requests/requests.js";

export const useNodeStore = defineStore("node", () => {
  const nodes = ref(null);
  const isLoading = ref(false);
  const error = ref(null);

  async function fetchNodes() {
    isLoading.value = true;
    console.log("Fetching nodes...");
    try {
      const response = await getNodes();
      console.log("Response: ", response);
      if (!response?.status) {
        error.value = new Error(
          "Respuesta inválida del servidor: status code ",
          response?.http_code
        );
        return;
      }
      nodes.value = response?.response_obj;
      error.value = null;
    } catch (err) {
      error.value = err;
    } finally {
      isLoading.value = false;
    }
  }

  return {
    nodes,
    isLoading,
    error,
    fetchNodes,
  };
});

import { defineStore } from "pinia";
import { ref } from "vue";

import { getNodes } from "../requests/requests.js";
import { useAuthStore } from "@/service/stores/auth.js";

export const useNodeStore = defineStore("node", () => {
  const nodes = ref([]);
  const isLoading = ref(false);
  const error = ref(null);

  async function fetchNodes() {
    const authStore = useAuthStore();
    if (!authStore.token) {
      return;
    }
    isLoading.value = true;
    try {
      const response = await getNodes();
      //
      if (!response?.status) {
        error.value = new Error(
          "Respuesta inválida del servidor: status code ",
          response?.http_code
        );
        //
        return;
      }
      nodes.value = [...(response?.response_obj ?? [])];
      error.value = null;
    } catch (err) {
      error.value = err;
      //
    } finally {
      isLoading.value = false;
    }
  }

  // Al inicializar el store, si el array está vacío, hacer fetch
  if (nodes.value.length === 0) {
    fetchNodes();
  }
  return {
    nodes,
    isLoading,
    error,
    fetchNodes,
  };
}, {
  persist: true,
});

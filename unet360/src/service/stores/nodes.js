import { defineStore } from "pinia";
import { ref } from "vue";

import { getNodes, getNodeStatuses } from "../requests/requests.js";
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
      const baseNodes = [...(response?.response_obj ?? [])];
      // Try to fetch statuses and merge
      try {
        const statusesResp = await getNodeStatuses();
        if (statusesResp?.status) {
          const statusMap = new Map((statusesResp.response_obj || []).map(s => [s.name, s]));
          nodes.value = baseNodes.map(n => {
            const statusEntry = statusMap.get(n.name);
            return {
              ...n,
              status: statusEntry?.status || null,
              reasons: statusEntry?.reasons || null,
            };
          });
        } else {
          nodes.value = baseNodes;
        }
      } catch (_) {
        nodes.value = baseNodes;
      }
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

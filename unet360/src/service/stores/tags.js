import { defineStore } from "pinia";
import { ref } from "vue";

import { getTags } from "../requests/requests.js";

export const useTagStore = defineStore(
  "tag",
  () => {
    const tags = ref(null);
    const isLoading = ref(false);
    const error = ref(null);

    async function fetchTags() {
      isLoading.value = true;
      try {
        const response = await getTags();
        if (!response?.status) {
          error.value = new Error(
            "Respuesta inválida del servidor: status code ",
            response?.http_code,
          );
          return;
        }
        tags.value = response?.response_obj;
        error.value = null;
      } catch (err) {
        error.value = err;
      } finally {
        isLoading.value = false;
      }
    }

    if (tags.value === null || tags.value.length === 0) {
      fetchTags();
    }

    return {
      tags,
      isLoading,
      error,
      fetchTags,
    };
  },
  {
    persist: true,
  },
);

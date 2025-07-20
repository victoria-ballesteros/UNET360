import { defineStore } from "pinia";
import { ref } from "vue";

import { isAuthenticated } from "../requests/auth";

export const useUserStore = defineStore(
  "user",
  () => {
    const user = ref(null);
    const authState = ref(null);
    const isLoading = ref(false);
    const error = ref(null);

    async function fetchUserState() {
      isLoading.value = true;
      try {
        const response = await isAuthenticated();
        authState.value = !!response?.status;
      } catch (err) {
        error.value = err;
      } finally {
        isLoading.value = false;
      }
    }

    return {
      user,
      authState,
      isLoading,
      error,
      fetchUserState,
    };
  },
  {
    persist: true,
  }
);

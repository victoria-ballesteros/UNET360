import { defineStore } from 'pinia'
import { ref } from 'vue'

import { getTags } from '../requests.js'

export const useTagStore = defineStore('tag', () => {
  const tags = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  async function fetchTags() {
    isLoading.value = true
    try {
        const response = await getTags()
        if (!response?.status){
          throw new Error('Respuesta inválida del servidor: status code ', response?.http_code)
        }
        tags.value = response?.response_obj
        error.value = null
    } catch (err) {
        console.error("Error: ", err)
        error.value = err
    } finally {
        isLoading.value = false
    }
  }

  return {
    tags,
    isLoading,
    error,
    fetchTags
  }
})

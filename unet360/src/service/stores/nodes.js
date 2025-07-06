import { defineStore } from 'pinia'
import { ref } from 'vue'

import { getNodes } from '../requests.js'

export const useNodeStore = defineStore('node', () => {
  const nodes = ref(null)
  const isLoading = ref(false)
  const error = ref(null)

  async function fetchNodes() {
    isLoading.value = true
    try {
        const response = await getNodes()
        if (!response?.status){
          throw new Error('Respuesta inválida del servidor: status code ', response?.http_code)
        }
        nodes.value = response?.response_obj
        error.value = null
    } catch (err) {
        console.error("Error: ", err)
        error.value = err
    } finally {
        isLoading.value = false
    }
  }

  return {
    nodes,
    isLoading,
    error,
    fetchNodes
  }
})

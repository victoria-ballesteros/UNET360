import axios from 'axios'

const url = 'http://localhost:8000/'

export async function getNodes() {
  const response = await axios.get(url + 'nodes/')
  return response.data
}

export async function getTags() {
  const response = await axios.get(url + 'tags/')
  return response.data
}
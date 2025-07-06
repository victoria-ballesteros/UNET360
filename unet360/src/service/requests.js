import axios from 'axios'

const url = 'http://localhost:8000/'

// NODES

export async function getNodes() {
  const response = await axios.get(url + 'nodes/')
  return response.data
}

export async function createNode() {
  
}

// TAGS

export async function getTags() {
  const response = await axios.get(url + 'tags/')
  return response.data
}

// LOCATIONS
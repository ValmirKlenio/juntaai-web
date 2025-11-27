import axios from 'axios'

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000/api'

const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

export const obterPerguntas = async () => {
  const response = await api.get('/perguntas')
  return response.data
}

export const enviarQuestionario = async (respostas) => {
  const response = await api.post('/questionario', { respostas })
  return response.data
}

export const obterEstatisticas = async () => {
  const response = await api.get('/estatisticas')
  return response.data
}

export const obterRecursosApoio = async (estado = null) => {
  const params = estado ? { estado } : {}
  const response = await api.get('/recursos-apoio', { params })
  return response.data
}

export default api

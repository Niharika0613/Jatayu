import axios from 'axios'

const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  timeout: 15000,
})

// Attach JWT token to every request
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token')
  if (token) config.headers.Authorization = `Bearer ${token}`
  return config
})

// Auto-refresh or logout on 401 or stale 404 User Not Found
api.interceptors.response.use(
  (res) => res,
  async (err) => {
    const isUserNotFound = err.response?.status === 404 && err.response?.data?.error === 'User not found'
    if (err.response?.status === 401 || isUserNotFound) {
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
      window.location.href = '/login'
    }
    return Promise.reject(err)
  }
)

export default api

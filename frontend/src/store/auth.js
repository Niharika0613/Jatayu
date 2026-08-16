import { defineStore } from 'pinia'
import { authAPI } from '../api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    token: localStorage.getItem('access_token') || null,
    loading: false,
    error: null,
  }),

  getters: {
    isLoggedIn:  (s) => !!s.token && !!s.user,
    isAdmin:     (s) => s.user?.role === 'admin',
    isStaff:     (s) => s.user?.role === 'staff',
    isTrekker:   (s) => s.user?.role === 'trekker',
    currentUser: (s) => s.user,
    userName:    (s) => s.user?.full_name || '',
  },

  actions: {
    async login(email, password) {
      this.loading = true
      this.error = null
      try {
        const res = await authAPI.login({ email, password })
        const { access_token, refresh_token, user } = res.data
        this._setSession(access_token, refresh_token, user)
        return { success: true, role: user.role }
      } catch (err) {
        this.error = err.response?.data?.error || 'Login failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    async register(formData) {
      this.loading = true
      this.error = null
      try {
        const res = await authAPI.register(formData)
        const { access_token, refresh_token, user } = res.data
        this._setSession(access_token, refresh_token, user)
        return { success: true }
      } catch (err) {
        this.error = err.response?.data?.error || 'Registration failed'
        return { success: false, error: this.error }
      } finally {
        this.loading = false
      }
    },

    logout() {
      this.user = null
      this.token = null
      localStorage.removeItem('access_token')
      localStorage.removeItem('refresh_token')
      localStorage.removeItem('user')
    },

    _setSession(token, refresh, user) {
      this.token = token
      this.user = user
      localStorage.setItem('access_token', token)
      localStorage.setItem('refresh_token', refresh)
      localStorage.setItem('user', JSON.stringify(user))
    },
  },
})

<template>
  <div class="auth-page">
    <div class="auth-bg">
      <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1200&q=80&fit=crop" alt="Himalayan landscape" />
      <div class="auth-bg-overlay"></div>
    </div>

    <div class="auth-card">
      <div class="auth-logo" style="display:flex;align-items:center;gap:10px">
        <img src="/logo-transparent.png" alt="Jatayu Logo" style="width:36px;height:auto;flex-shrink:0" />
        <div>
          <div class="logo-text">Jata<em>yu</em></div>
          <div class="logo-hindi">जटाyu · India's trekking soul</div>
        </div>
      </div>

      <h2 class="auth-title">Welcome Back!</h2>
      <p class="auth-sub">Login to your account</p>

      <div class="roles-display">
        <span class="roles-label">ROLES</span>
        <div class="roles-list">
          <span class="role-chip" style="display:inline-flex;align-items:center;gap:4px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" style="width:12px;height:12px"><rect x="3" y="11" width="18" height="11" rx="2" ry="2"></rect><path d="M7 11V7a5 5 0 0 1 10 0v4"></path></svg>
            Admin
          </span>
          <span class="role-chip" style="display:inline-flex;align-items:center;gap:4px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px"><path d="M8 3l4 8 5-5 5 15H2L8 3z"></path></svg>
            Trekking Staff
          </span>
          <span class="role-chip" style="display:inline-flex;align-items:center;gap:4px">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:12px;height:12px"><circle cx="12" cy="7" r="4"></circle><path d="M6 21v-2a6 6 0 0 1 12 0v2"></path></svg>
            User (Trekker)
          </span>
        </div>
      </div>

      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <div class="form-group">
        <label class="form-label">Email address</label>
        <input v-model="form.email" type="email" class="form-control" placeholder="your@email.com" @keyup.enter="submit" />
      </div>

      <div class="form-group">
        <label class="form-label">Password</label>
        <div class="password-input-wrapper">
          <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-control" placeholder="••••••••" @keyup.enter="submit" />
          <button type="button" class="password-toggle-btn" @click="showPassword = !showPassword" aria-label="Toggle password visibility">
            <svg v-if="showPassword" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"></path>
              <circle cx="12" cy="12" r="3"></circle>
            </svg>
            <svg v-else xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
              <path d="M17.94 17.94A10.07 10.07 0 0 1 12 20c-7 0-11-8-11-8a18.45 18.45 0 0 1 5.06-5.94M9.9 4.24A9.12 9.12 0 0 1 12 4c7 0 11 8 11 8a18.5 18.5 0 0 1-2.16 3.19m-6.72-1.07a3 3 0 1 1-4.24-4.24"></path>
              <line x1="1" y1="1" x2="23" y2="23"></line>
            </svg>
          </button>
        </div>
      </div>

      <div class="form-check">
        <input v-model="form.remember" type="checkbox" id="remember" />
        <label for="remember">Remember me</label>
      </div>

      <button class="btn-gold w-full mt-3" @click="submit" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        <span v-else>Login</span>
      </button>

      <p class="auth-switch">
        Don't have an account?
        <router-link to="/register">Register as User (Trekker)</router-link>
      </p>

      <p class="auth-note">
        <strong>Note:</strong> Only Users (Trekkers) can register themselves.<br/>Trekking Staff are created by Admin.
      </p>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../../store/auth'

const router = useRouter()
const auth   = useAuthStore()

const form    = reactive({ email: '', password: '', remember: false })
const showPassword = ref(false)
const loading = ref(false)
const error   = ref('')

async function submit() {
  if (!form.email || !form.password) { error.value = 'Email and password are required'; return }
  loading.value = true
  error.value   = ''
  const res = await auth.login(form.email, form.password)
  loading.value = false
  if (res.success) {
    if (res.role === 'admin')   router.push('/admin')
    else if (res.role === 'staff')   router.push('/staff')
    else router.push('/dashboard')
  } else {
    error.value = res.error
  }
}
</script>

<style scoped>
.auth-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  position: relative;
}
.auth-bg {
  position: fixed;
  inset: 0;
  z-index: 0;
}
.auth-bg img {
  width: 100%; height: 100%;
  object-fit: cover;
}
.auth-bg-overlay {
  position: absolute;
  inset: 0;
  background: rgba(6,14,8,0.72);
}
.auth-card {
  position: relative;
  z-index: 1;
  background: rgba(10,22,14,0.92);
  border: 0.5px solid rgba(255,255,255,0.1);
  border-radius: 18px;
  padding: 32px 36px;
  width: 400px;
  max-width: 95vw;
  backdrop-filter: blur(8px);
  max-height: 92vh;
  overflow-y: auto;
}
.auth-card::-webkit-scrollbar {
  width: 6px;
}
.auth-card::-webkit-scrollbar-track {
  background: transparent;
}
.auth-card::-webkit-scrollbar-thumb {
  background: rgba(232, 168, 56, 0.25);
  border-radius: 10px;
}
.auth-card::-webkit-scrollbar-thumb:hover {
  background: rgba(232, 168, 56, 0.45);
}
.password-input-wrapper {
  position: relative;
  width: 100%;
}
.password-toggle-btn {
  position: absolute;
  right: 12px;
  top: 50%;
  transform: translateY(-50%);
  background: transparent;
  border: none;
  color: var(--jatayu-gold);
  cursor: pointer;
  padding: 4px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 14px;
  z-index: 10;
  outline: none;
}
.password-toggle-btn:hover {
  opacity: 0.8;
}
.auth-logo {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 24px;
}
.logo-symbol {
  width: 36px; height: 36px;
  border-radius: 10px;
  background: rgba(232,168,56,0.15);
  border: 1px solid rgba(232,168,56,0.3);
  display: flex; align-items: center; justify-content: center;
  color: #E8A838; font-size: 16px;
}
.logo-text { color: #fff; font-size: 17px; font-weight: 500; }
.logo-text em { color: #E8A838; font-style: normal; }
.logo-hindi { font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 1px; }
.auth-title { color: #fff; font-size: 20px; font-weight: 500; margin: 0 0 4px; }
.auth-sub { color: rgba(255,255,255,0.4); font-size: 13px; margin: 0 0 20px; }
.roles-display { margin-bottom: 20px; }
.roles-label { font-size: 10px; color: rgba(255,255,255,0.3); text-transform: uppercase; letter-spacing: .06em; }
.roles-list { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 6px; }
.role-chip {
  font-size: 11px; padding: 3px 10px; border-radius: 20px;
  background: rgba(255,255,255,0.06); border: 0.5px solid rgba(255,255,255,0.12);
  color: rgba(255,255,255,0.6);
}
.form-check {
  display: flex; align-items: center; gap: 8px;
  font-size: 13px; color: rgba(255,255,255,0.5); margin-top: 4px;
}
.form-check input { accent-color: #E8A838; }
.w-full { width: 100%; }
.mt-3 { margin-top: 14px; }
.btn-gold { display: flex; align-items: center; justify-content: center; gap: 8px; }
.btn-gold:disabled { opacity: 0.6; cursor: not-allowed; }
.auth-switch { font-size: 13px; color: rgba(255,255,255,0.4); text-align: center; margin-top: 16px; }
.auth-switch a { color: #E8A838; text-decoration: none; }
.auth-note {
  font-size: 11px; color: rgba(255,255,255,0.3); text-align: center;
  margin-top: 14px; line-height: 1.5;
  background: rgba(255,255,255,0.03);
  border-radius: 8px; padding: 8px 12px;
}
</style>

<template>
  <div class="auth-page">
    <div class="auth-bg">
      <img src="https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=1200&q=80&fit=crop" alt="Kedarkantha trek" />
      <div class="auth-bg-overlay"></div>
    </div>

    <div class="auth-card" style="width:460px">
      <div class="auth-logo" style="display:flex;align-items:center;gap:10px">
        <img src="/logo-transparent.png" alt="Jatayu Logo" style="width:36px;height:auto;flex-shrink:0" />
        <div>
          <div class="logo-text">Jata<em>yu</em></div>
          <div class="logo-hindi">Create your account</div>
        </div>
      </div>

      <h2 class="auth-title">Create User Account</h2>
      <p class="auth-sub">Register as a Trekker</p>

      <div v-if="error" class="alert alert-error">{{ error }}</div>
      <div v-if="success" class="alert alert-success">{{ success }}</div>

      <div class="form-grid">
        <div class="form-group">
          <label class="form-label">Full Name *</label>
          <input v-model="form.full_name" type="text" class="form-control" placeholder="Your full name" />
        </div>

        <div class="form-group">
          <label class="form-label">Email Address *</label>
          <input v-model="form.email" type="email" class="form-control" placeholder="your@email.com" />
        </div>

        <div class="form-group">
          <label class="form-label">Password *</label>
          <div class="password-input-wrapper">
            <input v-model="form.password" :type="showPassword ? 'text' : 'password'" class="form-control" placeholder="Min 6 characters" />
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

        <div class="form-group">
          <label class="form-label">Confirm Password *</label>
          <div class="password-input-wrapper">
            <input v-model="form.confirm_password" :type="showConfirmPassword ? 'text' : 'password'" class="form-control" placeholder="Repeat password" />
            <button type="button" class="password-toggle-btn" @click="showConfirmPassword = !showConfirmPassword" aria-label="Toggle password visibility">
              <svg v-if="showConfirmPassword" xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
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

        <div class="form-group span-2">
          <label class="form-label">Contact Number *</label>
          <input v-model="form.contact_number" type="tel" class="form-control" placeholder="+91 9XXXXXXXXX" />
        </div>

        <!-- Jatayu extras -->
        <div class="form-group">
          <label class="form-label">Experience Level</label>
          <select v-model="form.experience_level" class="form-control">
            <option value="">Select level</option>
            <option>beginner</option>
            <option>intermediate</option>
            <option>experienced</option>
            <option>expert</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Blood Group</label>
          <select v-model="form.blood_group" class="form-control">
            <option value="">Select</option>
            <option v-for="b in bloods" :key="b">{{ b }}</option>
          </select>
        </div>

        <div class="form-group">
          <label class="form-label">Emergency Contact Name</label>
          <input v-model="form.emergency_contact_name" type="text" class="form-control" placeholder="Parent / Spouse" />
        </div>

        <div class="form-group">
          <label class="form-label">Emergency Contact Number</label>
          <input v-model="form.emergency_contact_number" type="tel" class="form-control" placeholder="+91 9XXXXXXXXX" />
        </div>
      </div>

      <button class="btn-gold w-full mt-3" @click="submit" :disabled="loading">
        <span v-if="loading" class="spinner"></span>
        <span v-else>Register</span>
      </button>

      <p class="auth-switch">
        Already have an account?
        <router-link to="/login">Login here</router-link>
      </p>

      <p class="auth-note">
        <strong>Note:</strong> Only Users (Trekkers) can register themselves.<br/>
        Trekking Staff are created by Admin.
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

const form = reactive({
  full_name: '', email: '', password: '', confirm_password: '',
  contact_number: '', experience_level: '', blood_group: '',
  emergency_contact_name: '', emergency_contact_number: '',
})
const bloods  = ['A+','A-','B+','B-','AB+','AB-','O+','O-']
const showPassword = ref(false)
const showConfirmPassword = ref(false)
const loading = ref(false)
const error   = ref('')
const success = ref('')

async function submit() {
  error.value = ''
  if (!form.full_name || !form.email || !form.password || !form.contact_number) {
    error.value = 'Full name, email, password, and contact number are required'
    return
  }
  if (form.password !== form.confirm_password) {
    error.value = 'Passwords do not match'
    return
  }
  loading.value = true
  const res = await auth.register(form)
  loading.value = false
  if (res.success) {
    success.value = 'Account created! Redirecting...'
    setTimeout(() => router.push('/dashboard'), 1200)
  } else {
    error.value = res.error
  }
}
</script>

<style scoped>
.auth-page { min-height: 100vh; display: flex; align-items: center; justify-content: center; position: relative; padding: 20px; }
.auth-bg { position: fixed; inset: 0; z-index: 0; }
.auth-bg img { width: 100%; height: 100%; object-fit: cover; }
.auth-bg-overlay { position: absolute; inset: 0; background: rgba(6,14,8,0.75); }
.auth-card {
  position: relative; z-index: 1;
  background: rgba(10,22,14,0.92); border: 0.5px solid rgba(255,255,255,0.1);
  border-radius: 18px; padding: 28px 32px; width: 460px; max-width: 95vw;
  backdrop-filter: blur(8px); max-height: 92vh; overflow-y: auto;
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
.auth-logo { display: flex; align-items: center; gap: 10px; margin-bottom: 18px; }
.logo-symbol { width: 34px; height: 34px; border-radius: 10px; background: rgba(232,168,56,.15); border: 1px solid rgba(232,168,56,.3); display: flex; align-items: center; justify-content: center; color: #E8A838; }
.logo-text { color: #fff; font-size: 16px; font-weight: 500; }
.logo-text em { color: #E8A838; font-style: normal; }
.logo-hindi { font-size: 10px; color: rgba(255,255,255,0.4); }
.auth-title { color: #fff; font-size: 19px; font-weight: 500; margin: 0 0 3px; }
.auth-sub { color: rgba(255,255,255,.4); font-size: 13px; margin: 0 0 18px; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.span-2 { grid-column: span 2; }
.w-full { width: 100%; }
.mt-3 { margin-top: 14px; }
.auth-switch { font-size: 13px; color: rgba(255,255,255,.4); text-align: center; margin-top: 14px; }
.auth-switch a { color: #E8A838; text-decoration: none; }
.auth-note { font-size: 11px; color: rgba(255,255,255,.3); text-align: center; margin-top: 12px; line-height: 1.5; background: rgba(255,255,255,.03); border-radius: 8px; padding: 8px; }
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
</style>

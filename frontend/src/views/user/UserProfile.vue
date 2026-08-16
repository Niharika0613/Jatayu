<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">My Profile</div>
          <div class="page-subtitle">Manage your Jatayu trekker profile</div>
        </div>
      </div>

      <div v-if="msg" class="alert alert-success">{{ msg }}</div>
      <div v-if="error" class="alert alert-error">{{ error }}</div>

      <div class="panel" style="max-width:560px">
        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Full Name</label>
            <input v-model="form.full_name" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Email</label>
            <input :value="form.email" class="form-control" disabled />
          </div>
          <div class="form-group">
            <label class="form-label">Contact Number</label>
            <input v-model="form.contact_number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Home City</label>
            <input v-model="form.home_city" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">State</label>
            <input v-model="form.state" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Experience Level</label>
            <select v-model="form.experience_level" class="form-control">
              <option value="">Select</option>
              <option>beginner</option><option>intermediate</option><option>experienced</option><option>expert</option>
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
            <input v-model="form.emergency_contact_name" class="form-control" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Emergency Contact Number</label>
            <input v-model="form.emergency_contact_number" class="form-control" />
          </div>
        </div>
        <button class="btn-gold mt-3" @click="save" :disabled="saving">{{ saving ? 'Saving...' : 'Save Changes' }}</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { useAuthStore } from '../../store/auth'
import { authAPI } from '../../api'

const auth = useAuthStore()
const bloods = ['A+','A-','B+','B-','AB+','AB-','O+','O-']
const saving = ref(false)
const msg = ref('')
const error = ref('')

const form = reactive({
  full_name: '', email: '', contact_number: '', home_city: '', state: '',
  experience_level: '', blood_group: '', emergency_contact_name: '', emergency_contact_number: '',
})

onMounted(() => {
  const u = auth.user
  Object.assign(form, u)
})

async function save() {
  saving.value = true
  msg.value = ''; error.value = ''
  try {
    const res = await authAPI.updateProfile(form)
    auth.user = res.data.user
    localStorage.setItem('user', JSON.stringify(res.data.user))
    msg.value = 'Profile updated successfully!'
  } catch (e) {
    error.value = e.response?.data?.error || 'Failed to update profile'
  } finally {
    saving.value = false
  }
}
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.span-2 { grid-column: span 2; }
.mt-3 { margin-top: 16px; }

/* Fix disabled input white background */
.form-control:disabled,
.form-control[disabled] {
  background: rgba(255, 255, 255, 0.03) !important;
  color: rgba(255, 255, 255, 0.35) !important;
  border-color: rgba(255, 255, 255, 0.06) !important;
  cursor: not-allowed;
  -webkit-text-fill-color: rgba(255, 255, 255, 0.35) !important;
  opacity: 1;
}
</style>

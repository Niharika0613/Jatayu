<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Staff Profile</div>
          <div class="page-subtitle">Manage your Trekking Staff details and specialties</div>
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
            <label class="form-label">Specialization</label>
            <input v-model="form.specialization" class="form-control" placeholder="e.g. High Altitude, First Aid" />
          </div>
          <div class="form-group">
            <label class="form-label">Experience (Years)</label>
            <input v-model.number="form.experience_years" type="number" class="form-control" min="0" />
          </div>
          <div class="form-group">
            <label class="form-label">Languages Spoken</label>
            <input v-model="form.languages_spoken" class="form-control" placeholder="e.g. Hindi, English" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Regions of Expertise</label>
            <input v-model="form.regions_expertise" class="form-control" placeholder="e.g. Garhwal Himalayas, Himachal Pradesh" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Certifications</label>
            <input v-model="form.certifications" class="form-control" placeholder="e.g. NIM Basic Mountaineering, Wilderness First Responder" />
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
const saving = ref(false)
const msg = ref('')
const error = ref('')

const form = reactive({
  full_name: '', email: '', contact_number: '', specialization: '', experience_years: 0,
  languages_spoken: '', regions_expertise: '', certifications: '',
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

/* Fix disabled input background */
.form-control:disabled {
  background: rgba(255, 255, 255, 0.03) !important;
  color: rgba(255, 255, 255, 0.35) !important;
  border-color: rgba(255, 255, 255, 0.06) !important;
  cursor: not-allowed;
}
</style>

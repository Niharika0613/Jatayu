<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Trekking Staff</div>
          <div class="page-subtitle">Manage trek staff accounts</div>
        </div>
        <button class="btn-gold" @click="showCreate = true">+ Create New Staff</button>
      </div>

      <div class="search-bar">
        <input v-model="search" class="search-input" placeholder="Search staff..." @input="debouncedFetch" />
      </div>

      <div class="panel">
        <table class="jatayu-table">
          <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Contact</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            <tr v-for="s in staffList" :key="s.id">
              <td>TS{{ String(s.id).padStart(3,'0') }}</td>
              <td>{{ s.full_name }}</td>
              <td>{{ s.email }}</td>
              <td>{{ s.contact_number }}</td>
              <td><span class="badge-status" :class="s.status==='active' ? 'badge-active' : 'badge-blacklisted'">{{ s.status }}</span></td>
              <td>
                <button v-if="s.status === 'active'" class="btn-danger btn-sm" @click="toggle(s, 'blacklist')">Blacklist</button>
                <button v-else class="btn-success btn-sm" @click="toggle(s, 'whitelist')">Whitelist</button>
              </td>
            </tr>
            <tr v-if="!staffList.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No staff found</td></tr>
          </tbody>
        </table>
      </div>

      <p style="font-size:11px;color:rgba(255,255,255,.3)"><strong>Note:</strong> Blacklisted staff cannot login or access the system.</p>
    </div>

    <!-- Create Staff Modal -->
    <div v-if="showCreate" class="modal-overlay" @click.self="showCreate = false">
      <div class="modal-box">
        <div class="modal-title">Create New Trekking Staff</div>
        <div v-if="formError" class="alert alert-error">{{ formError }}</div>

        <div class="form-grid">
          <div class="form-group">
            <label class="form-label">Full Name *</label>
            <input v-model="form.full_name" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Email Address *</label>
            <input v-model="form.email" type="email" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Contact Number *</label>
            <input v-model="form.contact_number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Status</label>
            <select v-model="form.status" class="form-control"><option>active</option><option>inactive</option></select>
          </div>
          <div class="form-group">
            <label class="form-label">Password *</label>
            <input v-model="form.password" type="password" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Confirm Password *</label>
            <input v-model="form.confirm_password" type="password" class="form-control" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Specialization (e.g. High Altitude, First Aid)</label>
            <input v-model="form.specialization" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Experience (years)</label>
            <input v-model.number="form.experience_years" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Languages Spoken</label>
            <input v-model="form.languages_spoken" class="form-control" placeholder="Garhwali, Hindi" />
          </div>
        </div>

        <p style="font-size:11px;color:rgba(255,255,255,.3);margin-top:10px">ℹ The staff will receive login credentials via email.</p>

        <div style="display:flex;gap:10px;margin-top:16px">
          <button class="btn-gold" @click="createStaff" :disabled="saving">{{ saving ? 'Creating...' : 'Create Staff' }}</button>
          <button class="btn-ghost" @click="showCreate = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { adminAPI } from '../../api'

const staffList = ref([])
const search = ref('')
const showCreate = ref(false)
const saving = ref(false)
const formError = ref('')

const form = reactive({
  full_name: '', email: '', contact_number: '', status: 'active',
  password: '', confirm_password: '', specialization: '',
  experience_years: null, languages_spoken: '',
})

let debounceTimer
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchStaff, 350)
}

async function fetchStaff() {
  const res = await adminAPI.listStaff({ q: search.value })
  staffList.value = res.data.staff
}

async function createStaff() {
  formError.value = ''
  if (!form.full_name || !form.email || !form.contact_number || !form.password) {
    formError.value = 'Please fill all required fields'
    return
  }
  if (form.password !== form.confirm_password) {
    formError.value = 'Passwords do not match'
    return
  }
  saving.value = true
  try {
    await adminAPI.createStaff(form)
    showCreate.value = false
    Object.assign(form, { full_name:'', email:'', contact_number:'', status:'active', password:'', confirm_password:'', specialization:'', experience_years:null, languages_spoken:'' })
    await fetchStaff()
  } catch (e) {
    formError.value = e.response?.data?.error || 'Failed to create staff'
  } finally {
    saving.value = false
  }
}

async function toggle(s, action) {
  if (action === 'blacklist') await adminAPI.blacklistStaff(s.id)
  else await adminAPI.whitelistStaff(s.id)
  await fetchStaff()
}

onMounted(fetchStaff)
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.span-2 { grid-column: span 2; }
</style>

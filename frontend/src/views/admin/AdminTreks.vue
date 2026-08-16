<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Treks</div>
          <div class="page-subtitle">Manage all trekking routes</div>
        </div>
        <button class="btn-gold" @click="openCreate">+ Add New Trek</button>
      </div>

      <div class="search-bar">
        <input v-model="search" class="search-input" placeholder="Search treks..." @input="debouncedFetch" />
      </div>

      <div class="panel">
        <table class="jatayu-table">
          <thead>
            <tr><th>ID</th><th>Trek Name</th><th>Location</th><th>Difficulty</th><th>Slots</th><th>Status</th><th>Actions</th></tr>
          </thead>
          <tbody>
            <tr v-for="t in treks" :key="t.id">
              <td>{{ t.id }}</td>
              <td>{{ t.name }}</td>
              <td>{{ t.location }}</td>
              <td>{{ t.difficulty }}</td>
              <td>{{ t.available_slots }}/{{ t.total_slots }}</td>
              <td><span class="badge-status" :class="'badge-' + t.status.toLowerCase()">{{ t.status }}</span></td>
              <td>
                <button class="btn-ghost btn-sm" @click="openEdit(t)">Edit</button>
                <button class="btn-danger btn-sm" style="margin-left:6px" @click="remove(t)">Delete</button>
              </td>
            </tr>
            <tr v-if="!treks.length"><td colspan="7" style="text-align:center;color:rgba(255,255,255,.3)">No treks found</td></tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Modal -->
    <div v-if="showModal" class="modal-overlay" @click.self="showModal = false">
      <div class="modal-box" style="width:620px">
        <div class="modal-title">{{ editingId ? 'Edit Trek' : 'Add New Trek' }}</div>
        <div v-if="formError" class="alert alert-error">{{ formError }}</div>

        <div class="form-grid">
          <div class="form-group span-2">
            <label class="form-label">Trek Name *</label>
            <input v-model="form.name" class="form-control" placeholder="e.g. Kedarkantha Trek" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Location *</label>
            <input v-model="form.location" class="form-control" placeholder="District, State" />
          </div>
          <div class="form-group">
            <label class="form-label">Difficulty *</label>
            <select v-model="form.difficulty" class="form-control">
              <option value="">Select</option>
              <option>Easy</option><option>Moderate</option><option>Hard</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Duration (days) *</label>
            <input v-model.number="form.duration_days" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Total Slots *</label>
            <input v-model.number="form.total_slots" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Available Slots</label>
            <input v-model.number="form.available_slots" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Start Date *</label>
            <input v-model="form.start_date" type="date" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">End Date *</label>
            <input v-model="form.end_date" type="date" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Assigned Staff</label>
            <select v-model="form.staff_id" class="form-control">
              <option :value="null">Unassigned</option>
              <option v-for="s in staffList" :key="s.id" :value="s.id">{{ s.full_name }}</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Status</label>
            <select v-model="form.status" class="form-control">
              <option>Pending</option><option>Approved</option><option>Open</option><option>Closed</option><option>Completed</option>
            </select>
          </div>

          <div class="form-group span-2" style="border-top:0.5px solid rgba(255,255,255,.08);padding-top:14px;margin-top:6px">
            <span style="font-size:11px;color:#E8A838;text-transform:uppercase;letter-spacing:.06em">Jatayu cultural details</span>
          </div>

          <div class="form-group">
            <label class="form-label">Category</label>
            <select v-model="form.category" class="form-control">
              <option>General</option><option>Snow</option><option>Pilgrimage</option>
              <option>Northeast</option><option>Tribal</option><option>Heritage</option>
              <option>Monsoon</option><option>Wildlife</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">State</label>
            <input v-model="form.state" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Region</label>
            <input v-model="form.region" class="form-control" placeholder="e.g. Garhwal Himalaya" />
          </div>
          <div class="form-group">
            <label class="form-label">Max Altitude (m)</label>
            <input v-model.number="form.max_altitude_m" type="number" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Nearest Railhead</label>
            <input v-model="form.nearest_railhead" class="form-control" />
          </div>
          <div class="form-group">
            <label class="form-label">Price (INR)</label>
            <input v-model.number="form.price_inr" type="number" class="form-control" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Best Season</label>
            <input v-model="form.best_season" class="form-control" placeholder="e.g. December–April" />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Cover Image URL</label>
            <input v-model="form.cover_image" class="form-control" placeholder="https://images.unsplash.com/..." />
          </div>
          <div class="form-group span-2">
            <label class="form-label">Mythological Significance</label>
            <textarea v-model="form.mythological_significance" class="form-control" rows="2"></textarea>
          </div>
          <div class="form-group span-2">
            <label class="form-label">Cultural Notes</label>
            <textarea v-model="form.cultural_notes" class="form-control" rows="2"></textarea>
          </div>
          <div class="form-group span-2">
            <label class="form-label">Description</label>
            <textarea v-model="form.description" class="form-control" rows="2"></textarea>
          </div>
        </div>

        <div style="display:flex;gap:10px;margin-top:18px">
          <button class="btn-gold" @click="save" :disabled="saving">{{ saving ? 'Saving...' : 'Save Trek' }}</button>
          <button class="btn-ghost" @click="showModal = false">Cancel</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { adminAPI } from '../../api'

const treks = ref([])
const staffList = ref([])
const search = ref('')
const showModal = ref(false)
const editingId = ref(null)
const saving = ref(false)
const formError = ref('')

const blankForm = () => ({
  name: '', location: '', difficulty: '', duration_days: null,
  total_slots: null, available_slots: null, start_date: '', end_date: '',
  staff_id: null, status: 'Pending', category: 'General', state: '', region: '',
  max_altitude_m: null, nearest_railhead: '', price_inr: null, best_season: '',
  cover_image: '', mythological_significance: '', cultural_notes: '', description: '',
})
const form = reactive(blankForm())

let debounceTimer
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchTreks, 350)
}

async function fetchTreks() {
  const res = await adminAPI.listTreks({ q: search.value })
  treks.value = res.data.treks
}

async function fetchStaff() {
  const res = await adminAPI.listStaff({ per_page: 100 })
  staffList.value = res.data.staff
}

function openCreate() {
  Object.assign(form, blankForm())
  editingId.value = null
  formError.value = ''
  showModal.value = true
}

function openEdit(t) {
  Object.assign(form, {
    ...t,
    start_date: t.start_date, end_date: t.end_date,
  })
  editingId.value = t.id
  formError.value = ''
  showModal.value = true
}

async function save() {
  formError.value = ''
  if (!form.name || !form.location || !form.difficulty || !form.duration_days || !form.total_slots || !form.start_date || !form.end_date) {
    formError.value = 'Please fill all required fields (*)'
    return
  }
  if (!form.available_slots) form.available_slots = form.total_slots

  saving.value = true
  try {
    if (editingId.value) {
      await adminAPI.updateTrek(editingId.value, form)
    } else {
      await adminAPI.createTrek(form)
    }
    showModal.value = false
    await fetchTreks()
  } catch (e) {
    formError.value = e.response?.data?.error || 'Failed to save trek'
  } finally {
    saving.value = false
  }
}

async function remove(t) {
  if (!confirm(`Delete trek "${t.name}"? This cannot be undone.`)) return
  await adminAPI.deleteTrek(t.id)
  await fetchTreks()
}

onMounted(() => {
  fetchTreks()
  fetchStaff()
})
</script>

<style scoped>
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
.span-2 { grid-column: span 2; }
textarea.form-control { resize: vertical; font-family: inherit; }
</style>

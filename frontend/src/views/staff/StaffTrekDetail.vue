<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <router-link to="/staff" style="font-size:12px;color:#E8A838;text-decoration:none">← Back to My Treks</router-link>
          <div class="page-title" style="margin-top:6px">{{ trek?.name }}</div>
        </div>
      </div>

      <div v-if="loading" class="spinner"></div>

      <template v-else-if="trek">
        <div class="trek-details-grid">
          <div class="detail-item"><span>Location</span><b>{{ trek.location }}</b></div>
          <div class="detail-item"><span>Difficulty</span><b>{{ trek.difficulty }}</b></div>
          <div class="detail-item"><span>Duration</span><b>{{ trek.duration_days }} days</b></div>
          <div class="detail-item"><span>Start Date</span><b>{{ formatDate(trek.start_date) }}</b></div>
          <div class="detail-item"><span>End Date</span><b>{{ formatDate(trek.end_date) }}</b></div>
          <div class="detail-item"><span>Total Slots</span><b>{{ trek.total_slots }}</b></div>
        </div>

        <div class="panel">
          <div class="panel-title">Manage Trek</div>
          <div class="form-grid">
            <div class="form-group">
              <label class="form-label">Available Slots</label>
              <input v-model.number="editForm.available_slots" type="number" class="form-control" :max="trek.total_slots" min="0" />
            </div>
            <div class="form-group">
              <label class="form-label">Status</label>
              <select v-model="editForm.status" class="form-control">
                <option>Open</option><option>Closed</option><option>Completed</option>
              </select>
            </div>
          </div>
          <div style="display:flex;gap:10px;margin-top:10px">
            <button class="btn-gold" @click="updateTrek">Update Trek</button>
            <button class="btn-success" @click="markCompleted" v-if="trek.status !== 'Completed'">Mark as Completed</button>
          </div>
        </div>

        <div class="panel">
          <div class="panel-title">Participants ({{ participants.length }})</div>
          <table class="jatayu-table">
            <thead><tr><th>Name</th><th>Email</th><th>Booking Date</th><th>Status</th></tr></thead>
            <tbody>
              <tr v-for="p in participants" :key="p.id">
                <td>{{ p.trekker_name }}</td>
                <td>{{ p.trekker_email }}</td>
                <td>{{ formatDate(p.booking_date) }}</td>
                <td><span class="badge-status" :class="'badge-' + p.status.toLowerCase()">{{ p.status }}</span></td>
              </tr>
              <tr v-if="!participants.length"><td colspan="4" style="text-align:center;color:rgba(255,255,255,.3)">No participants yet</td></tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { staffAPI } from '../../api'

const route = useRoute()
const trek = ref(null)
const participants = ref([])
const loading = ref(true)
const editForm = reactive({ available_slots: 0, status: 'Open' })

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function fetchTrek() {
  const res = await staffAPI.getTrek(route.params.id)
  trek.value = res.data.trek
  participants.value = res.data.participants
  editForm.available_slots = trek.value.available_slots
  editForm.status = trek.value.status === 'Completed' ? 'Closed' : trek.value.status
}

async function updateTrek() {
  if (editForm.available_slots < 0) {
    alert('Available slots cannot be negative.')
    return
  }
  if (editForm.available_slots > trek.value.total_slots) {
    alert(`Available slots (${editForm.available_slots}) cannot exceed Total Slots (${trek.value.total_slots}).`)
    return
  }
  try {
    await staffAPI.updateTrek(route.params.id, editForm)
    alert('Trek updated successfully!')
    await fetchTrek()
  } catch (e) {
    alert(e.response?.data?.error || 'Failed to update trek')
  }
}

async function markCompleted() {
  if (!confirm('Mark this trek as completed? This will complete all active bookings.')) return
  await staffAPI.completeTrek(route.params.id)
  await fetchTrek()
}

onMounted(async () => {
  await fetchTrek()
  loading.value = false
})
</script>

<style scoped>
.trek-details-grid {
  display: grid; grid-template-columns: repeat(3, 1fr); gap: 12px; margin-bottom: 20px;
}
.detail-item {
  background: rgba(255,255,255,.04); border: 0.5px solid rgba(255,255,255,.08);
  border-radius: 10px; padding: 12px 14px;
}
.detail-item span { display: block; font-size: 10px; color: rgba(255,255,255,.4); text-transform: uppercase; letter-spacing: .05em; margin-bottom: 4px; }
.detail-item b { font-size: 14px; color: #fff; font-weight: 500; }
.form-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0 14px; }
</style>

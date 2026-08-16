<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">My Dashboard</div>
          <div class="page-subtitle">Welcome, {{ auth.userName }}</div>
        </div>
      </div>

      <div v-if="loading" class="spinner"></div>
      <template v-else>
        <div class="stats-row" style="grid-template-columns:repeat(3,1fr)">
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M8 3l4 8 5-5 5 15H2L8 3z"></path></svg>
            </div>
            <div class="stat-val">{{ stats.assigned_treks }}</div>
            <div class="stat-label">Assigned Treks</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path><path d="M2 12h20"></path></svg>
            </div>
            <div class="stat-val">{{ stats.total_participants }}</div>
            <div class="stat-label">Total Participants</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M3 21h18M3 21l8-16 8 16M6.5 14h11"></path></svg>
            </div>
            <div class="stat-val">{{ stats.ongoing_treks }}</div>
            <div class="stat-label">Ongoing Treks</div>
          </div>
        </div>

        <div class="panel">
          <div class="panel-title">My Assigned Treks</div>
          <table class="jatayu-table">
            <thead>
              <tr><th>Trek Name</th><th>Dates</th><th>Participants</th><th>Slots</th><th>Status</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in treks" :key="t.id">
                <td>{{ t.name }}</td>
                <td>{{ formatDate(t.start_date) }} – {{ formatDate(t.end_date) }}</td>
                <td>{{ t.total_slots - t.available_slots }}</td>
                <td>{{ t.available_slots }}</td>
                <td><span class="badge-status" :class="'badge-' + t.status.toLowerCase()">{{ t.status }}</span></td>
                <td>
                  <router-link :to="`/staff/trek/${t.id}`" class="btn-gold btn-sm" style="text-decoration:none">
                    {{ t.status === 'Completed' ? 'View' : 'Manage' }}
                  </router-link>
                </td>
              </tr>
              <tr v-if="!treks.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No treks assigned yet</td></tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { useAuthStore } from '../../store/auth'
import { staffAPI } from '../../api'

const auth = useAuthStore()
const loading = ref(true)
const stats = ref({ assigned_treks: 0, total_participants: 0, ongoing_treks: 0 })
const treks = ref([])

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short' })
}

onMounted(async () => {
  try {
    const res = await staffAPI.dashboard()
    stats.value = res.data.stats
    treks.value = res.data.assigned_treks
  } finally {
    loading.value = false
  }
})
</script>

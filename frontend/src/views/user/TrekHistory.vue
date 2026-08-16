<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Trekking History</div>
          <div class="page-subtitle">All your completed and cancelled treks</div>
        </div>
        <button class="btn-gold" @click="exportCSV" :disabled="exporting">
          {{ exporting ? 'Exporting...' : '⬇ Export as CSV' }}
        </button>
      </div>

      <div v-if="exportMsg" class="alert alert-success">{{ exportMsg }}</div>

      <div class="stats-row" style="grid-template-columns:repeat(3,1fr)">
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M12 2l3.09 6.26L22 9.27l-5 4.87 1.18 6.88L12 17.77l-6.18 3.25L7 14.14 2 9.27l6.91-1.01L12 2z"></path></svg>
          </div>
          <div class="stat-val">{{ completedCount }}</div>
          <div class="stat-label">Treks Completed</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><polygon points="3 6 9 3 15 6 21 3 21 18 15 21 9 18 3 21"></polygon><line x1="9" y1="3" x2="9" y2="18"></line><line x1="15" y1="6" x2="15" y2="21"></line></svg>
          </div>
          <div class="stat-val">{{ statesExplored }}</div>
          <div class="stat-label">States Explored</div>
        </div>
        <div class="stat-card">
          <div class="stat-icon">
            <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M8 3l4 8 5-5 5 15H2L8 3z"></path></svg>
          </div>
          <div class="stat-val">{{ totalDays }}</div>
          <div class="stat-label">Days on Trail</div>
        </div>
      </div>

      <div class="panel">
        <table class="jatayu-table">
          <thead><tr><th>Trek Name</th><th>Trek Dates</th><th>Trekking Partner</th><th>Completed On</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-for="h in history" :key="h.id">
              <td>{{ h.trek_name }}</td>
              <td>{{ formatDate(h.trek_start_date) }} – {{ formatDate(h.trek_end_date) }}</td>
              <td>{{ h.travel_agency_name || 'Self Guided' }}</td>
              <td>{{ h.status === 'Completed' ? formatDate(h.trek_end_date) : '-' }}</td>
              <td><span class="badge-status" :class="'badge-' + h.status.toLowerCase()">{{ h.status }}</span></td>
              <td>
                <router-link v-if="h.status === 'Completed'" :to="`/treks/${h.trek_id}`" class="btn-ghost btn-sm" style="text-decoration:none">
                  Write Review
                </router-link>
                <span v-else>-</span>
              </td>
            </tr>
            <tr v-if="!history.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No history yet</td></tr>
          </tbody>
        </table>
      </div>

      <p style="font-size:11px;color:rgba(255,255,255,.3)"><strong>Note:</strong> History shows all your completed and cancelled treks.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { userAPI } from '../../api'

const history = ref([])
const exporting = ref(false)
const exportMsg = ref('')

const completedCount = computed(() => history.value.filter(h => h.status === 'Completed').length)
const statesExplored = computed(() => {
  const states = new Set(history.value.filter(h => h.status === 'Completed').map(h => h.trek_location))
  return states.size
})
const totalDays = computed(() => {
  return history.value.filter(h => h.status === 'Completed').reduce((sum, h) => {
    if (!h.trek_start_date || !h.trek_end_date) return sum
    const days = (new Date(h.trek_end_date) - new Date(h.trek_start_date)) / 86400000
    return sum + Math.round(days)
  }, 0)
})

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function fetchHistory() {
  const res = await userAPI.history()
  history.value = res.data.history
}

async function exportCSV() {
  exporting.value = true
  exportMsg.value = ''
  try {
    await userAPI.exportHistory()
    exportMsg.value = 'Export started! You will be notified by email once it is ready.'
  } finally {
    exporting.value = false
  }
}

onMounted(fetchHistory)
</script>

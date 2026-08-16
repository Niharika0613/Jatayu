<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Trek Participants</div>
          <div class="page-subtitle">Manage hikers and participants registered on your treks</div>
        </div>
      </div>

      <div v-if="loading" class="spinner"></div>

      <template v-else>
        <div class="panel">
          <table class="jatayu-table">
            <thead>
              <tr><th>Name</th><th>Email</th><th>Trek Name</th><th>Booking Date</th><th>Status</th></tr>
            </thead>
            <tbody>
              <tr v-for="p in participants" :key="p.id">
                <td><b>{{ p.trekker_name }}</b></td>
                <td>{{ p.trekker_email }}</td>
                <td>{{ p.trek_name }}</td>
                <td>{{ formatDate(p.booking_date) }}</td>
                <td><span class="badge-status" :class="'badge-' + p.status.toLowerCase()">{{ p.status }}</span></td>
              </tr>
              <tr v-if="!participants.length"><td colspan="5" style="text-align:center;color:rgba(255,255,255,.3)">No participants registered yet</td></tr>
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
import { staffAPI } from '../../api'

const loading = ref(true)
const participants = ref([])

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    const res = await staffAPI.allParticipants()
    participants.value = res.data.participants
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
</style>

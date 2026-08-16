<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">My Assigned Treks</div>
          <div class="page-subtitle">View and manage all your assigned trekking routes</div>
        </div>
      </div>

      <div v-if="loading" class="spinner"></div>

      <template v-else>
        <div class="panel">
          <table class="jatayu-table">
            <thead>
              <tr><th>Trek Name</th><th>Location</th><th>Dates</th><th>Participants</th><th>Slots Left</th><th>Status</th><th>Action</th></tr>
            </thead>
            <tbody>
              <tr v-for="t in treks" :key="t.id">
                <td><b>{{ t.name }}</b></td>
                <td>{{ t.location }}</td>
                <td>{{ formatDate(t.start_date) }} – {{ formatDate(t.end_date) }}</td>
                <td>{{ t.total_slots - t.available_slots }}</td>
                <td>{{ t.available_slots }} / {{ t.total_slots }}</td>
                <td><span class="badge-status" :class="'badge-' + t.status.toLowerCase()">{{ t.status }}</span></td>
                <td>
                  <router-link :to="`/staff/trek/${t.id}`" class="btn-gold btn-sm" style="text-decoration:none">
                    {{ t.status === 'Completed' ? 'View' : 'Manage' }}
                  </router-link>
                </td>
              </tr>
              <tr v-if="!treks.length"><td colspan="7" style="text-align:center;color:rgba(255,255,255,.3)">No treks assigned yet</td></tr>
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
const treks = ref([])

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    const res = await staffAPI.myTreks()
    treks.value = res.data.treks
  } finally {
    loading.value = false
  }
})
</script>

<style scoped>
</style>

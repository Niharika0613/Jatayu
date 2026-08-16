<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar" style="display:flex; justify-content:space-between; align-items:center">
        <div>
          <div class="page-title">Dashboard</div>
          <div class="page-subtitle">Welcome back, {{ auth.userName }}</div>
        </div>
        <div style="display:flex; gap:10px">
          <button @click="triggerDailyReminders" class="btn-gold" style="font-size:12px; padding:8px 16px">Trigger Daily Reminders ⏰</button>
          <button @click="triggerMonthlyReport" class="btn-gold" style="font-size:12px; padding:8px 16px">Trigger Monthly Report 📊</button>
          <button @click="exportBookings" class="btn-gold" style="font-size:12px; padding:8px 16px">Export All Bookings 📥</button>
        </div>
      </div>

      <div v-if="loading" class="spinner"></div>

      <template v-else>
        <!-- Statistics Cards -->
        <div class="stats-row mb-4">
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M8 3l4 8 5-5 5 15H2L8 3z"></path></svg>
            </div>
            <div class="stat-val">{{ stats.total_treks }}</div>
            <div class="stat-label">Total Treks</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><circle cx="12" cy="12" r="10"></circle><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"></path><path d="M2 12h20"></path></svg>
            </div>
            <div class="stat-val">{{ stats.total_users }}</div>
            <div class="stat-label">Total Users (Trekkers)</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M17 21v-2a4 4 0 0 0-4-4H5a4 4 0 0 0-4 4v2"></path><circle cx="9" cy="7" r="4"></circle></svg>
            </div>
            <div class="stat-val">{{ stats.total_staff }}</div>
            <div class="stat-label">Total Trekking Staff</div>
          </div>
          <div class="stat-card">
            <div class="stat-icon">
              <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-5 h-5" style="width:20px;height:20px"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line></svg>
            </div>
            <div class="stat-val">{{ stats.total_bookings }}</div>
            <div class="stat-label">Total Bookings</div>
          </div>
        </div>

        <!-- Analytics Charts -->
        <div class="charts-row mb-4">
          <div class="panel chart-container">
            <div class="panel-title">Popular Treks (Bookings Count)</div>
            <div class="chart-wrapper">
              <canvas id="popularTreksChart"></canvas>
            </div>
          </div>
          <div class="panel chart-container">
            <div class="panel-title">Bookings by Category</div>
            <div class="chart-wrapper">
              <canvas id="categoryChart"></canvas>
            </div>
          </div>
        </div>

        <!-- Recent Bookings Table -->
        <div class="panel">
          <div class="panel-title">
            Recent Bookings
            <router-link to="/admin/bookings" style="font-size:12px;color:#E8A838;text-decoration:none">View All Bookings →</router-link>
          </div>
          <table class="jatayu-table">
            <thead>
              <tr>
                <th>Booking ID</th><th>User (Trekker)</th><th>Trek</th><th>Booking Date</th><th>Status</th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="b in recentBookings" :key="b.id">
                <td>#{{ b.id }}</td>
                <td>{{ b.trekker_name }}</td>
                <td>{{ b.trek_name }}</td>
                <td>{{ formatDate(b.booking_date) }}</td>
                <td><span class="badge-status" :class="'badge-' + b.status.toLowerCase()">{{ b.status }}</span></td>
              </tr>
              <tr v-if="!recentBookings.length"><td colspan="5" style="text-align:center;color:rgba(255,255,255,.3)">No bookings yet</td></tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { useAuthStore } from '../../store/auth'
import { adminAPI } from '../../api'
import { Chart, registerables } from 'chart.js'

// Register all Chart.js components
Chart.register(...registerables)

const auth = useAuthStore()
const loading = ref(true)
const stats = ref({ total_treks: 0, total_users: 0, total_staff: 0, total_bookings: 0 })
const recentBookings = ref([])

let popularChartInstance = null
let categoryChartInstance = null

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

onMounted(async () => {
  try {
    const res = await adminAPI.dashboard()
    stats.value = res.data.stats
    recentBookings.value = res.data.recent_bookings

    // CRITICAL: Set loading to false so the v-else block is rendered in the DOM!
    loading.value = false

    // Wait for Vue to update the DOM and render the canvases
    await nextTick()

    // Initialize Popular Treks Chart
    const popularData = res.data.analytics?.popular_treks || []
    const popularCtx = document.getElementById('popularTreksChart')
    if (popularCtx && popularData.length) {
      if (popularChartInstance) {
        popularChartInstance.destroy()
      }
      popularChartInstance = new Chart(popularCtx, {
        type: 'bar',
        data: {
          labels: popularData.map(item => item.name.length > 15 ? item.name.substring(0, 15) + '...' : item.name),
          datasets: [{
            label: 'Bookings',
            data: popularData.map(item => item.count),
            backgroundColor: 'rgba(232, 168, 56, 0.65)',
            borderColor: 'rgba(232, 168, 56, 1)',
            borderWidth: 1,
            borderRadius: 4
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: { display: false },
          },
          scales: {
            y: {
              beginAtZero: true,
              ticks: { color: 'rgba(255,255,255,0.7)', stepSize: 1 },
              grid: { color: 'rgba(255,255,255,0.08)' }
            },
            x: {
              ticks: { color: 'rgba(255,255,255,0.7)' },
              grid: { color: 'rgba(255,255,255,0.08)' }
            }
          }
        }
      })
    }

    // Initialize Category Chart
    const catData = res.data.analytics?.category_distribution || []
    const catCtx = document.getElementById('categoryChart')
    if (catCtx && catData.length) {
      if (categoryChartInstance) {
        categoryChartInstance.destroy()
      }
      categoryChartInstance = new Chart(catCtx, {
        type: 'doughnut',
        data: {
          labels: catData.map(item => item.category),
          datasets: [{
            data: catData.map(item => item.count),
            backgroundColor: [
              'rgba(232, 168, 56, 0.75)',
              'rgba(30, 77, 50, 0.75)',
              'rgba(0, 168, 204, 0.75)',
              'rgba(224, 86, 36, 0.75)',
              'rgba(142, 68, 173, 0.75)',
              'rgba(189, 195, 199, 0.75)'
            ],
            borderColor: '#060e08',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: {
            legend: {
              position: 'right',
              labels: { color: 'rgba(255,255,255,0.85)' }
            }
          }
        }
      })
    }
  } catch (e) {
    console.error(e)
    loading.value = false
  }
})

const triggerDailyReminders = async () => {
  try {
    const res = await adminAPI.triggerDailyReminders()
    alert(res.data.message || 'Daily reminders triggered!')
  } catch (e) {
    alert(e.response?.data?.message || 'Error triggering daily reminders')
  }
}

const triggerMonthlyReport = async () => {
  try {
    const res = await adminAPI.triggerMonthlyReport()
    alert(res.data.message || 'Monthly report triggered!')
  } catch (e) {
    alert(e.response?.data?.message || 'Error triggering monthly report')
  }
}

const exportBookings = async () => {
  try {
    const res = await adminAPI.exportBookings()
    alert(res.data.message || 'Bookings export started successfully!')
  } catch (e) {
    alert(e.response?.data?.message || 'Error starting bookings export')
  }
}
</script>

<style scoped>
.charts-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
}
@media (max-width: 992px) {
  .charts-row {
    grid-template-columns: 1fr;
  }
}
.chart-container {
  padding: 20px;
}
.chart-wrapper {
  position: relative;
  height: 250px;
  width: 100%;
}
</style>

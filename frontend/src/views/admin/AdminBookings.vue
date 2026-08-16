<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">All Bookings</div>
          <div class="page-subtitle">Complete booking records across Jatayu</div>
        </div>
      </div>

      <div class="panel">
        <table class="jatayu-table">
          <thead>
            <tr><th>Booking ID</th><th>Trekker</th><th>Trek</th><th>Booking Date</th><th>Trek Dates</th><th>Payment</th><th>Status</th></tr>
          </thead>
          <tbody>
            <tr v-for="b in bookings" :key="b.id">
              <td>#{{ b.id }}</td>
              <td>{{ b.trekker_name }}<div style="font-size:11px;color:rgba(255,255,255,.35)">{{ b.trekker_email }}</div></td>
              <td>{{ b.trek_name }}</td>
              <td>{{ formatDate(b.booking_date) }}</td>
              <td>{{ formatDate(b.trek_start_date) }} – {{ formatDate(b.trek_end_date) }}</td>
              <td>₹{{ b.amount_paid || 0 }} <span style="color:rgba(255,255,255,.35)">({{ b.payment_status }})</span></td>
              <td><span class="badge-status" :class="'badge-' + b.status.toLowerCase()">{{ b.status }}</span></td>
            </tr>
            <tr v-if="!bookings.length"><td colspan="7" style="text-align:center;color:rgba(255,255,255,.3)">No bookings yet</td></tr>
          </tbody>
        </table>

        <div class="pagination" v-if="pages > 1">
          <button class="page-btn" v-for="p in pages" :key="p" :class="{active: p===page}" @click="goPage(p)">{{ p }}</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { adminAPI } from '../../api'

const bookings = ref([])
const page = ref(1)
const pages = ref(1)

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

async function fetchBookings() {
  const res = await adminAPI.listBookings({ page: page.value })
  bookings.value = res.data.bookings
  pages.value = res.data.pages
}

function goPage(p) { page.value = p; fetchBookings() }

onMounted(fetchBookings)
</script>

<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Partners</div>
          <div class="page-subtitle">Approve local restaurants and travel agencies</div>
        </div>
      </div>

      <div class="tabs">
        <button :class="['tab', tab==='restaurants' && 'active']" @click="tab='restaurants'">Restaurants & Cafes</button>
        <button :class="['tab', tab==='agencies' && 'active']" @click="tab='agencies'">Travel Agencies</button>
      </div>

      <div v-if="tab === 'restaurants'" class="panel">
        <table class="jatayu-table">
          <thead><tr><th>Name</th><th>Region</th><th>Type</th><th>Speciality</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-for="r in restaurants" :key="r.id">
              <td>{{ r.name }}</td>
              <td>{{ r.region }}, {{ r.state }}</td>
              <td>{{ r.type }}</td>
              <td>{{ r.speciality || '-' }}</td>
              <td><span class="badge-status" :class="'badge-' + r.status">{{ r.status }}</span></td>
              <td>
                <div style="display:flex;gap:6px">
                  <button v-if="r.status === 'pending' || r.status === 'rejected'" class="btn-success btn-sm" @click="approveR(r)">Approve</button>
                  <button v-if="r.status === 'pending' || r.status === 'approved'" class="btn-danger btn-sm" @click="rejectR(r)">Reject</button>
                  <button class="btn-ghost btn-sm" style="border-color:rgba(220,58,30,0.25);color:#ff7060" @click="deleteR(r)">Delete</button>
                </div>
              </td>
            </tr>
            <tr v-if="!restaurants.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No restaurants registered yet</td></tr>
          </tbody>
        </table>
      </div>

      <div v-else class="panel">
        <table class="jatayu-table">
          <thead><tr><th>Name</th><th>State</th><th>Services</th><th>Pricing</th><th>Status</th><th>Action</th></tr></thead>
          <tbody>
            <tr v-for="a in agencies" :key="a.id">
              <td>{{ a.name }}</td>
              <td>{{ a.state }}</td>
              <td>{{ a.services }}</td>
              <td>{{ a.pricing_tier || '-' }}</td>
              <td><span class="badge-status" :class="'badge-' + a.status">{{ a.status }}</span></td>
              <td>
                <div style="display:flex;gap:6px">
                  <button v-if="a.status === 'pending' || a.status === 'rejected'" class="btn-success btn-sm" @click="approveA(a)">Approve</button>
                  <button v-if="a.status === 'pending' || a.status === 'approved'" class="btn-danger btn-sm" @click="rejectA(a)">Reject</button>
                  <button class="btn-ghost btn-sm" style="border-color:rgba(220,58,30,0.25);color:#ff7060" @click="deleteA(a)">Delete</button>
                </div>
              </td>
            </tr>
            <tr v-if="!agencies.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No agencies registered yet</td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { adminAPI } from '../../api'

const tab = ref('restaurants')
const restaurants = ref([])
const agencies = ref([])

async function fetchRestaurants() {
  const res = await adminAPI.listRestaurants({ per_page: 50 })
  restaurants.value = res.data.restaurants
}
async function fetchAgencies() {
  const res = await adminAPI.listAgencies({ per_page: 50 })
  agencies.value = res.data.agencies
}

async function approveR(r) { await adminAPI.approveRestaurant(r.id); await fetchRestaurants() }
async function rejectR(r)  { await adminAPI.rejectRestaurant(r.id); await fetchRestaurants() }
async function deleteR(r)  { if (confirm(`Delete restaurant "${r.name}"?`)) { await adminAPI.deleteRestaurant(r.id); await fetchRestaurants() } }
async function approveA(a) { await adminAPI.approveAgency(a.id); await fetchAgencies() }
async function rejectA(a)  { await adminAPI.rejectAgency(a.id); await fetchAgencies() }
async function deleteA(a)  { if (confirm(`Delete agency "${a.name}"?`)) { await adminAPI.deleteAgency(a.id); await fetchAgencies() } }

onMounted(() => { fetchRestaurants(); fetchAgencies() })
</script>

<style scoped>
.tabs { display: flex; gap: 8px; margin-bottom: 18px; }
.tab {
  background: rgba(255,255,255,.05); border: 0.5px solid rgba(255,255,255,.1);
  color: rgba(255,255,255,.5); padding: 8px 18px; border-radius: 8px; font-size: 13px; cursor: pointer;
}
.tab.active { background: rgba(232,168,56,.15); border-color: rgba(232,168,56,.3); color: #E8A838; }
</style>

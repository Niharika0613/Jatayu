<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Users (Trekkers)</div>
          <div class="page-subtitle">Manage trekker accounts</div>
        </div>
      </div>

      <div class="search-bar">
        <input v-model="search" class="search-input" placeholder="Search users..." @input="debouncedFetch" />
      </div>

      <div class="panel">
        <table class="jatayu-table">
          <thead>
            <tr><th>ID</th><th>Name</th><th>Email</th><th>Contact</th><th>Status</th><th>Action</th></tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id">
              <td>U{{ String(u.id).padStart(4,'0') }}</td>
              <td>{{ u.full_name }}</td>
              <td>{{ u.email }}</td>
              <td>{{ u.contact_number }}</td>
              <td><span class="badge-status" :class="u.status==='active' ? 'badge-active' : 'badge-blacklisted'">{{ u.status }}</span></td>
              <td>
                <button v-if="u.status === 'active'" class="btn-danger btn-sm" @click="toggle(u, 'blacklist')">Blacklist</button>
                <button v-else class="btn-success btn-sm" @click="toggle(u, 'whitelist')">Whitelist</button>
              </td>
            </tr>
            <tr v-if="!users.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No users found</td></tr>
          </tbody>
        </table>
      </div>

      <p style="font-size:11px;color:rgba(255,255,255,.3)"><strong>Note:</strong> Blacklisted users cannot login or book treks.</p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { adminAPI } from '../../api'

const users = ref([])
const search = ref('')

let debounceTimer
function debouncedFetch() {
  clearTimeout(debounceTimer)
  debounceTimer = setTimeout(fetchUsers, 350)
}

async function fetchUsers() {
  const res = await adminAPI.listUsers({ q: search.value })
  users.value = res.data.users
}

async function toggle(u, action) {
  if (action === 'blacklist') await adminAPI.blacklistUser(u.id)
  else await adminAPI.whitelistUser(u.id)
  await fetchUsers()
}

onMounted(fetchUsers)
</script>

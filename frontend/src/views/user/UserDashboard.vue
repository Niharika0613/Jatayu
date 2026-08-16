<template>
  <div class="app-layout">
    <SidebarNav />
    <div class="main-content">
      <div class="topbar">
        <div>
          <div class="page-title">Trekkers Portal</div>
          <div class="page-subtitle">Preserving the sacred trails of Devbhumi</div>
        </div>
      </div>

      <div v-if="loading" class="spinner"></div>

      <template v-else>
        <!-- Premium Trekker Welcome Banner -->
        <div class="dashboard-hero" :style="{ backgroundImage: `linear-gradient(135deg, rgba(30, 77, 50, 0.55), rgba(6, 14, 8, 0.95)), url(${heroImage})` }">
          <div class="hero-overlay"></div>
          <div class="hero-title">Welcome Back, {{ auth.userName.split(' ')[0] }}!</div>
          <div class="hero-subtitle">
            Rank: {{ auth.user?.experience_level || 'Beginner' }} | Blood Group: {{ auth.user?.blood_group || 'O+' }}
          </div>
          <div class="hero-quote" v-html="heroQuote"></div>
          <div class="hero-stats">
            <div class="hero-stat-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="var(--jatayu-gold)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;display:inline-block;vertical-align:middle;margin-right:6px"><circle cx="12" cy="12" r="10"></circle><polyline points="12 6 12 12 16 14"></polyline></svg>
              Total Trek Days: &nbsp;<strong>{{ totalTrekDays }} Days</strong>
            </div>
            <div class="hero-stat-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="var(--jatayu-gold)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;display:inline-block;vertical-align:middle;margin-right:6px"><path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path><circle cx="12" cy="10" r="3"></circle></svg>
              Active Yatras: &nbsp;<strong>{{ activeBookingsCount }} Booked</strong>
            </div>
            <div class="hero-stat-item">
              <svg viewBox="0 0 24 24" fill="none" stroke="var(--jatayu-gold)" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" style="width:16px;height:16px;display:inline-block;vertical-align:middle;margin-right:6px"><polygon points="12 2 15.09 8.26 22 9.27 17 14.14 18.18 21.02 12 17.77 5.82 21.02 7 14.14 2 9.27 8.91 8.26 12 2"></polygon></svg>
              Status: &nbsp;<strong>Dharohar Sentinel</strong>
            </div>
          </div>
        </div>

        <!-- 🌤️ Local Weather & Safety Advisories -->
        <div class="weather-panel">
          <div v-for="w in weatherUpdates" :key="w.region" class="weather-card">
            <span class="weather-region">{{ w.region }}</span>
            <div class="weather-info">
              <span class="weather-temp">{{ w.temp }} · {{ w.cond }}</span>
              <span class="weather-status" :class="w.class">{{ w.status }}</span>
            </div>
          </div>
        </div>

        <!-- 🔥 Personalized Recommendation Alert -->
        <div class="recommend-banner">
          <span class="recommend-badge">For You</span>
          <span>We recommend <strong>{{ recommendedTreksText }}</strong> based on your <strong>{{ auth.user?.experience_level || 'Beginner' }}</strong> status.</span>
        </div>

        <!-- 🎒 Available Treks Panel -->
        <div class="panel">
          <div class="panel-title">
            Available Treks
            <div style="display:flex;gap:8px">
              <select v-model="filters.difficulty" class="filter-select" @change="filterTreks">
                <option value="">Difficulty: All</option>
                <option>Easy</option><option>Moderate</option><option>Hard</option>
              </select>
              <select v-model="filters.location" class="filter-select" @change="filterTreks">
                <option value="">Location: All</option>
                <option v-for="s in states" :key="s">{{ s }}</option>
              </select>
            </div>
          </div>

          <div class="trek-grid">
            <div v-for="t in filteredTreks" :key="t.id" class="trek-card" @click="$router.push(`/treks/${t.id}`)">
              <img class="trek-card-img" :src="t.cover_image || fallbackImg" :alt="t.name" />
              <div class="trek-card-body">
                <div class="trek-card-name">{{ t.name }}</div>
                <div class="trek-card-rating" style="font-size:11px;color:#E8A838;margin-bottom:4px">
                  <span v-if="t.avg_rating > 0">★ {{ t.avg_rating }} ({{ t.total_reviews }})</span>
                  <span v-else style="color:rgba(255,255,255,0.3)">No reviews yet</span>
                </div>
                <div class="trek-card-loc">{{ t.location }}</div>
                
                <!-- Custom Slot gauge bar -->
                <div class="slot-gauge-container">
                  <div class="slot-gauge-label">
                    <span>Slots Density</span>
                    <span :style="t.available_slots <= 5 ? 'color:#ff7060;font-weight:600' : ''">
                      {{ t.available_slots }} left
                    </span>
                  </div>
                  <div class="slot-gauge-track">
                    <div 
                      class="slot-gauge-bar" 
                      :class="t.available_slots > 15 ? 'gauge-green' : t.available_slots > 5 ? 'gauge-orange' : 'gauge-red'"
                      :style="{ width: Math.min((t.available_slots / 30) * 100, 100) + '%' }"
                    ></div>
                  </div>
                </div>

                <div class="trek-card-meta" style="margin-top: 10px;">
                  <span class="meta-pill">{{ t.difficulty }}</span>
                  <span class="meta-pill">{{ t.duration_days }}D</span>
                </div>
                <button
                  class="btn-gold btn-sm w-full mt-3"
                  :disabled="t.available_slots === 0"
                  @click.stop="book(t)"
                >
                  {{ t.available_slots > 0 ? 'Book Now' : 'Not Available' }}
                </button>
              </div>
            </div>
            <p v-if="!filteredTreks.length" style="color:rgba(255,255,255,.3);grid-column:1/-1">No treks match your filters</p>
          </div>
        </div>

        <!-- 🛡️ User Bookings Panel -->
        <div class="panel">
          <div class="panel-title">
            My Bookings
            <router-link to="/dashboard/history" style="font-size:12px;color:#E8A838;text-decoration:none">View All Bookings →</router-link>
          </div>
          <table class="jatayu-table">
            <thead><tr><th>Trek Name</th><th>Trekking Partner</th><th>Booking Date</th><th>Trek Dates</th><th>Status</th><th>Action</th></tr></thead>
            <tbody>
              <tr v-for="b in bookings" :key="b.id">
                <td>{{ b.trek_name }}</td>
                <td>{{ b.travel_agency_name || 'Self Guided' }}</td>
                <td>{{ formatDate(b.booking_date) }}</td>
                <td>{{ formatDate(b.trek_start_date) }} – {{ formatDate(b.trek_end_date) }}</td>
                <td><span class="badge-status" :class="'badge-' + b.status.toLowerCase()">{{ b.status }}</span></td>
                <td style="display:flex;gap:6px;align-items:center">
                  <router-link :to="`/treks/${b.trek_id}`" class="btn-ghost btn-sm" style="text-decoration:none">View Details</router-link>
                  <button v-if="b.status === 'Booked'" class="btn-danger btn-sm" @click="cancelBooking(b.id)">Cancel Yatra</button>
                </td>
              </tr>
              <tr v-if="!bookings.length"><td colspan="6" style="text-align:center;color:rgba(255,255,255,.3)">No bookings yet</td></tr>
            </tbody>
          </table>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import SidebarNav from '../../components/shared/SidebarNav.vue'
import { useAuthStore } from '../../store/auth'
import { userAPI, treksAPI } from '../../api'

const auth = useAuthStore()

const HERO_ASSETS = [
  {
    image: 'https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=1000&q=80',
    quote: '“चरैवेति चरैवेति” — <em>Keep walking, keep moving. The path reveals itself to those who persevere.</em>'
  },
  {
    image: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=1000&q=80',
    quote: '“सत्यं ज्ञानमनन्तं ब्रह्म” — <em>Truth, knowledge and infinity. The mountains are the home of ancient wisdom.</em>'
  },
  {
    image: 'https://images.unsplash.com/photo-1486915309851-b0cc1f8a0084?w=1000&q=80',
    quote: '“योगः कर्मसु कौशलम्” — <em>Yoga is excellence in action. Master your breath, conquer the steep climbs.</em>'
  },
  {
    image: 'https://images.unsplash.com/photo-1504280390367-361c6d9f38f4?w=1000&q=80',
    quote: '“क्षिति जल पावक गगन समीरा” — <em>Reconnect with the five sacred elements of nature in the high valleys.</em>'
  },
  {
    image: 'https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=1000&q=80',
    quote: '“गिरयः सन्तु मानवाः” — <em>Let the mountains be the protectors of mankind. Respect the sacred trails.</em>'
  }
]

const userAssetIndex = computed(() => {
  const userId = auth.user?.id || 0
  return userId % HERO_ASSETS.length
})

const heroImage = computed(() => HERO_ASSETS[userAssetIndex.value].image)
const heroQuote = computed(() => HERO_ASSETS[userAssetIndex.value].quote)
const loading = ref(true)
const treks = ref([])
const bookings = ref([])
const states = ref([])
const fallbackImg = 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&q=70&fit=crop'

const weatherUpdates = [
  { region: 'Garhwal Peaks', temp: '14°C', cond: 'Clear', status: 'Safe', class: 'status-safe' },
  { region: 'Zanskar Range', temp: '-12°C', cond: 'Heavy Snow', status: 'Caution', class: 'status-caution' },
  { region: 'Sikkim Peaks', temp: '18°C', cond: 'Rainy', status: 'Caution', class: 'status-caution' },
  { region: 'Western Ghats', temp: '22°C', cond: 'Sunny', status: 'Safe', class: 'status-safe' }
]

const recommendedTreksText = computed(() => {
  const level = (auth.user?.experience_level || 'beginner').toLowerCase()
  if (level === 'beginner') {
    return 'Brahmatal Trek and Dayara Bugyal'
  } else if (level === 'intermediate') {
    return 'Valley of Flowers and Tungnath Trek'
  } else {
    return 'Kedarnath Yatra and Chadar Frozen River'
  }
})

const totalTrekDays = computed(() => {
  return bookings.value.reduce((sum, b) => {
    if (b.status === 'Cancelled') return sum
    if (!b.trek_start_date || !b.trek_end_date) return sum
    const diffTime = Math.abs(new Date(b.trek_end_date) - new Date(b.trek_start_date))
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24)) + 1
    return sum + diffDays
  }, 0)
})

const activeBookingsCount = computed(() => {
  return bookings.value.filter(b => b.status === 'Booked').length
})

const filters = reactive({ difficulty: '', location: '' })

const filteredTreks = computed(() => {
  return treks.value.filter(t =>
    (!filters.difficulty || t.difficulty === filters.difficulty) &&
    (!filters.location || t.state === filters.location)
  )
})

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

function filterTreks() {} // reactive via computed

async function book(t) {
  try {
    await userAPI.bookTrek(t.id)
    await loadData()
  } catch (e) {
    alert(e.response?.data?.error || 'Booking failed')
  }
}

async function cancelBooking(bookingId) {
  if (!confirm('Are you sure you want to cancel this booking?')) return
  try {
    await userAPI.cancelBooking(bookingId, { reason: 'Cancelled by user' })
    await loadData()
  } catch (e) {
    alert(e.response?.data?.error || 'Cancellation failed')
  }
}

async function loadData() {
  const [dash, statesRes] = await Promise.all([userAPI.dashboard(), treksAPI.states()])
  treks.value = dash.data.available_treks
  bookings.value = dash.data.recent_bookings
  states.value = statesRes.data.states
}

onMounted(async () => {
  await loadData()
  loading.value = false
})
</script>

<style scoped>
.trek-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 14px; margin-top: 14px; }
.w-full { width: 100%; }
.mt-3 { margin-top: 14px; }

.dashboard-hero {
  position: relative;
  background: linear-gradient(135deg, rgba(30, 77, 50, 0.55), rgba(6, 14, 8, 0.95)), url('https://images.unsplash.com/photo-1544735716-392fe2489ffa?w=1000&q=80') center/cover;
  border: 1px solid rgba(232, 168, 56, 0.15);
  border-radius: 16px;
  padding: 24px 30px;
  margin-bottom: 24px;
  overflow: hidden;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.3);
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: radial-gradient(circle at top right, rgba(232, 168, 56, 0.1), transparent);
  pointer-events: none;
}

.hero-title {
  font-size: 26px;
  font-weight: 600;
  color: #fff;
  margin-bottom: 6px;
}

.hero-subtitle {
  font-size: 13px;
  color: var(--jatayu-gold);
  margin-bottom: 16px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  font-weight: 500;
}

.hero-quote {
  font-style: italic;
  font-size: 14px;
  color: rgba(255, 255, 255, 0.7);
  background: rgba(255, 255, 255, 0.04);
  border-left: 3px solid var(--jatayu-gold);
  padding: 8px 14px;
  border-radius: 4px;
  margin-bottom: 20px;
}

.hero-stats {
  display: flex;
  gap: 16px;
  flex-wrap: wrap;
}

.hero-stat-item {
  background: rgba(10, 22, 14, 0.85);
  border: 0.5px solid rgba(255, 255, 255, 0.1);
  padding: 10px 16px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: rgba(255, 255, 255, 0.8);
}

.hero-stat-item strong {
  color: var(--jatayu-gold);
}

/* Weather safety panel */
.weather-panel {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 12px;
  margin-bottom: 24px;
}

.weather-card {
  background: rgba(255, 255, 255, 0.02);
  border: 0.5px solid var(--jatayu-card-border);
  border-radius: 12px;
  padding: 12px 16px;
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.weather-region {
  font-size: 11px;
  color: var(--jatayu-muted);
  text-transform: uppercase;
  font-weight: 600;
  letter-spacing: 0.03em;
}

.weather-info {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 2px;
}

.weather-temp {
  font-size: 14px;
  font-weight: 600;
  color: #fff;
}

.weather-status {
  font-size: 10px;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 500;
}

.status-safe { background: rgba(80, 210, 140, 0.15); color: #50d28c; }
.status-caution { background: rgba(232, 168, 56, 0.15); color: var(--jatayu-gold); }

/* Recommendation Banner */
.recommend-banner {
  background: rgba(232, 168, 56, 0.06);
  border: 0.5px dashed rgba(232, 168, 56, 0.3);
  border-radius: 10px;
  padding: 12px 18px;
  margin-bottom: 24px;
  font-size: 13px;
  display: flex;
  align-items: center;
  gap: 8px;
  color: #f0f0ec;
}

.recommend-badge {
  background: var(--jatayu-gold);
  color: #000;
  font-weight: 600;
  font-size: 10px;
  padding: 2px 6px;
  border-radius: 4px;
  text-transform: uppercase;
}

/* Slot gauge styling */
.slot-gauge-container {
  margin: 10px 0;
}

.slot-gauge-label {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: var(--jatayu-muted);
  margin-bottom: 4px;
}

.slot-gauge-track {
  width: 100%;
  height: 6px;
  background: rgba(255, 255, 255, 0.08);
  border-radius: 3px;
  overflow: hidden;
}

.slot-gauge-bar {
  height: 100%;
  border-radius: 3px;
  transition: width 0.3s ease;
}

.gauge-green { background: #50d28c; }
.gauge-orange { background: #E8A838; }
.gauge-red { background: #ff7060; }
</style>

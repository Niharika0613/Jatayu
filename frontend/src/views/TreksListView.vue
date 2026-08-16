<template>
  <div class="treks-page">
    <nav class="topbar">
      <router-link to="/" class="logo-mark">
        <div class="logo-symbol">◈</div>
        <div class="logo-text">Jata<em>yu</em></div>
      </router-link>
      <div class="topbar-cta">
        <router-link to="/login" class="btn-ghost-nav">Sign in</router-link>
      </div>
    </nav>

    <div class="split-container">
      <!-- 1. Left Panel: Discover Routes Sidebar -->
      <div class="sidebar-panel">
        <div class="panel-header">
          <h2 class="title">Discover Trails</h2>
          <p class="subtitle">Explore hand-curated trails of Devbhumi</p>
        </div>

        <div class="search-filters">
          <input v-model="q" class="search-input" placeholder="Search routes..." @input="debouncedFetch" />
          <div class="filters-row">
            <select v-model="difficulty" class="filter-select" @change="fetchTreks">
              <option value="">Difficulty: All</option>
              <option>Easy</option>
              <option>Moderate</option>
              <option>Hard</option>
            </select>
            <select v-model="category" class="filter-select" @change="fetchTreks">
              <option value="">Category: All</option>
              <option v-for="c in categories" :key="c.key" :value="c.key">{{ c.label }}</option>
            </select>
          </div>
        </div>

        <div class="routes-list-scroll">
          <div 
            v-for="t in treks" 
            :key="t.id" 
            class="route-card" 
            :class="{ active: selectedTrek && selectedTrek.id === t.id }"
            @click="selectTrek(t)"
          >
            <img class="route-thumb" :src="t.cover_image || fallbackImg" :alt="t.name" />
            <div class="route-info">
              <div class="route-badge-row">
                <span class="difficulty-badge" :class="t.difficulty.toLowerCase()">{{ t.difficulty }}</span>
                <span class="rating-badge">⭐ {{ t.avg_rating > 0 ? t.avg_rating : 'New' }}</span>
              </div>
              <h4 class="route-name">{{ t.name }}</h4>
              <div class="route-specs">
                <span>⏱️ {{ t.duration_days }} Days</span>
                <span>📈 {{ t.max_altitude_m }}m</span>
                <span>₹{{ t.price_inr }}</span>
              </div>
            </div>
          </div>
          <p v-if="!treks.length" class="no-results">No trails found matching search</p>
        </div>
      </div>

      <!-- 2. Middle Panel: Selected Route Detail Card (Slide-in) -->
      <transition name="slide-panel">
        <div v-if="selectedTrek" class="details-panel">
          <div class="details-header">
            <button class="btn-close" @click="selectedTrek = null">✕</button>
            <div class="image-grid">
              <div class="grid-main">
                <img :src="selectedTrek.cover_image || fallbackImg" :alt="selectedTrek.name" />
              </div>
              <div class="grid-side">
                <img src="https://images.unsplash.com/photo-1544829099-b9a0c07fad1a?w=300&q=80&fit=crop" alt="Trail peak" />
                <img src="https://images.unsplash.com/photo-1454496522488-7a8e488e8606?w=300&q=80&fit=crop" alt="Mountain pass" />
              </div>
            </div>
          </div>

          <div class="details-body">
            <div class="badge-row">
              <span class="difficulty-badge" :class="selectedTrek.difficulty.toLowerCase()">{{ selectedTrek.difficulty }}</span>
              <span class="rating-badge" v-if="selectedTrek.avg_rating > 0">⭐ {{ selectedTrek.avg_rating }} ({{ selectedTrek.total_reviews }} reviews)</span>
            </div>
            
            <h3 class="trail-title">{{ selectedTrek.name }}</h3>
            <p class="trail-loc">{{ selectedTrek.location }}, {{ selectedTrek.state }}</p>

            <div class="specs-grid">
              <div class="spec-box">
                <span class="icon">⏱️</span>
                <span class="val">{{ selectedTrek.duration_days }} Days</span>
                <span class="lbl">Duration</span>
              </div>
              <div class="spec-box">
                <span class="icon">📈</span>
                <span class="val">{{ selectedTrek.max_altitude_m }}m</span>
                <span class="lbl">Max Altitude</span>
              </div>
              <div class="spec-box">
                <span class="icon">🎟️</span>
                <span class="val">₹{{ selectedTrek.price_inr }}</span>
                <span class="lbl">Permit & Gear</span>
              </div>
            </div>

            <div class="description-section">
              <h5>Trail Description</h5>
              <p>{{ selectedTrek.description || 'Embark on a magnificent journey through ancient trails, witness local heritage, and challenge the mighty peaks of northern India.' }}</p>
            </div>

            <div class="action-buttons-row">
              <button class="btn-action-outline" @click="downloadGPXFile(selectedTrek)">
                📥 Download GPX
              </button>
              <button class="btn-action-primary" @click="$router.push(`/treks/${selectedTrek.id}`)">
                View Details & Book
              </button>
            </div>
          </div>
        </div>
      </transition>

      <!-- 3. Right Panel: Interactive Leaflet Map -->
      <div class="map-panel">
        <div id="map-canvas"></div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, nextTick } from 'vue'
import { useRoute } from 'vue-router'
import { treksAPI } from '../api'
import L from 'leaflet'
import 'leaflet/dist/leaflet.css'

const route = useRoute()
const treks = ref([])
const categories = ref([])
const q = ref('')
const difficulty = ref('')
const category = ref(route.query.category || '')
const fallbackImg = 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=400&q=70&fit=crop'

const selectedTrek = ref(null)

let map = null
let currentPolyline = null
let currentMarkers = []

// Dynamic route paths based on locations for all 22 treks
function getTrekCoordinates(trek) {
  const name = trek.name.toLowerCase()
  if (name.includes('kedarkantha')) {
    return [
      [31.0772, 78.1889],
      [31.0664, 78.2045],
      [31.0232, 78.2198]
    ]
  } else if (name.includes('chadar')) {
    return [
      [34.0200, 77.2000],
      [33.9900, 77.2150],
      [33.9600, 77.2300],
      [33.9100, 77.2500]
    ]
  } else if (name.includes('brahmatal')) {
    return [
      [30.0163, 79.6033],
      [30.0350, 79.6100],
      [30.0833, 79.6200]
    ]
  } else if (name.includes('dayara')) {
    return [
      [30.8264, 78.6014],
      [30.8450, 78.5800],
      [30.8650, 78.5500]
    ]
  } else if (name.includes('flowers') || name.includes('valley')) {
    return [
      [30.6272, 79.5492],
      [30.6500, 79.5800],
      [30.6890, 79.5920],
      [30.7275, 79.6053]
    ]
  } else if (name.includes('hampta')) {
    return [
      [32.2272, 77.2530],
      [32.2400, 77.2750],
      [32.2790, 77.3450],
      [32.3275, 77.3850]
    ]
  } else if (name.includes('dzukou')) {
    return [
      [25.5684, 94.1283],
      [25.6050, 94.0920]
    ]
  } else if (name.includes('sandakphu')) {
    return [
      [27.0142, 88.1253],
      [27.0370, 88.0830],
      [27.0850, 88.0120],
      [27.1083, 88.0003]
    ]
  } else if (name.includes('goechala')) {
    return [
      [27.3780, 88.2201],
      [27.4200, 88.2000],
      [27.4500, 88.1900],
      [27.4830, 88.1500],
      [27.5670, 88.1670]
    ]
  } else if (name.includes('kuari')) {
    return [
      [30.5052, 79.6231],
      [30.4850, 79.6450],
      [30.4630, 79.6720],
      [30.4480, 79.7120]
    ]
  } else if (name.includes('roopkund')) {
    return [
      [30.0163, 79.6033],
      [30.1020, 79.6700],
      [30.1500, 79.7200],
      [30.2200, 79.7400],
      [30.2641, 79.7350]
    ]
  } else if (name.includes('kumara') || name.includes('pushpagiri')) {
    return [
      [12.6631, 75.6190],
      [12.6820, 75.6350],
      [12.6680, 75.6880]
    ]
  } else if (name.includes('phulara')) {
    return [
      [31.0772, 78.1889],
      [31.0950, 78.2100],
      [31.1150, 78.2400],
      [31.1275, 78.2600]
    ]
  } else if (name.includes('ranthan') || name.includes('kharak')) {
    return [
      [30.0352, 79.9450],
      [30.0820, 79.9850]
    ]
  } else if (name.includes('aancha')) {
    return [
      [32.5532, 76.1250],
      [32.4820, 76.0120]
    ]
  } else if (name.includes('pin bhaba') || name.includes('bhaba')) {
    return [
      [31.5641, 78.0120],
      [31.6200, 77.9850],
      [31.7050, 77.9250],
      [31.8100, 78.0100]
    ]
  } else if (name.includes('kedarnath')) {
    return [
      [30.6441, 79.0673],
      [30.6820, 79.0650],
      [30.7352, 79.0669]
    ]
  } else if (name.includes('hemkund')) {
    return [
      [30.6272, 79.5492],
      [30.6890, 79.5920],
      [30.7001, 79.6151]
    ]
  } else if (name.includes('tungnath')) {
    return [
      [30.4852, 79.1850],
      [30.4880, 79.2150],
      [30.4901, 79.2251]
    ]
  } else if (name.includes('shrikhand')) {
    return [
      [31.3852, 77.5120],
      [31.4250, 77.5500],
      [31.4650, 77.5900],
      [31.4872, 77.6210]
    ]
  } else if (name.includes('kinner') || name.includes('kailash')) {
    return [
      [31.5452, 78.2850],
      [31.5650, 78.3200],
      [31.5832, 78.3510]
    ]
  } else if (name.includes('amarnath')) {
    return [
      [34.2541, 75.4120],
      [34.2350, 75.4450],
      [34.2150, 75.4850],
      [34.1950, 75.5120],
      [34.2152, 75.5169]
    ]
  }
  return [
    [30.3275, 78.0325],
    [30.3450, 78.0550],
    [30.3800, 78.0720],
    [30.4020, 78.0930]
  ]
}

function initMap() {
  if (map) return
  map = L.map('map-canvas', {
    zoomControl: false
  }).setView([30.3165, 78.0322], 8)

  // OpenTopoMap for a traditional, rich physical topographic paper-map style
  L.tileLayer('https://{s}.tile.opentopomap.org/{z}/{x}/{y}.png', {
    attribution: 'Map data: © OpenStreetMap contributors, SRTM | Map style: © OpenTopoMap (CC-BY-SA)',
    maxZoom: 17
  }).addTo(map)

  L.control.zoom({
    position: 'bottomright'
  }).addTo(map)
}

function selectTrek(t) {
  selectedTrek.value = t
  
  if (!map) return

  // Clear previous layers
  if (currentPolyline) {
    map.removeLayer(currentPolyline)
  }
  currentMarkers.forEach(m => map.removeLayer(m))
  currentMarkers = []

  const coordinates = getTrekCoordinates(t)

  // Draw polyline
  currentPolyline = L.polyline(coordinates, {
    color: '#E8A838',
    weight: 4,
    opacity: 0.95
  }).addTo(map)

  // Custom start / end markers
  const startMarker = L.circleMarker(coordinates[0], {
    radius: 7,
    fillColor: '#50d28c',
    color: '#fff',
    weight: 2,
    fillOpacity: 1
  }).addTo(map).bindPopup('Trailhead: Start Point')
  
  const endMarker = L.circleMarker(coordinates[coordinates.length - 1], {
    radius: 7,
    fillColor: '#ff7060',
    color: '#fff',
    weight: 2,
    fillOpacity: 1
  }).addTo(map).bindPopup('Trail End / Shrine')

  currentMarkers.push(startMarker, endMarker)

  // Zoom and fit bounds nicely
  map.fitBounds(currentPolyline.getBounds(), {
    padding: [50, 50],
    animate: true,
    duration: 1.2
  })
}

function downloadGPXFile(t) {
  const coords = getTrekCoordinates(t)
  const trkpts = coords.map(c => `      <trkpt lat="${c[0]}" lon="${c[1]}"><ele>0</ele></trkpt>`).join('\n')
  const gpxContent = `<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.1" creator="Jatayu" xmlns="http://www.topografix.com/GPX/1/1">
  <metadata>
    <name>${t.name}</name>
    <desc>GPS Track for ${t.name}</desc>
  </metadata>
  <trk>
    <name>${t.name}</name>
    <trkseg>
${trkpts}
    </trkseg>
  </trk>
</gpx>`
  const blob = new Blob([gpxContent], { type: 'application/gpx+xml' })
  const url = URL.createObjectURL(blob)
  const a = document.createElement('a')
  a.href = url
  a.download = `${t.name.toLowerCase().replace(/\s+/g, '_')}_route.gpx`
  a.click()
  URL.revokeObjectURL(url)
}

let debounceTimer
function debouncedFetch() { clearTimeout(debounceTimer); debounceTimer = setTimeout(fetchTreks, 350) }

async function fetchTreks() {
  const res = await treksAPI.list({ q: q.value, difficulty: difficulty.value, category: category.value })
  treks.value = res.data.treks
  
  // Auto-select first trek on load if available
  if (treks.value.length && !selectedTrek.value) {
    selectTrek(treks.value[0])
  }
}

onMounted(async () => {
  initMap()
  const catRes = await treksAPI.categories()
  categories.value = catRes.data.categories
  await fetchTreks()
})
</script>

<style scoped>
.treks-page { 
  background: #060e08; 
  height: 100vh;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}
.topbar { 
  display: flex; 
  align-items: center; 
  justify-content: space-between; 
  padding: 14px 24px; 
  border-bottom: 0.5px solid rgba(255,255,255,.08); 
  height: 65px;
  flex-shrink: 0;
}
.logo-mark { display: flex; align-items: center; gap: 10px; text-decoration: none; }
.logo-symbol { width: 32px; height: 32px; border-radius: 9px; background: rgba(232,168,56,.15); border: 1px solid rgba(232,168,56,.3); display: flex; align-items: center; justify-content: center; color: #E8A838; }
.logo-text { color: #fff; font-size: 16px; font-weight: 500; }
.logo-text em { color: #E8A838; font-style: normal; }
.btn-ghost-nav { background: rgba(255,255,255,.08); border: 0.5px solid rgba(255,255,255,.18); color: #fff; font-size: 12px; padding: 7px 16px; border-radius: 8px; text-decoration: none; }

.split-container {
  display: flex;
  flex: 1;
  overflow: hidden;
  position: relative;
}

/* 1. Sidebar list pane */
.sidebar-panel {
  width: 380px;
  display: flex;
  flex-direction: column;
  border-right: 1px solid rgba(255,255,255,0.08);
  background: rgba(8, 18, 12, 0.98);
  z-index: 10;
  flex-shrink: 0;
}
.panel-header {
  padding: 20px;
  border-bottom: 0.5px solid rgba(255,255,255,0.05);
}
.panel-header .title {
  color: #fff;
  font-family: Georgia, serif;
  font-size: 20px;
  font-weight: 600;
}
.panel-header .subtitle {
  color: rgba(255,255,255,0.45);
  font-size: 11.5px;
  margin-top: 4px;
}
.search-filters {
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 10px;
  border-bottom: 0.5px solid rgba(255,255,255,0.05);
}
.search-input {
  background: rgba(255,255,255,0.04);
  border: 1px solid rgba(255,255,255,0.12);
  color: #fff;
  padding: 8px 12px;
  border-radius: 8px;
  font-size: 12.5px;
  outline: none;
  width: 100%;
}
.search-input:focus {
  border-color: #E8A838;
}
.filters-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 8px;
}
.filter-select {
  background: #0f1c12;
  border: 1px solid rgba(255,255,255,0.12);
  color: #fff;
  padding: 8px;
  border-radius: 6px;
  font-size: 11.5px;
  outline: none;
}
.filter-select option {
  background: #0d1b11;
}

.routes-list-scroll {
  flex: 1;
  overflow-y: auto;
  padding: 16px 20px;
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.route-card {
  display: flex;
  gap: 12px;
  background: rgba(255,255,255,0.02);
  border: 0.5px solid rgba(255,255,255,0.06);
  border-radius: 12px;
  padding: 10px;
  cursor: pointer;
  transition: all 0.2s ease;
}
.route-card:hover {
  background: rgba(255,255,255,0.04);
  border-color: rgba(232, 168, 56, 0.2);
}
.route-card.active {
  background: rgba(232, 168, 56, 0.08);
  border-color: #E8A838;
}
.route-thumb {
  width: 80px;
  height: 80px;
  object-fit: cover;
  border-radius: 8px;
  flex-shrink: 0;
}
.route-info {
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  flex: 1;
}
.route-badge-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.difficulty-badge {
  font-size: 9px;
  font-weight: 600;
  text-transform: uppercase;
  padding: 2px 6px;
  border-radius: 4px;
}
.difficulty-badge.easy { background: rgba(80, 210, 140, 0.15); color: #50d28c; }
.difficulty-badge.moderate { background: rgba(232, 168, 56, 0.15); color: #E8A838; }
.difficulty-badge.hard { background: rgba(255, 100, 100, 0.15); color: #ff9090; }
.rating-badge {
  font-size: 10px;
  color: #E8A838;
}
.route-name {
  color: #fff;
  font-size: 13.5px;
  font-weight: 500;
  margin: 4px 0;
}
.route-specs {
  display: flex;
  gap: 8px;
  font-size: 10.5px;
  color: rgba(255,255,255,0.4);
}

/* 2. Slide-in Details Panel */
.details-panel {
  width: 420px;
  background: rgba(8, 18, 12, 0.99);
  border-right: 1px solid rgba(255,255,255,0.08);
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  z-index: 9;
  box-shadow: 10px 0 30px rgba(0,0,0,0.5);
  flex-shrink: 0;
}
.details-header {
  position: relative;
}
.btn-close {
  position: absolute;
  top: 12px;
  right: 12px;
  z-index: 5;
  background: rgba(0,0,0,0.5);
  color: #fff;
  border: none;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  transition: background 0.2s;
}
.btn-close:hover {
  background: rgba(0,0,0,0.8);
}
.image-grid {
  display: flex;
  gap: 4px;
  height: 180px;
}
.grid-main {
  flex: 2;
}
.grid-main img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.grid-side {
  flex: 1;
  display: flex;
  flex-direction: column;
  gap: 4px;
}
.grid-side img {
  flex: 1;
  width: 100%;
  height: calc(50% - 2px);
  object-fit: cover;
}

.details-body {
  padding: 20px;
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.badge-row {
  display: flex;
  gap: 8px;
  align-items: center;
}
.trail-title {
  color: #fff;
  font-family: Georgia, serif;
  font-size: 20px;
  font-weight: 600;
  margin: 0;
}
.trail-loc {
  color: rgba(255,255,255,0.55);
  font-size: 12px;
  margin-top: -8px;
}
.specs-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 8px;
}
.spec-box {
  background: rgba(255,255,255,0.03);
  border: 0.5px solid rgba(255,255,255,0.06);
  border-radius: 8px;
  padding: 10px;
  text-align: center;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.spec-box .icon { font-size: 16px; margin-bottom: 4px; }
.spec-box .val { font-size: 12px; color: #fff; font-weight: 600; }
.spec-box .lbl { font-size: 8.5px; color: rgba(255,255,255,0.4); text-transform: uppercase; margin-top: 2px; }

.description-section h5 {
  font-size: 11.5px;
  color: rgba(255,255,255,0.45);
  text-transform: uppercase;
  letter-spacing: 0.05em;
  margin-bottom: 6px;
}
.description-section p {
  font-size: 12.5px;
  color: rgba(255,255,255,0.75);
  line-height: 1.6;
}

.action-buttons-row {
  display: grid;
  grid-template-columns: 1fr 1.2fr;
  gap: 10px;
  margin-top: 10px;
}
.btn-action-outline {
  background: transparent;
  border: 1px solid rgba(232, 168, 56, 0.4);
  color: #E8A838;
  padding: 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.2s ease;
}
.btn-action-outline:hover {
  background: rgba(232, 168, 56, 0.08);
}
.btn-action-primary {
  background: #E8A838;
  border: none;
  color: #1a0800;
  padding: 10px;
  border-radius: 8px;
  font-size: 12px;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s;
}
.btn-action-primary:hover {
  background: #f7b749;
}

/* 3. Map Panel */
.map-panel {
  flex: 1;
  height: 100%;
  position: relative;
}
#map-canvas {
  height: 100%;
  width: 100%;
}

.no-results {
  color: rgba(255,255,255,0.3);
  text-align: center;
  padding: 40px 0;
  font-size: 13px;
}

/* Transitions */
.slide-panel-enter-active, .slide-panel-leave-active {
  transition: all 0.3s ease;
}
.slide-panel-enter-from, .slide-panel-leave-to {
  transform: translateX(-100%);
  opacity: 0;
}
</style>

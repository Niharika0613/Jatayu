<template>
  <div v-if="trek" class="detail-page">
    <div class="hero">
      <img :src="trek.cover_image || fallbackImg" :alt="trek.name" />
      <div class="hero-overlay"></div>
      <nav class="hero-top">
        <router-link to="/" class="logo-mark">
          <div class="logo-symbol">◈</div>
          <div class="logo-text">Jata<em>yu</em></div>
        </router-link>
        <div class="nav-right">
          <button class="nav-btn" @click="$router.back()">← Back</button>
          <router-link v-if="!auth.isLoggedIn" to="/login" class="nav-btn primary">Sign in to book</router-link>
        </div>
      </nav>
      <div class="hero-bottom">
        <div class="cat-tags">
          <span class="tag">{{ trek.category }}</span>
          <span v-if="trek.permit_required" class="tag tag-permit">Permit required</span>
          <span v-else class="tag">No permit needed</span>
        </div>
        <div class="hero-title">{{ trek.name }}</div>
        <div class="hero-subtitle">{{ trek.location }} · {{ trek.region }} · {{ trek.max_altitude_m }}m</div>
      </div>
    </div>

    <!-- Sliding Itinerary Drawer (Fixed on the far left edge of the viewport) -->
    <div class="left-itinerary-drawer" :class="{ 'drawer-open': isItineraryOpen }">
      <!-- Toggle Handle Tab -->
      <button class="drawer-handle-tab" @click="isItineraryOpen = !isItineraryOpen">
        <span class="handle-text">ITINERARY</span>
        <span class="handle-arrow">{{ isItineraryOpen ? '◀' : '▶' }}</span>
      </button>

      <!-- Drawer Content -->
      <div class="drawer-inner" v-if="trek">
        <div class="drawer-header">
          <div class="drawer-header-title">Stage Wise Planner</div>
          <button class="drawer-close-btn" @click="isItineraryOpen = false">✕</button>
        </div>
        <div class="drawer-body">
          <div class="itinerary-timeline">
            <div v-for="(day, index) in parsedItinerary" :key="index" class="itinerary-node">
              <div class="node-left">
                <div class="node-day">{{ day.day }}</div>
              </div>
              <div class="node-connector">
                <div class="node-dot"><span class="dot-inner"></span></div>
                <div class="node-line" v-if="index !== parsedItinerary.length - 1"></div>
              </div>
              <div class="node-content">
                <div class="node-title">{{ day.title }}</div>
                <div class="node-details" v-if="day.dist || day.alt">
                  <span v-if="day.dist" class="node-pill">Distance: {{ day.dist }}</span>
                  <span v-if="day.alt" class="node-pill">Altitude: {{ day.alt }}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Original stat-strip -->
    <div class="stat-strip">
      <div class="stat-item"><div class="stat-val">{{ trek.duration_days }}</div><div class="stat-key">Days</div></div>
      <div class="stat-item"><div class="stat-val">{{ trek.difficulty }}</div><div class="stat-key">Difficulty</div></div>
      <div class="stat-item"><div class="stat-val accent">{{ trek.max_altitude_m }}m</div><div class="stat-key">Max altitude</div></div>
      <div class="stat-item"><div class="stat-val">{{ trek.best_season || '-' }}</div><div class="stat-key">Best season</div></div>
      <div class="stat-item"><div class="stat-val">{{ trek.nearest_railhead || '-' }}</div><div class="stat-key">Railhead</div></div>
    </div>

    <!-- Live Safety Advisory Ticker (Full-width scrolling band) -->
    <div v-if="trek.safety_alerts" class="safety-marquee-band">
      <div class="marquee-content">
        <span v-for="n in 6" :key="n" class="ticker-text">
          TRAIL ADVISORY: {{ trek.safety_alerts }} &nbsp;&nbsp;·&nbsp;&nbsp;
        </span>
      </div>
    </div>

    <div class="body">

      <!-- About the Trek -->
      <div v-if="trek.description" class="section">
        <div class="sec-head">About this trek</div>
        <div class="dark-card">
          <div class="overview-text mb-4">{{ trek.description }}</div>
          
          <!-- Details specs & Highlights grid -->
          <div class="trek-extended-details mt-4">
            <div class="specs-grid">
              <div class="spec-card">
                <span class="spec-icon">◈</span>
                <div>
                  <div class="spec-label">Terrain Type</div>
                  <div class="spec-val">{{ getTrekTerrain(trek.name) }}</div>
                </div>
              </div>
              <div class="spec-card">
                <span class="spec-icon">◈</span>
                <div>
                  <div class="spec-label">Trail Type</div>
                  <div class="spec-val">{{ getTrekTrailType(trek.name) }}</div>
                </div>
              </div>
              <div class="spec-card">
                <span class="spec-icon">◈</span>
                <div>
                  <div class="spec-label">Fitness Required</div>
                  <div class="spec-val">Excellent Endurance & Acclimatization</div>
                </div>
              </div>
              <div class="spec-card">
                <span class="spec-icon">◈</span>
                <div>
                  <div class="spec-label">Flora & Fauna</div>
                  <div class="spec-val">Alpine Meadows, Monals, Blue Sheep</div>
                </div>
              </div>
            </div>
            
            <div class="highlights-section mt-4">
              <h5 class="highlights-title">Trail Highlights</h5>
              <ul class="highlights-list">
                <li v-for="(hl, idx) in trekHighlights" :key="idx">
                  <span class="hl-marker">◈</span> {{ hl }}
                </li>
              </ul>
            </div>
          </div>
        </div>
      </div>

      <!-- Mythology and Legend (Devbhumi Gatha) -->
      <div v-if="trek.mythological_significance" class="section mythology-section">
        <div class="sec-head --mythology">
          <span class="symbol">◈</span> Devbhumi Gatha (Sacred Legend)
        </div>
        <div class="mythology-card">
          <div class="card-glow"></div>
          <div class="myth-text">
            {{ trek.mythological_significance }}
          </div>
        </div>
      </div>

      <!-- Culture Hub: Expandable/Collapsible Drawer (Moved up) -->
      <div class="culture-explorer-panel mt-4">
        <div class="explorer-banner">
          <div class="banner-content">
            <h4>Local Heritage & Traditional Trails</h4>
            <p>Learn more about the local culture, cuisine, festivals, and where to eat near the trail.</p>
          </div>
          <button class="btn-toggle-culture" @click="showCultureExplorer = !showCultureExplorer">
            {{ showCultureExplorer ? 'Hide Culture Guide ✕' : 'Explore Culture & Local Food' }}
          </button>
        </div>

        <div v-if="showCultureExplorer" class="explorer-tab-content mt-3">
          <!-- Local Food -->
          <div class="sub-culture-section">
            <h5 class="sub-section-title">Traditional Food Trail (Eat Like a Local)</h5>
            <div v-if="localFood.length" class="food-scroll">
              <div v-for="f in localFood" :key="f.id" class="food-card">
                <img v-if="f.photo_url" class="food-img" :src="f.photo_url" :alt="f.name" />
                <div v-else class="food-img-placeholder">Local Dish</div>
                <div class="food-body">
                  <div class="food-name">{{ f.name }} <span v-if="f.hindi_name" style="color:rgba(255,255,255,.4);font-weight:400">{{ f.hindi_name }}</span></div>
                  <div class="food-desc">{{ f.description }}</div>
                  <span class="food-tag">{{ f.is_vegetarian ? 'Veg' : 'Non-veg' }} · {{ f.category }}</span>
                </div>
              </div>
            </div>
            <p v-else class="no-data-text">Local food menu is currently being compiled for this trail.</p>
          </div>

          <!-- Culture & Festivals with Traditional Videos/Photos -->
          <div class="sub-culture-section mt-4">
            <h5 class="sub-section-title">Indigenous Culture & Festivals</h5>
            <div v-if="trek.cultural_notes || trek.local_tribe_culture || trek.hidden_places" class="culture-grid">
              <div v-if="trek.local_tribe_culture" class="cult-item">
                <div class="cult-label">Local Tribe / Language</div>
                <div class="cult-val">{{ trek.local_tribe_culture }}</div>
              </div>
              <div v-if="trek.cultural_notes" class="cult-item">
                <div class="cult-label">Cultural Context</div>
                <div class="cult-val">{{ trek.cultural_notes }}</div>
                <a v-if="trek.state && trek.state.toLowerCase().includes('ladakh')" href="https://www.instagram.com/reel/DXOfflyj76J/" target="_blank" class="cult-reel-link mt-2">
                  Watch: Gur Gur Chai Preparation →
                </a>
              </div>
              <div v-if="trek.festivals_enroute" class="cult-item">
                <div class="cult-label">Festivals en route</div>
                <div class="cult-val">
                  {{ trek.festivals_enroute }}
                  <a v-if="trek.name && trek.name.toLowerCase().includes('dayara')" href="https://www.instagram.com/reel/C_H9cdRJlta/" target="_blank" class="cult-reel-inline-link">
                    (Watch Celebration →)
                  </a>
                </div>
              </div>
              <div v-if="trek.hidden_places" class="cult-item">
                <div class="cult-label">Hidden Trails & Offbeat Attractions</div>
                <div class="cult-val">{{ trek.hidden_places }}</div>
              </div>
            </div>
            <p v-else class="no-data-text">Cultural archives are currently being compiled for this trail.</p>

            <!-- Traditional Heritage Photo Gallery (Dynamic) -->
            <div class="culture-gallery-section mt-4" v-if="heritagePhotos.length">
              <h5 class="sub-section-title">Traditional Heritage Photo Gallery</h5>
              <div class="heritage-gallery-carousel mt-2">
                <div v-for="(photo, pidx) in heritagePhotos" :key="pidx" class="heritage-carousel-item">
                  <img :src="photo.src" :alt="photo.title" />
                  <div class="gallery-caption">{{ photo.title }}</div>
                </div>
              </div>
            </div>

            <!-- Traditional Heritage Video Trail (Dynamic & Targeted) -->
            <div class="culture-video-section mt-4" v-if="trek.state && (trek.state.toLowerCase().includes('himachal') || trek.state.toLowerCase().includes('ladakh') || trek.state.toLowerCase().includes('nagaland') || trek.state.toLowerCase().includes('west bengal') || trek.state.toLowerCase().includes('sikkim') || (trek.name && trek.name.toLowerCase().includes('dayara')))">
              <h5 class="sub-section-title">Traditional Heritage Video Trail</h5>
              
              <!-- West Bengal & Sikkim video list -->
              <div v-if="trek.state.toLowerCase().includes('west bengal') || trek.state.toLowerCase().includes('sikkim')" class="wb-videos-grid">
                <div class="video-item">
                  <div class="video-container">
                    <video controls loop muted class="heritage-video">
                      <source src="https://v1.pinimg.com/videos/iht/expMp4/5b/2f/9c/5b2f9cfa6ae3324f63f6f5c9bf7b9e70_720w.mp4" type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                    <div class="video-caption">Sacred Buddhist Cham Mask Dance (Sandakphu & Sikkim Border)</div>
                  </div>
                </div>
                <div class="video-item">
                  <div class="video-container">
                    <video controls loop muted class="heritage-video">
                      <source src="https://v1.pinimg.com/videos/mc/720p/55/f7/31/55f731272c6a5f18f00c729e337a345a.mp4" type="video/mp4" />
                      Your browser does not support the video tag.
                    </video>
                    <div class="video-caption">Saga Dawa Holy Month Rituals & Celebrations</div>
                  </div>
                </div>
              </div>

              <!-- Other states -->
              <div v-else class="video-container mt-2">
                <video controls loop muted class="heritage-video">
                  <source :src="getHeritageVideoSrc(trek.state, trek.name)" type="video/mp4" />
                  Your browser does not support the video tag.
                </video>
                <div class="video-caption">{{ getHeritageVideoCaption(trek.state, trek.name) }}</div>
              </div>
            </div>

          </div>

          <!-- Where to Eat (with Owner contacts and call buttons) -->
          <div class="sub-culture-section mt-4">
            <h5 class="sub-section-title">Local Eateries & Bhojanalayas</h5>
            <div v-if="restaurants.length" class="partner-grid">
              <div v-for="r in restaurants" :key="r.id" class="partner-card eatery-card">
                <div class="partner-name">{{ r.name }} <span class="verified" v-if="r.is_verified">✓</span></div>
                <div class="partner-meta">{{ r.village }}, {{ r.region }} · {{ r.distance_from_trailhead_km }}km from trailhead</div>
                <div class="partner-desc">{{ r.speciality }}</div>
                <!-- Contact info & direct dial tel call action -->
                <div class="eatery-contact-info mt-3">
                  <div class="contact-row">Host: <b>{{ r.owner_name || 'Local Resident' }}</b></div>
                  <div class="contact-row">Phone: <b>{{ r.contact_number || '+91 98765 43210' }}</b></div>
                  <a :href="'tel:' + (r.contact_number || '+919876543210')" class="btn-call-eatery mt-2">Call Eatery</a>
                </div>
              </div>
            </div>
            <p v-else class="no-data-text">No local eateries or dharamsalas listed near the trailhead yet.</p>
          </div>
        </div>
      </div>

      <!-- Elevation Chart Section (Moved down) -->
      <div v-if="trek.elevation_profile" class="section mt-4">
        <div class="sec-head">Elevation Profile</div>
        <div class="elevation-chart-card">
          <div class="chart-container-wrapper">
            <canvas id="elevationChart"></canvas>
          </div>
        </div>
      </div>

      <!-- Partner Selector Card & Dossier -->
      <div v-if="agencies.length && trek.is_bookable" class="partner-selector-card mt-4">
        <div class="selector-header">
          <span class="selector-icon">◈</span>
          <span class="selector-title">Select Trekking Partner</span>
        </div>
        <div class="selector-body">
          <p class="selector-help-text">Choose between a self-guided trip or booking a packaged tour with a verified travel partner:</p>
          <select id="agency-select" v-model="selectedAgencyId" class="partner-select">
            <option :value="null">Self Guided / Base Trek — ₹{{ trek.price_inr }}</option>
            <option v-for="a in agencies" :key="a.id" :value="a.id">
              {{ a.name }} ({{ a.pricing_tier.toUpperCase() }}) — ₹{{ a.package_starting_price_inr }}
            </option>
          </select>

          <!-- Selected Partner Details Dossier -->
          <div v-if="selectedAgency" class="selected-partner-card mt-3">
            <div class="partner-card-header">
              <span class="badge-status badge-approved">VERIFIED PARTNER DETAILS</span>
              <h4>{{ selectedAgency.name }}</h4>
            </div>
            <div class="partner-card-body">
              <div class="partner-info-row">
                <span>Contact:</span> <b>{{ selectedAgency.contact_number }}</b>
              </div>
              <div class="partner-info-row">
                <span>Email:</span> <b>{{ selectedAgency.email }}</b>
              </div>
              <div class="partner-info-row" v-if="selectedAgency.website">
                <span>Website:</span> <b><a :href="'http://' + selectedAgency.website" target="_blank" style="color:var(--jatayu-gold);text-decoration:none">{{ selectedAgency.website }}</a></b>
              </div>
              <div class="partner-info-row">
                <span>Base Area:</span> <b>{{ selectedAgency.base_city }}, {{ selectedAgency.state }}</b>
              </div>
              <div class="partner-info-row">
                <span>Credentials:</span> <b style="color:#50d28c">{{ selectedAgency.certifications || 'IMF Certified Partner' }}</b>
              </div>
              <div class="partner-services-list mt-2">
                <span v-for="s in selectedAgency.services.split(',')" :key="s" class="meta-pill">{{ s.replace('_', ' ') }}</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Review placeholder info card for logged out or ineligible users -->
      <div v-if="!myBooking" class="review-placeholder-card mb-4 mt-4">
        <div class="placeholder-icon">◈</div>
        <div class="placeholder-text-content">
          <div class="placeholder-title">Verified Reviews Only</div>
          <div class="placeholder-desc" v-if="!auth.isLoggedIn">
            Please <router-link to="/login" style="color:#E8A838;text-decoration:underline">Sign In</router-link> with a trekker account (e.g., <code>amit@gmail.com</code> / <code>Password@123</code>) to write reviews.
          </div>
          <div class="placeholder-desc" v-else>
            Only trekkers with active bookings can write reviews. Book this trek to write a review after completion!
          </div>
        </div>
      </div>

      <!-- Verified Review Submission Form -->
      <div v-if="myBooking" class="review-form-card mb-4 mt-4">
        <div class="form-title">Submit a Verified Review</div>
        <p class="form-help">Since you completed this trek, you can share your experience and trail conditions with other hikers:</p>
        
        <div class="form-row">
          <div class="form-group">
            <label class="form-label">Rating Stars</label>
            <select v-model="newReview.rating" class="form-input select-stars">
              <option value="5">★★★★★ (5 Stars)</option>
              <option value="4">★★★★☆ (4 Stars)</option>
              <option value="3">★★★☆☆ (3 Stars)</option>
              <option value="2">★★☆☆☆ (2 Stars)</option>
              <option value="1">★☆☆☆☆ (1 Star)</option>
            </select>
          </div>
          <div class="form-group">
            <label class="form-label">Trail Condition</label>
            <select v-model="newReview.trail_condition" class="form-input">
              <option value="Clear">Clear / Dry</option>
              <option value="Snowy">Snowy / Icy</option>
              <option value="Muddy">Muddy / Slushy</option>
              <option value="Rocky">Rocky / Rough</option>
              <option value="Overgrown">Overgrown / Wild</option>
            </select>
          </div>
        </div>
        
        <div class="form-group mt-2">
          <label class="form-label">Written Comment</label>
          <textarea v-model="newReview.comment" class="form-input text-area" placeholder="Describe the trail conditions, difficulty, views, or helpful tips..."></textarea>
        </div>
        
        <button class="submit-review-btn mt-2" @click="submitReview" :disabled="submittingReview">
          {{ submittingReview ? 'Submitting...' : 'Submit Verified Review' }}
        </button>
        <div v-if="reviewErr" class="alert alert-error mt-2">{{ reviewErr }}</div>
      </div>

      <!-- Reviews list -->
      <div class="section mt-4">
        <div class="sec-head">Trekker Reviews</div>
        <div class="reviews-list">
          <div v-for="r in reviews" :key="r.id" class="review-card">
            <div class="review-header">
              <div>
                <span class="stars-display">{{ '★'.repeat(r.rating) }}{{ '☆'.repeat(5 - r.rating) }}</span>
                <span class="reviewer-name">{{ r.reviewer_name }}</span>
              </div>
              <span v-if="r.trail_condition" class="condition-badge" :class="'condition-' + r.trail_condition.toLowerCase()">
                {{ r.trail_condition }}
              </span>
            </div>
            <p class="review-comment">{{ r.comment || 'No comment provided.' }}</p>
            <span class="review-date">{{ formatDate(r.created_at) }} · Verified Booking</span>
          </div>
          <p v-if="!reviews.length" style="color:rgba(255,255,255,.3);text-align:center;padding:20px">No reviews yet. Be the first to review!</p>
        </div>
      </div>

      <!-- Jatayu Dharohar Conservation Pledge -->
      <div v-if="trek.is_bookable" class="pledge-card mt-4">
        <div class="pledge-header">
          <span class="pledge-icon">◈</span>
          <span class="pledge-title">The Jatayu Dharohar Pledge</span>
        </div>
        <label class="pledge-checkbox-label">
          <input type="checkbox" v-model="acceptPledge" class="pledge-checkbox" />
          <span class="pledge-text">
            I pledge to respect local traditions, keep the mountain trails plastic-free, support native guides, and protect the sacred heritage of Devbhumi.
          </span>
        </label>
      </div>

      <!-- Footer Booking Bar -->
      <div class="book-bar">
        <div class="price-block">
          <div class="price">₹{{ displayPrice }}</div>
          <div class="price-sub">per person · all inclusive</div>
        </div>
        <div class="slots-block">
          <div class="slots-num">{{ trek.available_slots }}</div>
          <div class="slots-label">slots left</div>
        </div>
        <div style="text-align:right">
          <div style="color:rgba(255,255,255,.4);font-size:10px;margin-bottom:4px">{{ formatDate(trek.start_date) }} – {{ formatDate(trek.end_date) }}</div>
          <button class="book-btn" @click="book" :disabled="!trek.is_bookable || booking || !acceptPledge">
            {{ trek.is_bookable ? (booking ? 'Booking...' : 'Book this trek') : 'Not available' }}
          </button>
        </div>
      </div>
      <div v-if="bookMsg" class="alert alert-success" style="margin-top:12px">{{ bookMsg }}</div>
      <div v-if="bookErr" class="alert alert-error" style="margin-top:12px">{{ bookErr }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, computed, nextTick } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { treksAPI, userAPI } from '../api'
import { useAuthStore } from '../store/auth'
import { Chart, registerables } from 'chart.js'

Chart.register(...registerables)

const route = useRoute()
const router = useRouter()
const auth = useAuthStore()

const trek = ref(null)
const localFood = ref([])
const restaurants = ref([])
const agencies = ref([])
const selectedAgencyId = ref(null)
const booking = ref(false)
const bookMsg = ref('')
const bookErr = ref('')
const fallbackImg = 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=900&q=80&fit=crop'

const showCultureExplorer = ref(false)
const acceptPledge = ref(false)
const isItineraryOpen = ref(false)

// Reviews State
const reviews = ref([])
const myBooking = ref(null)
const submittingReview = ref(false)
const reviewErr = ref('')
const newReview = ref({ rating: '5', comment: '', trail_condition: 'Clear' })

let elevationChartInstance = null

const displayPrice = computed(() => {
  if (!trek.value) return 0
  if (!selectedAgencyId.value) return trek.value.price_inr
  const selected = agencies.value.find(a => a.id === selectedAgencyId.value)
  return selected ? selected.package_starting_price_inr : trek.value.price_inr
})

const selectedAgency = computed(() => {
  if (!selectedAgencyId.value) return null
  return agencies.value.find(a => a.id === selectedAgencyId.value)
})

function formatDate(d) {
  if (!d) return '-'
  return new Date(d).toLocaleDateString('en-IN', { day: '2-digit', month: 'short', year: 'numeric' })
}

// Day-by-day Itinerary parsing
const parsedItinerary = computed(() => {
  if (!trek.value || !trek.value.itinerary) return []
  return trek.value.itinerary.split('|').map(segment => {
    const parts = segment.split(':')
    return {
      day: parts[0] || '',
      title: parts[1] || '',
      dist: parts[2] || '',
      alt: parts[3] || ''
    }
  })
})

// Trek Highlights, Terrain, and Trail Type dynamic helpers
const trekHighlights = computed(() => {
  if (!trek.value) return []
  const name = trek.value.name.toLowerCase()
  if (name.includes('kedarnath')) {
    return [
      'Sacred darshan at one of the 12 Jyotirlingas',
      'Dramatic snow-capped peak panoramas of Kedarnath dome',
      'Enchanting crossing of Mandakini river pathways',
      'Pristine stone-paved pilgrimage trail'
    ]
  }
  if (name.includes('chadar')) {
    return [
      'Walking on frozen Zanskar river sheet (Chadar)',
      'Sub-zero winter glamping expeditions',
      'Towering frozen waterfalls and gorge canyon walls',
      'Interaction with isolated Zanskari village folks'
    ]
  }
  if (name.includes('flowers')) {
    return [
      'Stunning UNESCO World Heritage valley carpeted in endemic alpine blooms',
      'Picturesque sightings of Himalayan Monal and blue sheep',
      'Breathtaking streams and misty glacial waterfalls',
      'Pristine views of Trishul and Kamet snow massifs'
    ]
  }
  if (name.includes('hemkund')) {
    return [
      'Pilgrimage to the highest Gurudwara in the world (4,329m)',
      'Scenic reflections in the sacred glacial lake Hemkund',
      'Fields of rare Brahmakamal flowers en route',
      'Breathtaking views of Saptarishi peaks'
    ]
  }
  return [
    'Pristine alpine forests and deep ridge valleys',
    'Spectacular views of Himalayan snow peaks',
    'Charming campsites under starry mountain skies',
    'Rich exposure to regional traditional cultures'
  ]
})

const heritagePhotos = computed(() => {
  if (!trek.value || !trek.value.state) return []
  const name = (trek.value.name || '').toLowerCase()
  if (name.includes('kedarnath')) {
    return [
      { src: '/chorabari_lake.png', title: 'Pristine Chorabari Glacial Lake' },
      { src: '/bhairav_temple.png', title: 'Sacred Bhairavnath Temple Shrine' }
    ]
  }
  if (name.includes('kuari')) {
    return [
      { src: '/kuari_oak_forest.png', title: 'Oak & Rhododendron Forest en route' },
      { src: '/gorson_bugyal.jpg', title: 'Stunning Gorson Bugyal Meadows' },
      { src: '/harela_festival.jpg', title: 'Traditional Harela Green Festival' }
    ]
  }
  if (name.includes('hemkund')) {
    return [
      { src: '/laxman_temple.png', title: 'Sacred Lakshman Temple' },
      { src: '/hemkund_gurudwara.png', title: 'Hemkund Sahib Gurudwara Shrine' }
    ]
  }
  if (name.includes('hampta')) {
    return [
      { src: '/shea_goru.png', title: 'High-Altitude Shea Goru Campsite' },
      { src: '/chandra_tal.png', title: 'Scenic Chandra Tal Glacial Lake Crossing' },
      { src: '/ladarcha_festival.jpg', title: 'Traditional Ladarcha Summer Fair in Spiti' }
    ]
  }
  if (name.includes('chadar')) {
    return [
      { src: '/chadar_frozen_river.png', title: 'Walking on Frozen Zanskar River' },
      { src: '/chadar_campsite.png', title: 'Sub-Zero Wilderness Campsite' }
    ]
  }
  if (name.includes('dayara')) {
    return [
      { src: '/dayara.jpg', title: 'Expansive Alpine Meadows of Dayara Bugyal' },
      { src: '/gorson_bugyal.jpg', title: 'Stunning Slopes & Grasslands' },
      { src: '/harela_festival.jpg', title: 'Traditional Greenery and Harvest Festival' }
    ]
  }
  const state = trek.value.state.toLowerCase()
  if (state.includes('uttarakhand')) {
    return [
      { src: '/jhora_dance.png', title: 'Jhora Folk Dance Circle' },
      { src: '/choliya_dance.png', title: 'Choliya Sword Warrior Dance' }
    ]
  }
  if (state.includes('himachal')) {
    return [
      { src: '/pahadi_attire.png', title: 'Traditional Pahadi Costumes & Attire' }
    ]
  }
  return []
})

function getTrekTerrain(name) {
  if (!name) return 'Mountainous'
  const n = name.toLowerCase()
  if (n.includes('chadar')) return 'Frozen River Sheet / Ice Shelf'
  if (n.includes('flowers') || n.includes('valley')) return 'Alpine Meadow / Dirt Trail'
  if (n.includes('kedarnath') || n.includes('amarnath')) return 'Glacial Valley / Stone Paved Ridge'
  return 'Forest Trail / Boulder Crossing'
}

function getTrekTrailType(name) {
  if (!name) return 'Out and Back'
  const n = name.toLowerCase()
  if (n.includes('loop')) return 'Loop Trail'
  return 'Out & Back (Pilgrim / Traditional Route)'
}

function getHeritageVideoSrc(state, name) {
  const n = (name || '').toLowerCase()
  if (n.includes('dayara')) {
    return 'https://v1.pinimg.com/videos/mc/720p/91/5c/be/915cbe0c364378f8c851bd755cb8e402.mp4'
  }
  if (!state) return '/raulane-video.mp4'
  const s = state.toLowerCase()
  if (s.includes('ladakh')) return '/spitukgutor.mp4'
  if (s.includes('himachal')) return '/raulane-video.mp4'
  return '/hornbill.mp4'
}

function getHeritageVideoCaption(state, name) {
  const n = (name || '').toLowerCase()
  if (n.includes('dayara')) {
    return 'Snowy Scenic Vista and Winter Trail (Dayara Bugyal, Uttarakhand)'
  }
  if (!state) return 'Pahadi Folk Dance (Raulane Festival)'
  const s = state.toLowerCase()
  if (s.includes('ladakh')) return 'Sacred Buddhist Cham Mask Dance (Spituk Gutor, Ladakh)'
  if (s.includes('himachal')) return 'Traditional Pahadi Folk Dance (Raulane Festival, Himachal Pradesh)'
  return 'Tribal Heritage Dance (Hornbill Festival, Northeast India)'
}

async function fetchTrek() {
  const res = await treksAPI.get(route.params.id)
  trek.value = res.data.trek
  localFood.value = res.data.local_food
  restaurants.value = res.data.restaurants
  agencies.value = res.data.agencies

  await fetchReviewsAndEligibility()

  await nextTick()
  drawElevationChart()

  setTimeout(() => {
    isItineraryOpen.value = true
  }, 600)
}

async function fetchReviewsAndEligibility() {
  const revRes = await treksAPI.reviews(route.params.id)
  reviews.value = revRes.data.reviews

  if (auth.isLoggedIn && auth.isTrekker) {
    try {
      const bookingsRes = await userAPI.myBookings()
      const userBookings = bookingsRes.data.bookings || []
      
      const eligible = userBookings.find(b => 
        b.trek_id === trek.value.id && 
        b.status !== 'Cancelled' && 
        !reviews.value.some(r => r.booking_id === b.id)
      )
      myBooking.value = eligible || null
    } catch (e) {
      console.error("Error fetching bookings for review eligibility:", e)
    }
  }
}

async function submitReview() {
  if (!myBooking.value) return
  submittingReview.value = true
  reviewErr.value = ''
  try {
    await userAPI.submitReview(myBooking.value.id, {
      rating: parseInt(newReview.value.rating),
      comment: newReview.value.comment,
      trail_condition: newReview.value.trail_condition
    })
    newReview.value = { rating: '5', comment: '', trail_condition: 'Clear' }
    myBooking.value = null
    await fetchTrek()
  } catch (e) {
    reviewErr.value = e.response?.data?.error || 'Failed to submit review'
  } finally {
    submittingReview.value = false
  }
}

function drawElevationChart() {
  if (!trek.value || !trek.value.elevation_profile) return
  const ctx = document.getElementById('elevationChart')
  if (!ctx) return

  const coords = trek.value.elevation_profile.split(',').map(item => {
    const [dist, alt] = item.split(':')
    return { x: parseFloat(dist), y: parseFloat(alt) }
  })

  const existingChart = Chart.getChart(ctx)
  if (existingChart) {
    existingChart.destroy()
  }

  elevationChartInstance = new Chart(ctx, {
    type: 'line',
    data: {
      labels: coords.map(c => `${c.x} km`),
      datasets: [{
        label: 'Altitude (m)',
        data: coords.map(c => c.y),
        borderColor: '#E8A838',
        backgroundColor: 'rgba(232, 168, 56, 0.12)',
        borderWidth: 2,
        fill: true,
        tension: 0.3,
        pointRadius: 4,
        pointBackgroundColor: '#E8A838'
      }]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: {
        legend: { display: false }
      },
      scales: {
        y: {
          title: { display: true, text: 'Altitude (meters)', color: 'rgba(255,255,255,0.5)', font: { size: 10 } },
          ticks: { color: 'rgba(255,255,255,0.7)', font: { size: 9 } },
          grid: { color: 'rgba(255,255,255,0.06)' }
        },
        x: {
          title: { display: true, text: 'Distance (kilometers)', color: 'rgba(255,255,255,0.5)', font: { size: 10 } },
          ticks: { color: 'rgba(255,255,255,0.7)', font: { size: 9 } },
          grid: { color: 'rgba(255,255,255,0.06)' }
        }
      }
    }
  })
}

async function book() {
  if (!auth.isLoggedIn) { router.push('/login'); return }
  if (!auth.isTrekker) { bookErr.value = 'Only trekkers can book treks'; return }
  booking.value = true
  bookErr.value = ''
  try {
    await userAPI.bookTrek({
      trek_id: trek.value.id,
      travel_agency_id: selectedAgencyId.value
    })
    bookMsg.value = `Successfully booked ${trek.value.name}!`
    await fetchTrek()
  } catch (e) {
    bookErr.value = e.response?.data?.error || 'Booking failed'
  } finally {
    booking.value = false
  }
}

onMounted(fetchTrek)
</script>

<style scoped>
.detail-page { background: #060e08; min-height: 100vh; }
.hero { position: relative; height: 360px; overflow: hidden; }
.hero img { width: 100%; height: 100%; object-fit: cover; }
.hero-overlay { position: absolute; inset: 0; background: linear-gradient(0deg, rgba(8,18,12,.96) 0%, rgba(8,18,12,.4) 50%, rgba(8,18,12,.15) 100%); }
.hero-top { position: absolute; top: 0; left: 0; right: 0; padding: 18px 32px; display: flex; align-items: center; justify-content: space-between; z-index: 1; }
.logo-mark { display: flex; align-items: center; gap: 8px; text-decoration: none; }
.logo-symbol { width: 30px; height: 30px; border-radius: 8px; background: rgba(232,168,56,.15); border: 1px solid rgba(232,168,56,.3); display: flex; align-items: center; justify-content: center; color: #E8A838; font-size: 13px; }
.logo-text { color: #fff; font-size: 14px; font-weight: 500; }
.logo-text em { color: #E8A838; font-style: normal; }
.nav-right { display: flex; gap: 8px; }
.nav-btn { background: rgba(255,255,255,.12); border: 0.5px solid rgba(255,255,255,.2); color: #fff; font-size: 11px; padding: 6px 14px; border-radius: 20px; cursor: pointer; text-decoration: none; }
.nav-btn.primary { background: #E8A838; color: #1a0800; border-color: #E8A838; }
.hero-bottom { position: absolute; bottom: 0; left: 0; right: 0; padding: 24px 32px; z-index: 1; }
.cat-tags { display: flex; gap: 6px; margin-bottom: 12px; }
.tag { font-size: 10px; font-weight: 500; padding: 3px 10px; border-radius: 12px; background: rgba(150,190,255,.18); color: #96beff; border: 0.5px solid rgba(150,190,255,.25); }
.tag-permit { background: rgba(255,100,100,.18); color: #ff9090; border-color: rgba(255,100,100,.25); }
.hero-title { color: #fff; font-size: 30px; font-weight: 500; font-family: Georgia, serif; }
.hero-subtitle { color: rgba(255,255,255,.55); font-size: 13px; margin-top: 6px; }

.stat-strip { display: grid; grid-template-columns: repeat(5,1fr); background: rgba(8,18,12,.95); border-bottom: 0.5px solid rgba(255,255,255,.08); }
.stat-item { padding: 14px 12px; text-align: center; border-right: 0.5px solid rgba(255,255,255,.07); }
.stat-item:last-child { border-right: none; }
.stat-val { color: #fff; font-size: 14px; font-weight: 500; }
.stat-val.accent { color: #E8A838; }
.stat-key { color: rgba(255,255,255,.4); font-size: 9px; margin-top: 3px; text-transform: uppercase; letter-spacing: .05em; }

.body { max-width: 900px; margin: 0 auto; padding: 24px 32px 60px; }
.section { margin-bottom: 24px; }
.sec-head { font-size: 12px; font-weight: 500; color: rgba(255,255,255,.45); text-transform: uppercase; letter-spacing: .07em; margin-bottom: 12px; }
.dark-card { background: rgba(255,255,255,.04); border: 0.5px solid rgba(255,255,255,.09); border-radius: 12px; padding: 16px 18px; }
.myth-text { color: rgba(255,255,255,.75); font-size: 14px; line-height: 1.7; font-style: italic; border-left: 2px solid #E8A838; padding-left: 14px; }

/* Day-by-Day timeline */
.itinerary-timeline {
  position: relative;
  padding-left: 8px;
  margin-top: 18px;
}
.itinerary-node {
  display: flex;
  position: relative;
  margin-bottom: 24px;
}
.itinerary-node:last-child {
  margin-bottom: 0;
}
.node-left {
  width: 48px;
  flex-shrink: 0;
}
.node-day {
  font-size: 11px;
  font-weight: 600;
  text-transform: uppercase;
  color: var(--jatayu-gold);
  letter-spacing: 0.05em;
  background: rgba(232, 168, 56, 0.1);
  padding: 3px 6px;
  border-radius: 6px;
  text-align: center;
  border: 0.5px solid rgba(232, 168, 56, 0.2);
}
.node-connector {
  position: relative;
  width: 24px;
  display: flex;
  justify-content: center;
}
.node-dot {
  font-size: 10px;
  z-index: 2;
  background: #060e08;
  height: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
}
.node-line {
  position: absolute;
  top: 18px;
  bottom: -28px;
  width: 1px;
  background: rgba(232, 168, 56, 0.25);
  z-index: 1;
}
.node-content {
  flex-grow: 1;
  background: rgba(255, 255, 255, 0.02);
  border: 0.5px solid rgba(255, 255, 255, 0.05);
  border-radius: 10px;
  padding: 12px 16px;
  margin-left: 8px;
}
.node-title {
  color: #fff;
  font-size: 13.5px;
  font-weight: 500;
}
.node-details {
  display: flex;
  gap: 8px;
  margin-top: 8px;
}
.node-pill {
  font-size: 10px;
  padding: 2px 8px;
  background: rgba(255,255,255,0.05);
  border-radius: 4px;
  color: rgba(255,255,255,0.6);
}

/* Mythology Section */
.mythology-section {
  margin: 32px 0;
}
.sec-head.--mythology {
  display: flex;
  align-items: center;
  gap: 8px;
  color: var(--jatayu-gold);
  font-weight: 600;
  font-family: Georgia, serif;
}
.mythology-card {
  position: relative;
  background: linear-gradient(145deg, #0e1e12, #070e0a);
  border: 1px solid rgba(232, 168, 56, 0.25);
  box-shadow: 0 0 15px rgba(232, 168, 56, 0.08);
  border-radius: 14px;
  padding: 24px;
  overflow: hidden;
}
.mythology-card .card-glow {
  position: absolute;
  top: -40px;
  right: -40px;
  width: 100px;
  height: 100px;
  background: radial-gradient(circle, rgba(232, 168, 56, 0.12) 0%, transparent 70%);
  pointer-events: none;
}
.mythology-card .myth-text {
  font-size: 14.5px;
  line-height: 1.75;
  color: rgba(255, 255, 255, 0.85);
  font-style: normal;
  border-left: none;
  padding-left: 0;
}

/* Elevation profile chart */
.elevation-chart-card {
  background: rgba(255, 255, 255, 0.03);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
  margin-top: 10px;
}
.chart-container-wrapper {
  height: 180px;
  position: relative;
}

/* Culture Hub Explorer */
.culture-explorer-panel {
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(232, 168, 56, 0.25);
  border-radius: 14px;
  padding: 20px;
  margin: 30px 0;
}
.explorer-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}
.banner-content h4 {
  font-size: 15px;
  color: #fff;
  font-family: Georgia, serif;
  margin-bottom: 4px;
}
.banner-content p {
  font-size: 11.5px;
  color: rgba(255,255,255,0.5);
}
.btn-toggle-culture {
  background: rgba(232, 168, 56, 0.15);
  border: 1.5px solid rgba(232, 168, 56, 0.4);
  color: #E8A838;
  font-size: 11.5px;
  padding: 8px 18px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s ease;
}
.btn-toggle-culture:hover {
  background: rgba(232, 168, 56, 0.25);
  box-shadow: 0 0 10px rgba(232, 168, 56, 0.2);
}
.explorer-tab-content {
  border-top: 0.5px solid rgba(255,255,255,0.08);
  padding-top: 20px;
  animation: fadeIn 0.3s ease-out;
}
.sub-culture-section .sub-section-title {
  font-size: 12.5px;
  color: #E8A838;
  font-weight: 600;
  margin-bottom: 12px;
  font-family: Georgia, serif;
}
.no-data-text {
  color: rgba(255,255,255,0.3);
  font-size: 11.5px;
}
.culture-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.cult-item { background: rgba(255,255,255,.04); border: 0.5px solid rgba(255,255,255,.08); border-radius: 10px; padding: 14px; }
.cult-label { font-size: 10px; color: rgba(255,255,255,.4); text-transform: uppercase; letter-spacing: .05em; margin-bottom: 4px; }
.cult-val { font-size: 13px; color: rgba(255,255,255,.8); }
.cult-reel-inline-link {
  display: inline-block;
  font-size: 11px;
  font-weight: 600;
  color: #E8A838;
  text-decoration: none;
  margin-left: 8px;
  transition: opacity 0.2s ease;
}
.cult-reel-inline-link:hover {
  text-decoration: underline;
  opacity: 0.9;
}
.cult-reel-link {
  display: inline-block;
  margin-top: 8px;
  font-size: 11.5px;
  font-weight: 600;
  color: #E8A838;
  text-decoration: none;
  padding: 4px 10px;
  background: rgba(232, 168, 56, 0.1);
  border: 1px solid rgba(232, 168, 56, 0.25);
  border-radius: 6px;
  transition: all 0.2s ease;
}
.cult-reel-link:hover {
  background: rgba(232, 168, 56, 0.2);
  box-shadow: 0 0 8px rgba(232, 168, 56, 0.2);
}

.food-scroll { display: grid; grid-template-columns: repeat(2, 1fr); gap: 12px; }
@media (max-width: 600px) { .food-scroll { grid-template-columns: 1fr; } }
.food-card { border-radius: 10px; overflow: hidden; background: rgba(255,255,255,.04); border: 0.5px solid rgba(255,255,255,.08); display: flex; flex-direction: row; min-height: 100px; }
.food-img { width: 100px; min-height: 100px; object-fit: cover; flex-shrink: 0; }
.food-img-placeholder { width: 100px; min-height: 100px; display: flex; align-items: center; justify-content: center; font-size: 12px; color: rgba(255,255,255,.3); background: rgba(255,255,255,.03); flex-shrink: 0; }
.food-body { padding: 10px 12px; }
.food-name { color: #fff; font-size: 12px; font-weight: 500; }
.food-desc { color: rgba(255,255,255,.45); font-size: 10px; margin-top: 4px; line-height: 1.4; }
.food-tag { display: inline-block; margin-top: 6px; font-size: 9px; padding: 2px 7px; border-radius: 8px; background: rgba(232,168,56,.15); color: #E8A838; }

.partner-grid { display: grid; grid-template-columns: repeat(2,1fr); gap: 10px; }
.partner-card { background: rgba(255,255,255,.04); border: 0.5px solid rgba(255,255,255,.08); border-radius: 10px; padding: 14px; }
.partner-name { color: #fff; font-size: 13px; font-weight: 500; }
.verified { color: #50d28c; }
.partner-meta { color: rgba(255,255,255,.4); font-size: 11px; margin-top: 4px; }
.partner-desc { color: rgba(255,255,255,.6); font-size: 11px; margin-top: 6px; }

/* Partner Selector & Dossier Card */
.partner-selector-card {
  background: rgba(255, 255, 255, 0.02);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
}
.selector-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.selector-title {
  color: #fff;
  font-weight: 600;
  font-size: 14px;
}
.selector-help-text {
  color: rgba(255,255,255,0.5);
  font-size: 11.5px;
  margin-bottom: 12px;
}
.partner-select {
  background: #0f1c12;
  border: 1px solid rgba(255,255,255,0.15);
  color: #fff;
  padding: 10px;
  border-radius: 6px;
  font-size: 12.5px;
  outline: none;
  width: 100%;
}
.selected-partner-card {
  background: linear-gradient(135deg, rgba(232, 168, 56, 0.06), rgba(8, 18, 12, 0.95));
  border: 1.5px solid rgba(232, 168, 56, 0.25);
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 4px 15px rgba(0,0,0,0.3);
}
.partner-card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  border-bottom: 0.5px solid rgba(232, 168, 56, 0.15);
  padding-bottom: 10px;
  margin-bottom: 12px;
}
.partner-card-header h4 {
  font-size: 14px;
  color: #fff;
  font-family: Georgia, serif;
}
.badge-status {
  font-size: 9px;
  font-weight: 600;
  padding: 3px 8px;
  border-radius: 4px;
}
.badge-approved {
  background: rgba(80, 210, 140, 0.15);
  color: #50d28c;
  border: 0.5px solid rgba(80, 210, 140, 0.3);
}
.partner-card-body {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.partner-info-row {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
}
.partner-info-row span {
  color: rgba(255,255,255,0.45);
}
.partner-info-row b {
  color: rgba(255,255,255,0.9);
}
.partner-services-list {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
}
.meta-pill {
  font-size: 9px;
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.7);
  padding: 3px 8px;
  border-radius: 4px;
  text-transform: capitalize;
  border: 0.5px solid rgba(255,255,255,0.1);
}

/* Pledge Card */
.pledge-card {
  background: linear-gradient(135deg, rgba(30, 77, 50, 0.2), rgba(6, 14, 8, 0.95));
  border: 1px solid rgba(80, 210, 140, 0.2);
  border-radius: 14px;
  padding: 20px 24px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.25);
}
.pledge-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}
.pledge-icon {
  font-size: 18px;
}
.pledge-title {
  color: #50d28c;
  font-weight: 600;
  font-size: 15px;
  font-family: Georgia, serif;
}
.pledge-checkbox-label {
  display: flex;
  gap: 12px;
  cursor: pointer;
  align-items: flex-start;
}
.pledge-checkbox {
  accent-color: #50d28c;
  margin-top: 4px;
  width: 16px;
  height: 16px;
  cursor: pointer;
}
.pledge-text {
  font-size: 13px;
  line-height: 1.5;
  color: rgba(255, 255, 255, 0.8);
}

/* Reviews */
.review-form-card {
  background: rgba(255, 255, 255, 0.02);
  border: 0.5px solid rgba(255, 255, 255, 0.08);
  border-radius: 12px;
  padding: 20px;
}
.form-title { color: #fff; font-size: 14px; font-weight: 600; }
.form-help { color: rgba(255,255,255,0.5); font-size: 11px; margin-bottom: 12px; }
.form-row { display: grid; grid-template-columns: 1fr 1fr; gap: 10px; }
.form-group { display: flex; flex-direction: column; gap: 4px; }
.form-label { font-size: 10px; color: rgba(255,255,255,0.4); text-transform: uppercase; }
.form-input {
  background: #0f1c12;
  border: 1px solid rgba(255,255,255,0.15);
  color: #fff;
  padding: 8px 10px;
  border-radius: 6px;
  font-size: 12px;
  outline: none;
}
.text-area { height: 60px; resize: none; font-family: inherit; }
.submit-review-btn { background: #50d28c; color: #060e08; border: none; font-size: 12px; font-weight: 600; padding: 10px 20px; border-radius: 6px; cursor: pointer; }
.submit-review-btn:disabled { opacity: 0.5; }
.reviews-list { display: flex; flex-direction: column; gap: 12px; }
.review-card { background: rgba(255, 255, 255, 0.03); border: 0.5px solid rgba(255, 255, 255, 0.08); border-radius: 12px; padding: 16px; }
.review-header { display: flex; justify-content: space-between; align-items: center; margin-bottom: 8px; }
.stars-display { color: #E8A838; letter-spacing: 2px; font-size: 13px; }
.reviewer-name { color: #fff; font-size: 12px; font-weight: 500; margin-left: 10px; }
.condition-badge { font-size: 9px; font-weight: 500; padding: 3px 8px; border-radius: 10px; }
.condition-clear { background: rgba(232, 168, 56, 0.15); color: #E8A838; border: 0.5px solid rgba(232, 168, 56, 0.25); }
.condition-snowy { background: rgba(90, 200, 250, 0.15); color: #5ac8fa; border: 0.5px solid rgba(90, 200, 250, 0.25); }
.condition-muddy { background: rgba(255, 100, 100, 0.15); color: #ff9090; border: 0.5px solid rgba(255, 100, 100, 0.25); }
.condition-rocky { background: rgba(189, 195, 199, 0.15); color: #bdc3c7; border: 0.5px solid rgba(189, 195, 199, 0.25); }
.condition-overgrown { background: rgba(80, 210, 140, 0.15); color: #50d28c; border: 0.5px solid rgba(80, 210, 140, 0.25); }
.review-comment { color: rgba(255, 255, 255, 0.85); font-size: 13px; line-height: 1.5; margin-bottom: 6px; }
.review-date { color: rgba(255, 255, 255, 0.35); font-size: 10px; }

/* Book bar */
.book-bar { background: rgba(8,18,12,.98); border: 0.5px solid rgba(232,168,56,.25); border-radius: 12px; padding: 18px 20px; display: flex; align-items: center; justify-content: space-between; margin-top: 28px; }
.price { color: #E8A838; font-size: 22px; font-weight: 500; }
.price-sub { color: rgba(255,255,255,.4); font-size: 10px; }
.slots-num { color: #fff; font-size: 18px; font-weight: 500; text-align: center; }
.slots-label { color: rgba(255,255,255,.4); font-size: 10px; text-align: center; }
.book-btn { background: #E8A838; border: none; color: #1a0800; font-size: 13px; font-weight: 500; padding: 11px 26px; border-radius: 10px; cursor: pointer; }
.book-btn:disabled { opacity: .5; cursor: not-allowed; }

/* Left Itinerary Drawer CSS */
.left-itinerary-drawer {
  position: fixed;
  top: 0;
  left: -380px; /* Hidden by default */
  width: 380px;
  height: 100vh;
  background: linear-gradient(180deg, #09150c 0%, #050b06 100%);
  border-right: 1px solid rgba(232, 168, 56, 0.25);
  box-shadow: 10px 0 25px rgba(0, 0, 0, 0.6);
  z-index: 1000;
  transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1), left 0.4s cubic-bezier(0.16, 1, 0.3, 1);
  display: flex;
  flex-direction: column;
}

.left-itinerary-drawer.drawer-open {
  transform: translateX(380px); /* Slide out into view */
}

/* Handle Tab sticking out of the drawer */
.drawer-handle-tab {
  position: absolute;
  top: 50%;
  right: -36px; /* Stick out on the right boundary of the drawer */
  transform: translateY(-50%);
  background: linear-gradient(135deg, #e8a838, #c78d28);
  border: 1px solid rgba(232, 168, 56, 0.4);
  border-left: none;
  color: #1a0800;
  border-radius: 0 10px 10px 0;
  padding: 18px 8px;
  cursor: pointer;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  box-shadow: 4px 0 15px rgba(232, 168, 56, 0.3);
  z-index: 1001;
  transition: all 0.2s ease;
}

.drawer-handle-tab:hover {
  box-shadow: 6px 0 20px rgba(232, 168, 56, 0.5);
  filter: brightness(1.1);
}

.drawer-handle-tab .handle-icon {
  font-size: 14px;
}

.drawer-handle-tab .handle-text {
  writing-mode: vertical-rl;
  text-orientation: mixed;
  font-size: 11px;
  font-weight: 700;
  letter-spacing: 0.1em;
}

.drawer-handle-tab .handle-arrow {
  font-size: 8px;
  margin-top: 4px;
}

/* Drawer contents */
.drawer-inner {
  height: 100%;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.drawer-header {
  padding: 20px 24px;
  border-bottom: 1.5px solid rgba(232, 168, 56, 0.15);
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.drawer-header-title {
  color: #fff;
  font-size: 16px;
  font-weight: 600;
  font-family: Georgia, serif;
  letter-spacing: 0.02em;
}

.drawer-close-btn {
  background: transparent;
  border: none;
  color: rgba(255, 255, 255, 0.4);
  font-size: 18px;
  cursor: pointer;
  transition: color 0.2s;
}

.drawer-close-btn:hover {
  color: #fff;
}

.drawer-body {
  flex-grow: 1;
  overflow-y: auto;
  padding: 24px;
}

.drawer-body::-webkit-scrollbar {
  width: 5px;
}

.drawer-body::-webkit-scrollbar-track {
  background: transparent;
}

.drawer-body::-webkit-scrollbar-thumb {
  background: rgba(232, 168, 56, 0.3);
  border-radius: 4px;
}

.drawer-body::-webkit-scrollbar-thumb:hover {
  background: rgba(232, 168, 56, 0.5);
}

/* Safety Marquee Ticker Band */
.safety-marquee-band {
  background: linear-gradient(90deg, #1f0b08, #2a0f0a);
  border-top: 1px solid rgba(255, 100, 100, 0.25);
  border-bottom: 1px solid rgba(255, 100, 100, 0.25);
  padding: 10px 0;
  overflow: hidden;
  position: relative;
  z-index: 5;
  width: 100%;
}
.safety-marquee-band .marquee-content {
  display: flex;
  white-space: nowrap;
  gap: 30px;
  animation: safetyMarqueeScroll 35s linear infinite;
}
.safety-marquee-band .ticker-text {
  font-family: 'Outfit', sans-serif;
  font-size: 11px;
  font-weight: 600;
  color: #ff9090;
  letter-spacing: 0.05em;
  text-transform: uppercase;
}
@keyframes safetyMarqueeScroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* Emojiless Timeline Dot */
.node-dot .dot-inner {
  display: block;
  width: 8px;
  height: 8px;
  background: #E8A838;
  border-radius: 50%;
  box-shadow: 0 0 8px #E8A838;
}

/* Extended specs & Highlights section */
.trek-extended-details {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 20px;
}
.specs-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 10px;
}
@media (max-width: 900px) {
  .specs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (max-width: 480px) {
  .specs-grid {
    grid-template-columns: 1fr;
  }
}
.spec-card {
  background: rgba(255, 255, 255, 0.03);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  padding: 10px 12px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.spec-icon {
  font-size: 18px;
}
.spec-label {
  font-size: 9px;
  color: rgba(255, 255, 255, 0.4);
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.spec-val {
  font-size: 11.5px;
  font-weight: 500;
  color: #fff;
  margin-top: 2px;
}

/* Trail Highlights list styling */
.highlights-section {
  background: rgba(232, 168, 56, 0.03);
  border: 1px solid rgba(232, 168, 56, 0.12);
  border-radius: 12px;
  padding: 18px 20px;
}
.highlights-title {
  color: #E8A838;
  font-size: 13.5px;
  font-weight: 600;
  margin-bottom: 12px;
  font-family: Georgia, serif;
}
.highlights-list {
  list-style: none;
  padding: 0;
  margin: 0;
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 12px 24px;
}
@media (max-width: 600px) {
  .highlights-list {
    grid-template-columns: 1fr;
    gap: 8px;
  }
}
.highlights-list li {
  font-size: 12.5px;
  color: rgba(255, 255, 255, 0.85);
  display: flex;
  align-items: flex-start;
  gap: 8px;
  line-height: 1.5;
}
.hl-marker {
  color: #E8A838;
  font-size: 9px;
  margin-top: 3px;
}

/* Review placeholder card styling */
.review-placeholder-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px dashed rgba(255, 255, 255, 0.12);
  border-radius: 12px;
  padding: 16px 20px;
  display: flex;
  align-items: center;
  gap: 16px;
}
.placeholder-icon {
  font-size: 20px;
  background: rgba(232, 168, 56, 0.08);
  width: 42px;
  height: 42px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #E8A838;
  border: 1px solid rgba(232, 168, 56, 0.2);
  flex-shrink: 0;
}
.placeholder-text-content {
  flex-grow: 1;
}
.placeholder-title {
  color: #fff;
  font-size: 13.5px;
  font-weight: 600;
  margin-bottom: 4px;
}
.placeholder-desc {
  color: rgba(255, 255, 255, 0.45);
  font-size: 11.5px;
  line-height: 1.45;
}
.placeholder-desc code {
  background: rgba(255, 255, 255, 0.08);
  padding: 1.5px 5px;
  border-radius: 4px;
  color: #E8A838;
  font-family: monospace;
  font-size: 11px;
}

/* Heritage Gallery */
.heritage-gallery-carousel {
  display: flex;
  overflow-x: auto;
  gap: 16px;
  scroll-snap-type: x mandatory;
  padding-bottom: 8px;
}
.heritage-gallery-carousel::-webkit-scrollbar {
  height: 6px;
}
.heritage-gallery-carousel::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.02);
  border-radius: 4px;
}
.heritage-gallery-carousel::-webkit-scrollbar-thumb {
  background: rgba(232, 168, 56, 0.2);
  border-radius: 4px;
}
.heritage-carousel-item {
  flex: 0 0 240px;
  scroll-snap-align: start;
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-radius: 10px;
  overflow: hidden;
  box-shadow: 0 4px 10px rgba(0,0,0,0.3);
  transition: transform 0.3s ease, border-color 0.3s ease;
}
.heritage-carousel-item:hover {
  transform: translateY(-3px);
  border-color: rgba(232, 168, 56, 0.3);
}
.heritage-carousel-item img {
  width: 100%;
  height: 150px;
  object-fit: cover;
  display: block;
}
.gallery-caption {
  background: rgba(10, 10, 10, 0.85);
  padding: 8px 10px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.7);
  text-align: center;
  border-top: 1px solid rgba(255, 255, 255, 0.06);
}

/* Video / Multimedia Trail styling */
.culture-video-section {
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 20px;
}
.video-container {
  background: #000;
  border: 1.5px solid rgba(232, 168, 56, 0.15);
  border-radius: 12px;
  overflow: hidden;
  box-shadow: 0 4px 15px rgba(0,0,0,0.5);
  max-width: 560px;
  margin: 0 auto;
}
.heritage-video {
  width: 100%;
  height: 280px;
  display: block;
}
.video-caption {
  background: rgba(20, 20, 20, 0.95);
  padding: 8px 12px;
  font-size: 11px;
  color: rgba(255, 255, 255, 0.5);
  text-align: center;
  border-top: 1.5px solid rgba(232, 168, 56, 0.15);
}

/* West Bengal & Sikkim side-by-side vertical video layout */
.wb-videos-grid {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
  max-width: 640px;
  margin: 16px auto 0;
}
.wb-videos-grid .video-container {
  max-width: 100%;
  aspect-ratio: 9 / 16;
  display: flex;
  flex-direction: column;
  height: 480px;
}
.wb-videos-grid .heritage-video {
  width: 100%;
  flex-grow: 1;
  height: calc(100% - 36px);
  object-fit: cover;
}
.wb-videos-grid .video-caption {
  flex-shrink: 0;
  height: 36px;
  display: flex;
  align-items: center;
  justify-content: center;
}
@media (max-width: 600px) {
  .wb-videos-grid {
    grid-template-columns: 1fr;
    max-width: 300px;
  }
}

/* Instagram Reel Callout Card styles */
.instagram-reel-card {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(232, 168, 56, 0.2);
  border-radius: 12px;
  padding: 16px 20px;
  box-shadow: 0 4px 12px rgba(0,0,0,0.4);
  max-width: 560px;
  margin: 16px auto 0;
  text-align: left;
}
.reel-details {
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.reel-title {
  color: #fff;
  font-size: 13.5px;
  font-weight: 600;
}
.reel-desc {
  color: rgba(255, 255, 255, 0.5);
  font-size: 11.5px;
  line-height: 1.4;
}
.btn-watch-reel {
  display: inline-block;
  align-self: flex-start;
  background: #E8A838;
  border: none;
  color: #1a0800;
  font-size: 11px;
  font-weight: 600;
  padding: 6px 12px;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  margin-top: 6px;
  transition: all 0.2s ease;
}
.btn-watch-reel:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 10px rgba(232, 168, 56, 0.3);
}

/* Eatery phone and call action button styling */
.eatery-contact-info {
  background: rgba(255, 255, 255, 0.02);
  border-top: 1px solid rgba(255, 255, 255, 0.06);
  padding-top: 12px;
}
.contact-row {
  font-size: 11px;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 4px;
}
.contact-row b {
  color: rgba(255, 255, 255, 0.85);
  font-weight: 500;
}
.btn-call-eatery {
  display: inline-block;
  background: #E8A838;
  border: none;
  color: #1a0800;
  font-size: 11.5px;
  font-weight: 600;
  padding: 6px 14px;
  border-radius: 6px;
  cursor: pointer;
  text-decoration: none;
  text-align: center;
  transition: all 0.2s ease;
}
.btn-call-eatery:hover {
  filter: brightness(1.1);
  box-shadow: 0 0 10px rgba(232, 168, 56, 0.2);
}

@keyframes fadeIn {
  from { opacity: 0; transform: translateY(5px); }
  to { opacity: 1; transform: translateY(0); }
}
</style>
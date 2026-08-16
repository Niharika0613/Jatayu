<template>
  <div class="home-page">

    <!-- ═══════════════════════════════════════════════════
         HERO — Cinematic Mountain Video Experience
    ════════════════════════════════════════════════════════ -->
    <section class="hero" ref="heroSection">
      <div class="hero-video-layer">
        <video autoplay loop muted playsinline class="hero-video">
          <source src="/hero-video.mp4" type="video/mp4" />
          <img src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1800&q=85&fit=crop" alt="Himalayas at Sunset" class="hero-img-fallback" />
        </video>
      </div>

      <div class="hero-overlay"></div>
      <div class="hero-vignette"></div>

      <!-- ── NAVBAR ─────────────────────────────────────── -->
      <nav class="hero-nav">
        <div class="nav-brand" style="display:flex;align-items:center;gap:10px">
          <img src="/logo-transparent.png" alt="Jatayu Logo" style="width:36px;height:auto;flex-shrink:0" />
          <div>
            <div class="nav-brand__name">Jata<em>yu</em></div>
            <div class="nav-brand__sub">India's Trekking Soul</div>
          </div>
        </div>
        <div class="nav-links">
          <router-link to="/treks" class="nav-link">Explore Treks</router-link>
          <router-link to="/treks?category=Snow" class="nav-link">Snow Yatras</router-link>
          <router-link to="/treks?category=Pilgrimage" class="nav-link">Pilgrimages</router-link>
        </div>
        <div class="nav-actions">
          <template v-if="auth.isLoggedIn">
            <router-link
              :to="auth.isAdmin ? '/admin' : auth.isStaff ? '/staff' : '/dashboard'"
              class="nav-btn nav-btn--gold"
            >My Dashboard ↗</router-link>
          </template>
          <template v-else>
            <router-link to="/login" class="nav-btn nav-btn--ghost">Sign in</router-link>
            <router-link to="/register" class="nav-btn nav-btn--gold">Begin Yatra</router-link>
          </template>
        </div>
      </nav>

      <!-- ── HERO HEADLINE ──────────────────────────────── -->
      <div class="hero-headline-wrap" ref="headlineWrap">
        <div class="hero-eyebrow" ref="eyebrowEl">UTTARAKHAND · HIMACHAL · SIKKIM · LADAKH</div>
        <h1 class="hero-headline" ref="headlineEl">
          Where Peaks<br>Touch the <em>Sky</em>
        </h1>
        <p class="hero-subline" ref="sublineEl">
          Singular voyages to sacred summits, shaped for those<br>
          who seek beauty beyond the ordinary and the known.
        </p>
        <div class="hero-ctas" ref="ctasEl">
          <a href="#featured-treks" class="hero-cta hero-cta--fill" @click.prevent="scrollTo('#featured-treks')">
            Discover Treks
            <svg width="14" height="14" viewBox="0 0 16 16" fill="none">
              <path d="M3 8h10M9 4l4 4-4 4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round"/>
            </svg>
          </a>
          <router-link to="/register" class="hero-cta hero-cta--outline">Start Free</router-link>
        </div>
      </div>

      <!-- Scroll Indicator -->
      <div class="scroll-hint" ref="scrollHint">
        <div class="scroll-hint__dot"></div>
        <div class="scroll-hint__line"></div>
        <span>Scroll Down</span>
      </div>
    </section>

    <!-- ─── SACRED SCROLLING STRIP (TRANSITION BAND) ─── -->
    <div class="sacred-marquee-band">
      <div class="marquee-content">
        <span>✦ SACRED TRAILS</span>
        <span>✦ TRADITIONAL YATRAS</span>
        <span>✦ MYSTICAL PEAKS</span>
        <span>✦ SOUL JOURNEYS</span>
        <span>✦ ANCIENT SHRINES</span>
        <span>✦ RITUCHAKRA PASSES</span>
        <span>✦ KEDARNATH DHAM</span>
        <span>✦ AMARNATH EXPEDITION</span>
        <span>✦ HORNBILL WARRIORS</span>
        <span>✦ RAULANE FAIR</span>
        
        <span>✦ SACRED TRAILS</span>
        <span>✦ TRADITIONAL YATRAS</span>
        <span>✦ MYSTICAL PEAKS</span>
        <span>✦ SOUL JOURNEYS</span>
        <span>✦ ANCIENT SHRINES</span>
        <span>✦ RITUCHAKRA PASSES</span>
        <span>✦ KEDARNATH DHAM</span>
        <span>✦ AMARNATH EXPEDITION</span>
        <span>✦ HORNBILL WARRIORS</span>
        <span>✦ RAULANE FAIR</span>
      </div>
    </div>

    <!-- ═══════════════════════════════════════════════════
         FEATURED TREKS CAROUSEL (Gold Traditional Style)
    ════════════════════════════════════════════════════════ -->
    <section id="featured-treks" class="treks-section scroll-fade">
      <div class="sec-header --center">
        <span class="sec-overline">Handpicked Expeditions</span>
        <h2 class="sec-title">Sacred Journeys & Featured Yatras</h2>
        <div class="divider-line --center"></div>
      </div>

      <div class="carousel-container">
        <button class="carousel-control prev" @click="scrollCarousel(-1)">←</button>
        <div class="carousel-track-snap" ref="carouselTrack">
          <div
            v-for="t in displayTreks"
            :key="t.id"
            class="trek-card-gold snap-slide"
            @click="$router.push(`/treks/${t.id}`)"
          >
            <div class="trek-card-gold__img-wrap">
              <img :src="t.cover_image || fallback" :alt="t.name" />
              <div class="trek-card-gold__price-tag">₹{{ t.price_inr?.toLocaleString('en-IN') }}</div>
              <div class="trek-card-gold__badge">{{ t.category }}</div>
            </div>
            <div class="trek-card-gold__body">
              <div class="trek-card-gold__rating">
                <span class="rating-star">⭐</span> {{ t.avg_rating || '4.8' }} <span class="rating-count">({{ t.total_reviews || '24' }} Reviews)</span>
              </div>
              <h3 class="trek-card-gold__title">{{ t.name }}</h3>
              <p class="trek-card-gold__loc">📍 {{ t.location }}</p>
              <div class="trek-card-gold__meta">
                <span>⏱ {{ t.duration_days }} Days</span>
                <span>🏔 {{ t.max_altitude_m || '3,800' }}m</span>
                <span :class="`difficulty-pill --${t.difficulty?.toLowerCase()}`">{{ t.difficulty }}</span>
              </div>
            </div>
          </div>
        </div>
        <button class="carousel-control next" @click="scrollCarousel(1)">→</button>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════
         RITUCHAKRA (Interactive Seasonal Wheel Engine)
    ════════════════════════════════════════════════════════ -->
    <section class="rituchakra-section scroll-fade">
      <div class="sec-header --center">
        <span class="sec-overline">Cosmic Mountain Rhythms</span>
        <h2 class="sec-title">ऋतुचक्र (Rituchakra Season Picker)</h2>
        <p class="sec-subtitle">Choose your spiritual trail based on the ancient Indian seasons and weather conditions.</p>
        <div class="divider-line --center"></div>
      </div>

      <div class="season-picker-wrap">
        <!-- Rituchakra Rotating Dial (Left Side) -->
        <div class="rituchakra-wheel-container">
          <div class="wheel-pointer">🪔</div>
          <div class="rituchakra-wheel" :style="{ transform: `rotate(-${wheelRotation}deg)` }">
            <div 
              v-for="(s, idx) in seasons" 
              :key="s.id" 
              :class="['wheel-slice', { active: activeSeason === s.id }]"
              :style="{ transform: `rotate(${idx * 72}deg) translateY(-110px) rotate(${wheelRotation - idx * 72}deg) ${activeSeason === s.id ? 'scale(1.15)' : 'scale(1)'}` }"
              @click="selectSeason(s.id, idx)"
            >
              <span class="slice-icon">{{ s.icon }}</span>
              <span class="slice-name">{{ s.id }}</span>
            </div>
            <div class="wheel-center" :style="{ transform: `rotate(${wheelRotation}deg)` }">
              <div class="wheel-center-inner">
                <span class="center-season-icon">{{ seasons.find(s => s.id === activeSeason).icon }}</span>
                <span class="center-season-lbl">{{ activeSeason }}</span>
              </div>
            </div>
          </div>
        </div>

        <!-- Details & Stretchy list (Right Side) -->
        <div class="season-details-panel">
          <div class="season-meta">
            <h3>{{ seasons.find(s => s.id === activeSeason).fullName }}</h3>
            <p class="season-desc">{{ seasons.find(s => s.id === activeSeason).desc }}</p>
            <div class="weather-alert">
              <span class="alert-icon">🌤</span>
              <span><strong>Optimal Trail Conditions:</strong> {{ seasons.find(s => s.id === activeSeason).safety }}</span>
            </div>
          </div>

          <div class="seasonal-list-container">
            <div class="seasonal-grid" v-if="filteredTreks.length" ref="seasonalGridEl">
              <div
                v-for="t in filteredTreks.slice(0, 3)"
                :key="t.id"
                class="seasonal-compact-card"
                @click="$router.push(`/treks/${t.id}`)"
              >
                <div class="seasonal-compact-img">
                  <img :src="t.cover_image || fallback" :alt="t.name" />
                </div>
                <div class="seasonal-compact-body">
                  <h4>{{ t.name }}</h4>
                  <p>{{ t.location }} · {{ t.duration_days }}d · ₹{{ t.price_inr?.toLocaleString('en-IN') }}</p>
                  <span class="seasonal-compact-tag">Recommended</span>
                </div>
              </div>
            </div>
            <div class="seasonal-empty" v-else>
              <span class="empty-icon">🪔</span>
              <p>Iss season ke liye treks ki booking jald hi shuru hogi. Tab tak hamare anya active seasons ko explore karein.</p>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════
         DEVBHUMI GATHA (Sacred Mythological Trails)
    ════════════════════════════════════════════════════════ -->
    <section class="gatha-section scroll-fade">
      <div class="sec-header --center">
        <span class="sec-overline">Chronicles of Sacred Paths</span>
        <h2 class="sec-title">देवभूमि गाथा (Mythological Trails)</h2>
        <p class="sec-subtitle">Indian mountains are not just rocks, they are pure divinity. Walk the pathways walked by gods.</p>
        <div class="divider-line --center"></div>
      </div>

      <div class="gatha-scroll-container">
        <div class="gatha-row">
          <div
            v-for="t in mythologicalTreks"
            :key="t.name"
            class="gatha-card"
          >
            <div class="gatha-card__bg-icon">◈</div>
            <div class="gatha-card__header">
              <span class="gatha-card__tag">{{ getGathaTag(t.name) }}</span>
              <span class="gatha-card__shloka">{{ getGathaShloka(t.name) }}</span>
            </div>
            <h3 class="gatha-card__title">{{ t.name }}</h3>
            <p class="gatha-card__text">"{{ t.mythological_significance }}"</p>
            <div class="gatha-card__footer">
              <span>📍 {{ t.location }}</span>
              <router-link v-if="t.id" :to="`/treks/${t.id}`" class="gatha-card__link">Yatra Details ↗</router-link>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════
         UTSAV OF THE PEAKS (Mountain Festivals & Sacred Fairs)
    ════════════════════════════════════════════════════════ -->
    <section class="festivals-section scroll-fade">
      <div class="sec-header --center">
        <span class="sec-overline">Mountain Heritage</span>
        <h2 class="sec-title">Utsav of the Peaks</h2>
        <p class="sec-subtitle">Discover the sacred local festivals and ancient spiritual fairs celebrated across our trekking regions.</p>
        <div class="divider-line --center"></div>
      </div>

      <div class="festivals-container">
        <!-- Left Column: Video/Image Card -->
        <div class="festival-display-card">
          <div class="festival-media-wrapper">
            <template v-if="mountainFestivals[activeFestivalIndex].video">
              <video autoplay loop muted playsinline class="festival-video" :key="mountainFestivals[activeFestivalIndex].video">
                <source :src="mountainFestivals[activeFestivalIndex].video" type="video/mp4" />
              </video>
            </template>
            <template v-else>
              <img :src="mountainFestivals[activeFestivalIndex].image" class="festival-image" alt="Festival" :key="mountainFestivals[activeFestivalIndex].image" />
            </template>
            <div class="festival-scrim"></div>
          </div>
          <div class="festival-display-content">
            <h3 class="display-name">{{ mountainFestivals[activeFestivalIndex].name }}</h3>
            <span class="display-region">📍 {{ mountainFestivals[activeFestivalIndex].region }}</span>
            <p class="display-desc">{{ mountainFestivals[activeFestivalIndex].description }}</p>
            <div class="display-vibe">
              <strong>Vibe:</strong> {{ mountainFestivals[activeFestivalIndex].vibe }}
            </div>
            <div class="display-trek">
              <strong>Connected Trek:</strong> {{ mountainFestivals[activeFestivalIndex].associatedTrek }}
            </div>
          </div>
        </div>

        <!-- Right Column: Interactive Menu List -->
        <div class="festivals-list">
          <div 
            v-for="(fest, idx) in mountainFestivals" 
            :key="fest.name"
            :class="['festival-item', { '--active': idx === activeFestivalIndex }]"
            @click="activeFestivalIndex = idx"
          >
            <div class="fest-item-header">
              <span class="fest-item-name">{{ fest.name }}</span>
              <span class="fest-item-dot"></span>
            </div>
            <span class="fest-item-region">{{ fest.region }}</span>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════
         YATRI DIARY (Polaroid & Experience Journal Reviews)
    ════════════════════════════════════════════════════════ -->
    <section class="diary-section scroll-fade">
      <div class="sec-header --center">
        <span class="sec-overline">Traveler Journals</span>
        <h2 class="sec-title">Yatri Diary</h2>
        <p class="sec-subtitle">Real experiences shared by hikers who completed their spiritual journeys with us.</p>
        <div class="divider-line --center"></div>
      </div>

      <div class="diary-grid">
        <div
          v-for="review in polaroidReviews"
          :key="review.id"
          class="polaroid-card"
        >
          <div class="polaroid-img-wrap">
            <img :src="review.img" :alt="review.trekName" />
            <span class="polaroid-stamp">APPROVED</span>
          </div>
          <div class="polaroid-body">
            <p class="polaroid-content">"{{ review.content }}"</p>
            <div class="polaroid-footer">
              <span class="polaroid-author">— {{ review.author }}</span>
              <span class="polaroid-date">{{ review.trekName }}, {{ review.date }}</span>
            </div>
          </div>
        </div>
      </div>
    </section>

    <!-- ═══════════════════════════════════════════════════
         JATAYU DHAROHAR (Conservation Pledge)
    ════════════════════════════════════════════════════════ -->
    <section class="dharohar-section scroll-fade">
      <div class="dharohar-container">
        <div class="dharohar-content">
          <span class="dharohar-tag">JATAYU DHAROHAR</span>
          <h2 class="dharohar-title">Himalayan Ecological Trust</h2>
          <p class="dharohar-desc">
            Traditional Indian culture worships mountains as gods. We are committed to leaving the peaks cleaner than we found them. We support local village economies and operate strictly on a zero-plastic trace-free model.
          </p>
          <div class="stats-counter-row">
            <div class="stat-counter">
              <div class="counter-num">1,420 kg</div>
              <div class="counter-label">Plastic waste collected</div>
            </div>
            <div class="stat-counter">
              <div class="counter-num">120+</div>
              <div class="counter-label">Local guide families supported</div>
            </div>
            <div class="stat-counter">
              <div class="counter-num">100%</div>
              <div class="counter-label">Carbon neutral treks</div>
            </div>
          </div>
        </div>
        <div class="dharohar-media">
          <img src="https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=75" alt="Clean Himalayas" class="dharohar-img" />
          <div class="dharohar-img-glow"></div>
        </div>
      </div>
    </section>

    <!-- Bottom CTA strip -->
    <div class="cta-strip">
      <div>
        <div class="cta-strip__title">Ready for your sacred yatra?</div>
        <div class="cta-strip__sub">Join thousands exploring the Indian summits with Jatayu.</div>
      </div>
      <router-link to="/register" class="hero-cta hero-cta--fill">Create Account ↗</router-link>
    </div>

  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted, computed } from 'vue'
import { gsap } from 'gsap'
import { treksAPI } from '../api'
import { useAuthStore } from '../store/auth'

const auth = useAuthStore()
const treks = ref([])
const fallback = 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=75'

// Element refs
const heroSection = ref(null)
const headlineWrap = ref(null)
const eyebrowEl = ref(null)
const headlineEl = ref(null)
const sublineEl = ref(null)
const ctasEl = ref(null)
const scrollHint = ref(null)
const seasonalGridEl = ref(null)
const carouselTrack = ref(null)

// ── FALLBACK TREKS IN CASE DB IS EMPTY ────────────────────────
const fallbackTreks = [
  {
    id: 1,
    name: 'Kedarkantha Yatra',
    location: 'Sankri, Uttarakhand',
    category: 'Snow',
    duration_days: 6,
    difficulty: 'Moderate',
    price_inr: 8500,
    max_altitude_m: 3810,
    available_slots: 8,
    total_slots: 20,
    avg_rating: 4.9,
    total_reviews: 42,
    cover_image: 'https://images.unsplash.com/photo-1626621341517-bbf3d9990a23?w=800&q=80',
    best_season: 'December - March',
    mythological_significance: 'Shiva stayed here in his bull form while hiding from the Pandavas, leaving his throat footprint (Kedar Kantha).'
  },
  {
    id: 2,
    name: 'Roopkund Mystery Lake',
    location: 'Lohajung, Uttarakhand',
    category: 'Heritage',
    duration_days: 8,
    difficulty: 'Hard',
    price_inr: 14500,
    max_altitude_m: 5029,
    available_slots: 4,
    total_slots: 15,
    avg_rating: 4.8,
    total_reviews: 31,
    cover_image: 'https://images.unsplash.com/photo-1605649487212-47bdab064df7?w=800&q=80',
    best_season: 'September - October',
    mythological_significance: 'Lord Shiva and Goddess Parvati created Roopkund Lake. Parvati bathed in its clear water and was enchanted by her own reflection.'
  },
  {
    id: 3,
    name: 'Valley of Flowers',
    location: 'Govindghat, Uttarakhand',
    category: 'Monsoon',
    duration_days: 6,
    difficulty: 'Easy',
    price_inr: 9500,
    max_altitude_m: 4300,
    available_slots: 12,
    total_slots: 25,
    avg_rating: 4.9,
    total_reviews: 58,
    cover_image: 'https://images.unsplash.com/photo-1548013146-72479768bada?w=800&q=80',
    best_season: 'July - August',
    mythological_significance: 'Mentioned in Ramayana, this is the sacred forest where Sanjeevani Buti was harvested by Hanuman to save Lakshmana.'
  }
]

// Display up to 8 treks for Featured Carousel
const displayTreks = computed(() => {
  return treks.value.length ? treks.value.slice(0, 8) : fallbackTreks
})

// Carousel navigation helper
function scrollCarousel(dir) {
  if (!carouselTrack.value) return
  const slide = carouselTrack.value.querySelector('.snap-slide')
  if (!slide) return
  const cardWidth = slide.offsetWidth
  carouselTrack.value.scrollBy({ left: dir * (cardWidth + 24), behavior: 'smooth' })
}

// ── RITUCHAKRA SEASONS ────────────────────────────────────────
const activeSeason = ref('Sharad')
const wheelRotation = ref(216) // Initial position for Sharad (index 3)

const seasons = [
  { 
    id: 'Vasant', 
    name: 'Vasant / Spring', 
    fullName: 'Vasant Ritu (Spring Season)',
    desc: 'Melting glacial ice, blooming rhododendrons, and awakening meadows.', 
    safety: 'Mild temperatures, low wind, clear mountain views.',
    icon: '🌸' 
  },
  { 
    id: 'Grishma', 
    name: 'Grishma / Summer', 
    fullName: 'Grishma Ritu (Summer Season)',
    desc: 'Open high mountain passes, lush bugyals (meadows), and comfortable nights.', 
    safety: 'Safe trails, excellent high altitude acclimatization.',
    icon: '☀️' 
  },
  { 
    id: 'Varsha', 
    name: 'Varsha / Monsoon', 
    fullName: 'Varsha Ritu (Monsoon Season)',
    desc: 'Valley of Flowers blooms at its peak. Mystical rain-veiled Himalayan slopes.', 
    safety: 'Landslide watch, rain gear essential, expert guide mandatory.',
    icon: '🌧️' 
  },
  { 
    id: 'Sharad', 
    name: 'Sharad / Autumn', 
    fullName: 'Sharad Ritu (Golden Autumn)',
    desc: 'Crystal-clear views of Nanda Devi and Trishul peaks under cloudless skies.', 
    safety: 'Very stable weather, cold nights, golden dry forest paths.',
    icon: '🍂' 
  },
  { 
    id: 'Shishir', 
    name: 'Shishir / Winter', 
    fullName: 'Shishir Ritu (Winter Snow)',
    desc: 'Snow-packed slopes, frozen alpine lakes, and dramatic white summits.', 
    safety: 'Heavy snow gear required, sub-zero protection, crampons needed.',
    icon: '❄️' 
  }
]

// Filter treks dynamically by season
const filteredTreks = computed(() => {
  const source = treks.value.length ? treks.value : fallbackTreks
  return source.filter(t => {
    const seasonStr = (t.best_season || '').toLowerCase()
    const catStr = (t.category || '').toLowerCase()
    
    if (activeSeason.value === 'Vasant') {
      return seasonStr.includes('march') || seasonStr.includes('april') || seasonStr.includes('spring')
    }
    if (activeSeason.value === 'Grishma') {
      return seasonStr.includes('may') || seasonStr.includes('june') || seasonStr.includes('summer')
    }
    if (activeSeason.value === 'Varsha') {
      return seasonStr.includes('july') || seasonStr.includes('august') || catStr.includes('monsoon') || catStr.includes('rain')
    }
    if (activeSeason.value === 'Sharad') {
      return seasonStr.includes('september') || seasonStr.includes('october') || seasonStr.includes('november') || seasonStr.includes('autumn')
    }
    if (activeSeason.value === 'Shishir') {
      return seasonStr.includes('december') || seasonStr.includes('january') || seasonStr.includes('february') || seasonStr.includes('winter') || catStr.includes('snow')
    }
    return true
  })
})

function selectSeason(seasonId, index) {
  activeSeason.value = seasonId
  if (index !== undefined) {
    wheelRotation.value = index * 72
  }
  // Smoothly stagger the new list layout using GSAP
  setTimeout(() => {
    if (seasonalGridEl.value) {
      gsap.from(seasonalGridEl.value.children, {
        opacity: 0,
        y: 20,
        stagger: 0.08,
        duration: 0.4,
        ease: 'power2.out'
      })
    }
  }, 50)
}

// ── MYTHOLOGICAL SIGNIFICANCE ─────────────────────────────────
const getGathaTag = (name) => {
  const lowercase = name.toLowerCase()
  if (lowercase.includes('brahma')) return 'Brahma Gatha'
  if (lowercase.includes('chadar')) return 'Zanskar Gatha'
  if (lowercase.includes('dayara')) return 'Aranya Gatha'
  if (lowercase.includes('sandakphu')) return 'Buddha Gatha'
  if (lowercase.includes('kedarnath')) return 'Rudra Gatha'
  if (lowercase.includes('hemkund')) return 'Khalsa Gatha'
  if (lowercase.includes('tungnath')) return 'Shiva Gatha'
  if (lowercase.includes('shrikhand')) return 'Mahadev Gatha'
  if (lowercase.includes('kinner')) return 'Kailash Gatha'
  if (lowercase.includes('amarnath')) return 'Amarnath Gatha'
  return 'Puranic Gatha'
}

const getGathaShloka = (name) => {
  const lowercase = name.toLowerCase()
  if (lowercase.includes('brahma')) return '“सृष्टिकर्त्रे नमः”'
  if (lowercase.includes('chadar')) return '“ॐ मणि पद्मे हूँ”'
  if (lowercase.includes('dayara')) return '“चरैवेति चरैवेति”'
  if (lowercase.includes('sandakphu')) return '“बुद्धं शरणं गच्छामि”'
  if (lowercase.includes('kedarnath')) return '“ॐ नमः शिवाय”'
  if (lowercase.includes('hemkund')) return '“सतनाम श्री वाहेगुरु”'
  if (lowercase.includes('tungnath')) return '“हर हर महादेव”'
  if (lowercase.includes('shrikhand')) return '“ॐ नमः शिवाय”'
  if (lowercase.includes('kinner')) return '“ॐ नमः शिवाय”'
  if (lowercase.includes('amarnath')) return '“जय बाबा बर्फानी”'
  return '“चरैवेति चरैवेति”'
}

const mythologicalTreks = computed(() => {
  const list = (treks.value.length ? treks.value : fallbackTreks).filter(t => t.mythological_significance)
  return list.length ? list.slice(0, 4) : fallbackTreks.slice(0, 3)
})

// ── MOUNTAIN FESTIVALS & UTSAVS ───────────────────────────────
const activeFestivalIndex = ref(0)
const mountainFestivals = [
  {
    name: 'Raulane Festival',
    region: 'Kinnaur, Himachal Pradesh',
    associatedTrek: 'Kinner Kailash Parikrama / Pin Bhaba / Shrikhand Mahadev',
    description: 'An ancient spring ritual celebrated in Kinnaur to express gratitude and bid a symbolic farewell to the Sauni (celestial mountain fairies) who protect the villagers during the harsh winter months.',
    vibe: 'Mystical masked dances, heavy ancestral silver jewelry, traditional Kinnauri woolen robes, and rhythmic drums.',
    video: '/raulane-video.mp4'
  },
  {
    name: 'Nanda Devi Raj Jat',
    region: 'Chamoli, Uttarakhand',
    associatedTrek: 'Roopkund Mystery Lake / Valley of Flowers / Kuari Pass',
    description: 'The legendary 12-yearly royal pilgrimage of Uttarakhand, honoring Goddess Nanda Devi\'s journey from her maternal home to her husband\'s abode on Mt. Nanda Devi.',
    vibe: 'Massive foot processions, sacred chants, local drums (Dhol-Damau), brass trumpets, and high-altitude shrines.',
    image: '/nandadevi.jpg'
  },
  {
    name: 'Kullu Dussehra',
    region: 'Kullu Valley, Himachal Pradesh',
    associatedTrek: 'Hampta Pass / Aancha Top / Pin Bhaba',
    description: 'A world-famous week-long festival where over 300 local deities in beautifully decorated palanquins assemble in Dhalpur Maidan to pay homage to Lord Raghunath.',
    vibe: 'Vibrant local trumpets (Karnal), traditional Nati folk dances, and majestic deity processions.',
    image: '/kulludussehra.jpg'
  },
  {
    name: 'Spituk Gustor',
    region: 'Leh, Ladakh',
    associatedTrek: 'Chadar Frozen River / Amarnath Cave Yatra',
    description: 'A sacred winter monastery festival featuring fearsome Cham dancers in heavy silk robes and masks representing protective Tibetan Buddhist deities, symbolizing the victory of dharma.',
    vibe: 'Monastic drums, brass cymbals, long horn trumpets (Dungchen), and meditative lama chants.',
    video: '/spitukgutor.mp4'
  },
  {
    name: 'Hornbill Festival',
    region: 'Kohima, Nagaland',
    associatedTrek: 'Dzukou Valley Trek',
    description: 'The ultimate festival of festivals showcasing the collective tribal culture, folklore, warrior dances, food, and music of all 17 major Naga tribes.',
    vibe: 'Traditional war shields, hornbill feathers, huge log drumming, and energetic warrior dances.',
    video: '/hornbill.mp4'
  }
]

// ── YATRI DIARY (Polaroid Reviews) ────────────────────────────
const polaroidReviews = [
  {
    id: 1,
    trekName: 'Kedarkantha Yatra',
    author: 'Rohan Sharma',
    date: 'Dec 2025',
    content: 'Standing at the frozen summit at 4 AM was beyond surreal. The wind was howling, but our local guide Devendra stood calmly, chanting a protective mountain prayer. It felt deeply spiritual.',
    audioDuration: '1m 24s',
    img: 'https://images.unsplash.com/photo-1464822759023-fed622ff2c3b?w=600&q=75'
  },
  {
    id: 2,
    trekName: 'Valley of Flowers',
    author: 'Priya Iyer',
    date: 'Aug 2025',
    content: 'The monsoon downpour made the trek challenging, but reaching the alpine valley filled with Himalayan blue poppies wiped out all fatigue. Authentic, root-level preservation at its best.',
    audioDuration: '0m 45s',
    img: '/flowers.png'
  }
]


// ── SCROLL TO SECTION ─────────────────────────────────────────
function scrollTo(selector) {
  const el = document.querySelector(selector)
  if (el) {
    el.scrollIntoView({ behavior: 'smooth' })
  }
}

// ── ENTRANCE ANIMATION ─────────────────────────────────────────
function runEntrance() {
  const tl = gsap.timeline({ defaults: { ease: 'power3.out' } })

  tl.from(eyebrowEl.value, { y: 16, opacity: 0, duration: 0.5 }, 0.2)
  tl.from(headlineEl.value, { y: 40, opacity: 0, duration: 0.7 }, 0.32)
  tl.from(sublineEl.value, { y: 14, opacity: 0, duration: 0.5 }, 0.52)
  tl.from(ctasEl.value, { y: 12, opacity: 0, duration: 0.45 }, 0.65)

  if (scrollHint.value) {
    tl.from(scrollHint.value, { opacity: 0, duration: 0.4 }, 0.9)
    gsap.to(scrollHint.value.querySelector('.scroll-hint__dot'), {
      y: 24, duration: 1.2, ease: 'power1.inOut', yoyo: true, repeat: -1
    })
  }
}

onMounted(async () => {
  runEntrance()

  // Scroll animations IntersectionObserver
  const observer = new IntersectionObserver((entries) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        entry.target.classList.add('visible')
      }
    })
  }, { threshold: 0.05, rootMargin: '0px 0px -50px 0px' })

  document.querySelectorAll('.scroll-fade').forEach(el => {
    observer.observe(el)
  })

  try {
    const res = await treksAPI.list({ per_page: 12 })
    treks.value = res.data.treks
  } catch (e) {
    console.warn('Treks load failed', e)
  }
})

onUnmounted(() => {
  gsap.killTweensOf('*')
})
</script>

<style scoped>
/* ─── Global Base ────────────────────────────────────────── */
.home-page {
  background: #0A090D; /* Ganga Dusk Black */
  min-height: 100vh;
  font-family: 'Outfit', sans-serif;
  overflow-x: hidden;
  color: #F5F5FA;
}

/* Section Common Layouts */
.sec-header {
  margin-bottom: 50px;
  padding: 0 52px;
}
.sec-header.--center {
  text-align: center;
  padding: 0 20px;
}
.sec-overline {
  font-size: 11px;
  letter-spacing: 0.3em;
  font-weight: 600;
  color: #E8A838; /* Swarna Gold */
  text-transform: uppercase;
  display: block;
  margin-bottom: 10px;
}
.sec-title {
  font-size: clamp(28px, 4vw, 44px);
  font-weight: 800;
  color: #fff;
  font-family: 'Cinzel', Georgia, serif;
  margin: 0 0 10px;
  letter-spacing: -0.01em;
}
.sec-subtitle {
  font-size: 15px;
  color: rgba(255,255,255,0.45);
  font-weight: 300;
  max-width: 600px;
  margin: 0 auto;
}
.divider-line {
  width: 80px;
  height: 2px;
  background: linear-gradient(90deg, #E8A838, transparent);
  margin-top: 15px;
}
.divider-line.--center {
  background: linear-gradient(90deg, transparent, #E8A838 50%, transparent);
  margin: 15px auto 0;
}

/* ══════════════════════════════════════════════════════════
   HERO SECTION
══════════════════════════════════════════════════════════ */
.hero {
  position: relative;
  width: 100%;
  height: 80vh;
  min-height: 520px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.hero-video-layer {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}
.hero-video {
  position: absolute;
  top: 50%;
  left: 50%;
  width: 80vh;
  height: 100vw;
  min-width: 520px;
  transform: translate(-50%, -50%) rotate(-90deg);
  object-fit: cover;
}
.hero-img-fallback {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.hero-overlay {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(10, 9, 13, 0.1) 0%, rgba(10, 9, 13, 0.55) 100%);
  z-index: 2;
  pointer-events: none;
}
.hero-vignette {
  position: absolute;
  inset: 0;
  z-index: 3;
  pointer-events: none;
  background: radial-gradient(circle, transparent 50%, rgba(10, 9, 13, 0.35) 100%);
}

.hero-nav {
  position: absolute;
  top: 0; left: 0; right: 0;
  z-index: 30;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 24px 52px;
}
.nav-brand {
  display: flex;
  align-items: center;
  gap: 12px;
}
.nav-brand__gem {
  width: 38px; height: 38px;
  border-radius: 10px;
  background: rgba(232,168,56,0.13);
  border: 1px solid rgba(232,168,56,0.32);
  display: flex; align-items: center; justify-content: center;
  color: #E8A838; font-size: 16px; font-weight: bold;
}
.nav-brand__name {
  color: #fff; font-size: 20px; font-weight: 700; letter-spacing: -0.01em;
  font-family: 'Cinzel', Georgia, serif;
}
.nav-brand__name em { color: #E8A838; font-style: normal; }
.nav-brand__sub {
  font-size: 10px; color: rgba(255,255,255,0.4); margin-top: 1px;
  text-transform: uppercase; letter-spacing: 0.1em;
}
.nav-links {
  display: flex; gap: 35px;
}
.nav-link {
  color: rgba(255,255,255,0.6); font-size: 13.5px; font-weight: 500;
  text-decoration: none; letter-spacing: 0.05em; transition: color 0.2s;
}
.nav-link:hover { color: #E8A838; }

.nav-actions { display: flex; gap: 12px; }
.nav-btn {
  font-size: 12.5px; font-weight: 600; padding: 9px 22px;
  border-radius: 100px; text-decoration: none; transition: all 0.25s;
}
.nav-btn--ghost {
  background: rgba(255,255,255,0.05);
  border: 1px solid rgba(255,255,255,0.15);
  color: rgba(255,255,255,0.85);
}
.nav-btn--ghost:hover {
  background: rgba(255,255,255,0.12);
  border-color: rgba(255,255,255,0.35);
}
.nav-btn--gold {
  background: #E8A838; color: #160a03;
  box-shadow: 0 4px 20px rgba(232,168,56,0.3);
}
.nav-btn--gold:hover {
  transform: translateY(-1px);
  box-shadow: 0 8px 28px rgba(232,168,56,0.45);
  filter: brightness(1.06);
}

.hero-headline-wrap {
  position: relative;
  z-index: 10;
  text-align: center;
  padding: 0 20px;
}
.hero-eyebrow {
  font-size: 10px;
  letter-spacing: 0.4em;
  font-weight: 600;
  color: #E8A838;
  text-transform: uppercase;
  margin-bottom: 22px;
}
.hero-headline {
  font-size: clamp(32px, 4.5vw, 62px);
  font-weight: 900;
  color: #fff;
  line-height: 1.08;
  letter-spacing: -0.01em;
  text-transform: uppercase;
  margin: 0 0 20px;
  font-family: 'Cinzel', Georgia, serif;
  text-shadow: 0 4px 30px rgba(0,0,0,0.8);
}
.hero-headline em {
  font-style: normal;
  background: linear-gradient(135deg, #ffeaa7 0%, #e8a838 50%, #b26a06 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  background-clip: text;
}
.hero-subline {
  font-size: clamp(12px, 1.4vw, 15px);
  color: rgba(255,255,255,0.7);
  font-weight: 300;
  line-height: 1.6;
  margin: 0 auto 30px;
  max-width: 650px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.4);
}
.hero-ctas {
  display: flex;
  gap: 16px;
  justify-content: center;
}
.hero-cta {
  display: inline-flex; align-items: center; gap: 8px;
  text-decoration: none; font-size: 13.5px; font-weight: 600;
  padding: 13px 30px; border-radius: 100px; transition: all 0.25s;
}
.hero-cta--fill {
  background: #E8A838; color: #160a03;
  box-shadow: 0 8px 30px rgba(232,168,56,0.35);
}
.hero-cta--fill:hover {
  transform: translateY(-2px);
  box-shadow: 0 14px 36px rgba(232,168,56,0.5);
  filter: brightness(1.08);
}
.hero-cta--outline {
  background: rgba(255,255,255,0.06);
  color: rgba(255,255,255,0.85);
  border: 1px solid rgba(255,255,255,0.18);
  backdrop-filter: blur(10px);
}
.hero-cta--outline:hover {
  background: rgba(255,255,255,0.12); color: #fff; transform: translateY(-2px);
  border-color: rgba(255,255,255,0.3);
}

.scroll-hint {
  position: absolute;
  bottom: 30px;
  left: 50%;
  transform: translateX(-50%);
  z-index: 25;
  display: flex; flex-direction: column; align-items: center; gap: 8px;
}
.scroll-hint span {
  font-size: 9px; letter-spacing: 0.25em; color: rgba(255,255,255,0.35); text-transform: uppercase;
}
.scroll-hint__line {
  width: 1px; height: 40px;
  background: linear-gradient(180deg, #E8A838, transparent);
}
.scroll-hint__dot {
  width: 6px; height: 6px; border-radius: 50%;
  background: #E8A838;
}

/* ══════════════════════════════════════════════════════════
   SACRED SCROLLING STRIP (TRANSITION BAND)
══════════════════════════════════════════════════════════ */
.sacred-marquee-band {
  background: linear-gradient(90deg, #130f1a, #1a1424);
  border-top: 1px solid rgba(232, 168, 56, 0.25);
  border-bottom: 1px solid rgba(232, 168, 56, 0.25);
  padding: 14px 0;
  overflow: hidden;
  position: relative;
  z-index: 10;
  box-shadow: inset 0 0 10px rgba(0, 0, 0, 0.8);
}
.marquee-content {
  display: flex;
  white-space: nowrap;
  gap: 40px;
  animation: marqueeScroll 25s linear infinite;
}
.marquee-content span {
  font-family: 'Cinzel', Georgia, serif;
  font-size: 11px;
  font-weight: 700;
  color: rgba(232, 168, 56, 0.85);
  letter-spacing: 0.2em;
  text-transform: uppercase;
  text-shadow: 0 0 8px rgba(232, 168, 56, 0.25);
}
@keyframes marqueeScroll {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* ══════════════════════════════════════════════════════════
   FEATURED CAROUSEL SECTION
══════════════════════════════════════════════════════════ */
.treks-section {
  padding: 60px 52px 30px;
  background: #0A090D;
}
.carousel-container {
  display: flex;
  align-items: center;
  position: relative;
  gap: 16px;
  margin-top: 30px;
}
.carousel-control {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(232, 168, 56, 0.3);
  color: #E8A838;
  font-size: 16px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s;
  flex-shrink: 0;
  z-index: 5;
}
.carousel-control:hover {
  background: #E8A838;
  color: #0A090D;
  box-shadow: 0 0 15px rgba(232, 168, 56, 0.4);
}
.carousel-track-snap {
  display: flex;
  gap: 24px;
  overflow-x: auto;
  scroll-snap-type: x mandatory;
  scrollbar-width: none;
  scroll-behavior: smooth;
  width: 100%;
  padding: 10px 0;
}
.carousel-track-snap::-webkit-scrollbar {
  display: none;
}
.snap-slide {
  scroll-snap-align: start;
  flex: 0 0 calc(33.333% - 16px);
  box-sizing: border-box;
}
@media (max-width: 1024px) {
  .snap-slide {
    flex: 0 0 calc(50% - 12px);
  }
}
@media (max-width: 768px) {
  .snap-slide {
    flex: 0 0 100%;
  }
}

.trek-card-gold {
  background: rgba(255, 255, 255, 0.02);
  border: 1px solid rgba(232, 168, 56, 0.15);
  border-radius: 20px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1);
  position: relative;
  box-shadow: 0 10px 30px rgba(0,0,0,0.3);
}
.trek-card-gold:hover {
  transform: translateY(-8px);
  border-color: rgba(232, 168, 56, 0.45);
  box-shadow: 0 20px 50px rgba(232, 168, 56, 0.12), 0 5px 15px rgba(0,0,0,0.5);
}
.trek-card-gold__img-wrap {
  height: 220px;
  position: relative;
  overflow: hidden;
}
.trek-card-gold__img-wrap img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s ease;
}
.trek-card-gold:hover .trek-card-gold__img-wrap img {
  transform: scale(1.08);
}
.trek-card-gold__price-tag {
  position: absolute;
  top: 15px; left: 15px;
  background: rgba(10, 9, 13, 0.85);
  color: #E8A838;
  font-weight: 700;
  padding: 6px 14px;
  border-radius: 30px;
  font-size: 14px;
  border: 1px solid rgba(232, 168, 56, 0.4);
}
.trek-card-gold__badge {
  position: absolute;
  top: 15px; right: 15px;
  background: #E8A838;
  color: #160a03;
  font-weight: 700;
  padding: 4px 12px;
  border-radius: 8px;
  font-size: 11px;
  text-transform: uppercase;
  letter-spacing: 0.05em;
}
.trek-card-gold__body {
  padding: 24px;
}
.trek-card-gold__rating {
  font-size: 12px;
  color: rgba(255,255,255,0.7);
  display: flex;
  align-items: center;
  gap: 5px;
  margin-bottom: 12px;
}
.rating-star {
  font-size: 13px;
  color: #E8A838;
}
.rating-count {
  color: rgba(255,255,255,0.4);
}
.trek-card-gold__title {
  font-size: 21px;
  font-weight: 700;
  color: #fff;
  font-family: 'Cinzel', Georgia, serif;
  margin: 0 0 6px;
  transition: color 0.2s;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}
.trek-card-gold:hover .trek-card-gold__title {
  color: #E8A838;
}
.trek-card-gold__loc {
  font-size: 12px;
  color: rgba(255,255,255,0.5);
  margin-bottom: 20px;
}
.trek-card-gold__meta {
  display: flex;
  gap: 10px;
  margin-bottom: 22px;
}
.trek-card-gold__meta span {
  font-size: 11.5px;
  color: rgba(255,255,255,0.85);
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid rgba(255,255,255,0.06);
  padding: 4px 10px;
  border-radius: 8px;
}
.difficulty-pill {
  font-weight: 600;
}
.difficulty-pill.--easy { color: #50d28c; }
.difficulty-pill.--moderate { color: #E8A838; }
.difficulty-pill.--hard { color: #ff7060; }

.slots-indicator {
  margin-top: 15px;
}
.slots-bar {
  height: 4px;
  width: 100%;
  background: rgba(255,255,255,0.08);
  border-radius: 10px;
  overflow: hidden;
  margin-bottom: 6px;
}
.slots-bar-fill {
  height: 100%;
  background: linear-gradient(90deg, #b26a06, #E8A838);
  border-radius: 10px;
}
.slots-text {
  display: flex;
  justify-content: space-between;
  font-size: 11px;
  color: rgba(255,255,255,0.4);
}

/* ══════════════════════════════════════════════════════════
   RITUCHAKRA (Seasonal Selector Wheel Engine Layout)
══════════════════════════════════════════════════════════ */
.rituchakra-section {
  padding: 40px 52px 50px;
  background: #060508;
  border-top: 1px solid rgba(255,255,255,0.02);
  border-bottom: 1px solid rgba(255,255,255,0.02);
}
.season-picker-wrap {
  margin-top: 50px;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 50px;
  align-items: center;
}
@media (max-width: 900px) {
  .season-picker-wrap {
    grid-template-columns: 1fr;
  }
}

.rituchakra-wheel-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  position: relative;
  height: 340px;
  justify-content: center;
}
.wheel-pointer {
  position: absolute;
  top: 10px;
  font-size: 22px;
  z-index: 5;
  filter: drop-shadow(0 0 8px #E8A838);
}
.rituchakra-wheel {
  width: 270px;
  height: 270px;
  border-radius: 50%;
  border: 2px solid rgba(232, 168, 56, 0.25);
  box-shadow: 0 0 35px rgba(232, 168, 56, 0.08), inset 0 0 35px rgba(232, 168, 56, 0.08);
  position: relative;
  transition: transform 0.8s cubic-bezier(0.25, 1, 0.5, 1);
  display: flex;
  align-items: center;
  justify-content: center;
  background: rgba(10, 9, 13, 0.6);
}
.rituchakra-wheel::before {
  content: '';
  position: absolute;
  inset: -12px;
  border-radius: 50%;
  border: 1px dashed rgba(232, 168, 56, 0.15);
  animation: rotateClockwise 60s linear infinite;
  pointer-events: none;
}
.rituchakra-wheel::after {
  content: '';
  position: absolute;
  inset: 15px;
  border-radius: 50%;
  border: 1px solid rgba(255, 255, 255, 0.03);
  pointer-events: none;
}
@keyframes rotateClockwise {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}
.wheel-slice {
  position: absolute;
  top: 50%;
  left: 50%;
  margin-top: -26px;
  margin-left: -40px;
  width: 80px;
  height: 52px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  border-radius: 30px;
  transition: all 0.3s ease;
}
.slice-icon {
  font-size: 20px;
}
.slice-name {
  font-size: 9.5px;
  font-weight: 700;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  color: rgba(255, 255, 255, 0.4);
  margin-top: 3px;
}
.wheel-slice.active .slice-name {
  color: #E8A838;
}
.wheel-slice.active {
  background: rgba(232, 168, 56, 0.08);
  border: 1px solid rgba(232, 168, 56, 0.3);
  transform: scale(1.1);
  box-shadow: 0 0 15px rgba(232, 168, 56, 0.15);
}
.wheel-center {
  width: 90px;
  height: 90px;
  border-radius: 50%;
  background: #0A090D;
  border: 1.5px solid rgba(232, 168, 56, 0.4);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 0 15px rgba(232, 168, 56, 0.1);
}
.wheel-center-inner {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
}
.center-season-icon {
  font-size: 22px;
}
.center-season-lbl {
  font-size: 9px;
  font-weight: 700;
  color: #E8A838;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-top: 4px;
}

.season-details-panel {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 40px;
  background: rgba(255,255,255,0.01);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 24px;
  padding: 40px;
}
.season-meta h3 {
  font-family: 'Cinzel', Georgia, serif;
  font-size: 26px;
  color: #fff;
  margin: 0 0 16px;
}
.season-desc {
  font-size: 15px;
  line-height: 1.8;
  color: rgba(255,255,255,0.65);
  margin-bottom: 24px;
}
.weather-alert {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(232, 168, 56, 0.06);
  border: 1px solid rgba(232, 168, 56, 0.15);
  padding: 16px 20px;
  border-radius: 12px;
  font-size: 13.5px;
  color: #E8A838;
}

.seasonal-compact-card {
  display: flex;
  gap: 20px;
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 16px;
  overflow: hidden;
  padding: 12px;
  margin-bottom: 16px;
  cursor: pointer;
  transition: all 0.25s;
}
.seasonal-compact-card:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(232, 168, 56, 0.3);
  transform: translateX(5px);
}
.seasonal-compact-img {
  width: 90px;
  height: 90px;
  border-radius: 10px;
  overflow: hidden;
  flex-shrink: 0;
}
.seasonal-compact-img img {
  width: 100%; height: 100%; object-fit: cover;
}
.seasonal-compact-body {
  display: flex;
  flex-direction: column;
  justify-content: center;
}
.seasonal-compact-body h4 {
  font-family: 'Cinzel', Georgia, serif;
  font-size: 16px;
  color: #fff;
  margin: 0 0 6px;
}
.seasonal-compact-body p {
  font-size: 12.5px;
  color: rgba(255,255,255,0.45);
  margin: 0 0 8px;
}
.seasonal-compact-tag {
  font-size: 9px;
  font-weight: 700;
  text-transform: uppercase;
  color: #E8A838;
  letter-spacing: 0.05em;
  align-self: flex-start;
}

.seasonal-empty {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 60px 20px;
  color: rgba(255,255,255,0.3);
}
.empty-icon {
  font-size: 40px;
  margin-bottom: 16px;
  opacity: 0.6;
}

/* ══════════════════════════════════════════════════════════
   DEVBHUMI GATHA
══════════════════════════════════════════════════════════ */
.gatha-section {
  padding: 50px 52px 90px;
  background: #0A090D;
}
.gatha-scroll-container {
  overflow-x: auto;
  margin-top: 50px;
  padding-bottom: 20px;
}
.gatha-scroll-container::-webkit-scrollbar {
  height: 4px;
}
.gatha-scroll-container::-webkit-scrollbar-thumb {
  background: rgba(232, 168, 56, 0.2);
  border-radius: 10px;
}
.gatha-row {
  display: flex;
  gap: 30px;
  width: max-content;
}

.gatha-card {
  width: 380px;
  background: #EFEFEF;
  border-radius: 20px;
  padding: 30px;
  box-shadow: 0 10px 40px rgba(0,0,0,0.6);
  position: relative;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
  min-height: 260px;
  border: 1px solid rgba(0,0,0,0.1);
  overflow: hidden;
}
.gatha-card__bg-icon {
  position: absolute;
  right: -20px;
  bottom: -30px;
  font-size: 160px;
  font-weight: 800;
  color: rgba(232, 168, 56, 0.08);
  pointer-events: none;
  font-family: serif;
}
.gatha-card__header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.gatha-card__tag {
  font-size: 9.5px;
  font-weight: 700;
  letter-spacing: 0.1em;
  color: #b26a06;
  text-transform: uppercase;
  border: 1px solid rgba(178, 106, 6, 0.2);
  padding: 3px 8px;
  border-radius: 6px;
}
.gatha-card__shloka {
  font-size: 11px;
  color: rgba(0,0,0,0.4);
  font-weight: 500;
}
.gatha-card__title {
  font-size: clamp(20px, 2.5vw, 24px);
  color: #1A191D;
  font-family: 'Cinzel', Georgia, serif;
  margin: 16px 0 10px;
  font-weight: 700;
}
.gatha-card__text {
  font-size: 13.5px;
  color: #4C4B4F;
  line-height: 1.6;
  margin: 0 0 20px;
  font-style: italic;
}
.gatha-card__footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
  color: rgba(0,0,0,0.5);
  font-weight: 500;
}
.gatha-card__link {
  color: #b26a06;
  text-decoration: none;
  font-weight: 700;
}
.gatha-card__link:hover {
  text-decoration: underline;
}

/* ══════════════════════════════════════════════════════════
   FESTIVALS SECTION (Utsav of the Peaks)
══════════════════════════════════════════════════════════ */
.festivals-section {
  padding: 50px 52px;
  background: #060508;
  border-top: 1px solid rgba(255,255,255,0.02);
}
.festivals-container {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 40px;
  margin-top: 50px;
}
@media (max-width: 992px) {
  .festivals-container {
    grid-template-columns: 1fr;
  }
}
.festival-display-card {
  position: relative;
  background: rgba(255,255,255,0.01);
  border: 1px solid rgba(255,255,255,0.05);
  border-radius: 24px;
  overflow: hidden;
  display: flex;
  flex-direction: column;
  box-shadow: 0 30px 60px rgba(0,0,0,0.8);
  min-height: 480px;
}
.festival-media-wrapper {
  position: absolute;
  inset: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  overflow: hidden;
}
.festival-video, .festival-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.festival-scrim {
  position: absolute;
  inset: 0;
  background: linear-gradient(180deg, rgba(10,9,13,0.1) 0%, rgba(10,9,13,0.85) 100%);
  z-index: 2;
}
.festival-display-content {
  position: relative;
  z-index: 3;
  margin-top: auto;
  padding: 40px;
  color: #fff;
}
.display-name {
  font-size: clamp(24px, 3vw, 32px);
  font-weight: 800;
  color: #fff;
  font-family: 'Cinzel', Georgia, serif;
  margin: 0 0 8px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}
.display-region {
  font-size: 13px;
  color: #E8A838;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.05em;
  display: inline-block;
  margin-bottom: 20px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}
.display-desc {
  font-size: 14.5px;
  color: rgba(255,255,255,0.9);
  line-height: 1.6;
  margin: 0 0 20px;
  max-width: 600px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}
.display-vibe, .display-trek {
  font-size: 13px;
  color: rgba(255,255,255,0.7);
  margin-bottom: 8px;
  text-shadow: 0 2px 10px rgba(0,0,0,0.8);
}
.display-vibe strong, .display-trek strong {
  color: #fff;
}

.festivals-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  justify-content: center;
}
.festival-item {
  background: rgba(255,255,255,0.02);
  border: 1px solid rgba(255,255,255,0.04);
  border-radius: 16px;
  padding: 18px 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
}
.festival-item:hover {
  background: rgba(255,255,255,0.05);
  border-color: rgba(255,255,255,0.1);
  transform: translateX(5px);
}
.festival-item.--active {
  background: rgba(232, 168, 56, 0.08);
  border-color: rgba(232, 168, 56, 0.4);
  box-shadow: 0 10px 30px rgba(232,168,56,0.05);
}
.fest-item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 4px;
}
.fest-item-name {
  font-size: 16px;
  font-weight: 700;
  color: #fff;
  font-family: 'Cinzel', Georgia, serif;
  transition: color 0.3s;
}
.festival-item.--active .fest-item-name {
  color: #E8A838;
}
.fest-item-dot {
  width: 6px;
  height: 6px;
  background: transparent;
  border-radius: 50%;
  transition: background 0.3s;
}
.festival-item.--active .fest-item-dot {
  background: #E8A838;
  box-shadow: 0 0 10px #E8A838;
}
.fest-item-region {
  font-size: 12px;
  color: rgba(255,255,255,0.4);
}
.festival-item.--active .fest-item-region {
  color: rgba(255,255,255,0.65);
}

/* ══════════════════════════════════════════════════════════
   YATRI DIARY
══════════════════════════════════════════════════════════ */
.diary-section {
  padding: 50px 52px;
  background: #0A090D;
}
.diary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(320px, 1fr));
  gap: 40px;
  margin-top: 50px;
}
.polaroid-card {
  background: #F4F3EF;
  padding: 18px 18px 28px;
  box-shadow: 0 15px 40px rgba(0,0,0,0.5);
  transform: rotate(-1.5deg);
  transition: transform 0.3s;
}
.polaroid-card:nth-child(2n) {
  transform: rotate(1.5deg);
}
.polaroid-card:hover {
  transform: scale(1.02) rotate(0deg);
  z-index: 10;
}
.polaroid-img-wrap {
  width: 100%;
  height: 220px;
  overflow: hidden;
  position: relative;
  border: 1px solid rgba(0,0,0,0.1);
  margin-bottom: 18px;
}
.polaroid-img-wrap img {
  width: 100%; height: 100%; object-fit: cover;
}
.polaroid-stamp {
  position: absolute;
  bottom: 12px; right: 12px;
  border: 2.5px solid #d2322d;
  color: #d2322d;
  font-weight: 900;
  font-size: 11px;
  padding: 3px 8px;
  border-radius: 4px;
  transform: rotate(-12deg);
  letter-spacing: 0.05em;
  background: rgba(255, 255, 255, 0.9);
}
.polaroid-body {
  padding: 0 4px;
}
.voice-memo-panel {
  display: flex;
  align-items: center;
  gap: 12px;
  background: rgba(0,0,0,0.04);
  border: 1px solid rgba(0,0,0,0.06);
  border-radius: 12px;
  padding: 8px 12px;
  margin-bottom: 14px;
}
.voice-play-btn {
  width: 28px; height: 28px;
  border-radius: 50%;
  border: none;
  background: #1C1A17;
  color: #fff;
  cursor: pointer;
  display: flex; align-items: center; justify-content: center;
  font-size: 10px;
}
.voice-wave {
  display: flex;
  align-items: center;
  gap: 3px;
  flex-grow: 1;
  height: 20px;
}
.wave-bar {
  width: 2.5px;
  height: 6px;
  background: rgba(0,0,0,0.18);
  border-radius: 4px;
}
.wave-bar:nth-child(2n) { height: 12px; }
.wave-bar:nth-child(3n) { height: 16px; }
.wave-bar.active {
  background: #E8A838;
  animation: wavePulse 1s ease-in-out infinite alternate;
}
.wave-bar:nth-child(2n).active { animation-delay: 0.15s; }
.wave-bar:nth-child(3n).active { animation-delay: 0.3s; }

@keyframes wavePulse {
  to { transform: scaleY(1.7); }
}
.voice-time {
  font-size: 11px;
  color: rgba(0,0,0,0.45);
}

.polaroid-content {
  font-family: 'Caveat', cursive;
  font-size: clamp(18px, 2.2vw, 21px);
  line-height: 1.4;
  margin: 0 0 16px;
  color: #3C3A35;
}
.polaroid-footer {
  display: flex;
  flex-direction: column;
  font-size: 11.5px;
  color: rgba(0,0,0,0.5);
  border-top: 1px dashed rgba(0,0,0,0.1);
  padding-top: 10px;
}
.polaroid-author {
  font-weight: 700;
  color: #1C1A17;
}

/* ══════════════════════════════════════════════════════════
   JATAYU DHAROHAR
══════════════════════════════════════════════════════════ */
.dharohar-section {
  padding: 50px 52px;
  background: #060508;
}
.dharohar-container {
  display: grid;
  grid-template-columns: 1.2fr 0.8fr;
  gap: 50px;
  background: linear-gradient(135deg, rgba(232,168,56,0.06), rgba(232,168,56,0.01));
  border: 1px solid rgba(232,168,56,0.15);
  border-radius: 28px;
  padding: 50px;
  align-items: center;
}
.dharohar-content {
  display: flex;
  flex-direction: column;
}
.dharohar-tag {
  font-size: 10px;
  letter-spacing: 0.35em;
  font-weight: 700;
  color: #E8A838;
  margin-bottom: 14px;
}
.dharohar-title {
  font-family: 'Cinzel', Georgia, serif;
  font-size: clamp(26px, 4vw, 36px);
  color: #fff;
  margin: 0 0 18px;
}
.dharohar-desc {
  font-size: 15px;
  line-height: 1.8;
  color: rgba(255,255,255,0.65);
  margin-bottom: 35px;
}
.stats-counter-row {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.stat-counter .counter-num {
  font-size: clamp(24px, 3.5vw, 34px);
  font-weight: 800;
  color: #E8A838;
  font-family: 'Cinzel', Georgia, serif;
}
.stat-counter .counter-label {
  font-size: 12px;
  color: rgba(255,255,255,0.45);
  margin-top: 4px;
}

.dharohar-media {
  position: relative;
  border-radius: 20px;
  overflow: hidden;
  height: 320px;
}
.dharohar-img {
  width: 100%; height: 100%; object-fit: cover;
}
.dharohar-img-glow {
  position: absolute; inset: 0;
  box-shadow: inset 0 0 50px rgba(10,9,13,0.8);
}

/* ─── Scroll Fade Animation ─── */
.scroll-fade {
  opacity: 0;
  transform: translateY(30px);
  transition: opacity 1.2s cubic-bezier(0.16, 1, 0.3, 1), transform 1.2s cubic-bezier(0.16, 1, 0.3, 1);
}
.scroll-fade.visible {
  opacity: 1;
  transform: translateY(0);
}

/* ══════════════════════════════════════════════════════════
   CTA STRIP & RESPONSIVE
══════════════════════════════════════════════════════════ */
.cta-strip {
  margin: 0 52px 80px;
  background: linear-gradient(135deg, rgba(232,168,56,0.1), rgba(232,168,56,0.02));
  border: 1px solid rgba(232,168,56,0.2);
  border-radius: 24px; padding: 40px 50px;
  display: flex; align-items: center; justify-content: space-between;
}
.cta-strip__title {
  color: #fff; font-size: clamp(20px, 3vw, 24px); font-weight: 700;
  font-family: 'Cinzel', Georgia, serif; margin-bottom: 8px;
}
.cta-strip__sub { color: rgba(255,255,255,0.4); font-size: 14px; }

/* ─── Responsive Styles ─────────────────────────────────── */
@media (max-width: 1024px) {
  .hero-nav { padding: 20px 30px; }
  .treks-section, .rituchakra-section, .gatha-section, .festivals-section, .diary-section, .dharohar-section {
    padding: 80px 30px;
  }
  .season-details-panel { grid-template-columns: 1fr; gap: 30px; padding: 30px; }
  .dharohar-container { grid-template-columns: 1fr; gap: 40px; padding: 35px; }
  .cta-strip { margin: 0 30px 60px; }
}

@media (max-width: 768px) {
  .hero-nav { padding: 16px 20px; }
  .nav-links { display: none; }
  .treks-section, .rituchakra-section, .gatha-section, .festivals-section, .diary-section, .dharohar-section {
    padding: 60px 20px;
  }
  .season-picker-wrap { gap: 30px; }
  .gatha-card { width: 310px; padding: 24px; }
  .stats-counter-row { grid-template-columns: 1fr; gap: 15px; }
  .cta-strip { margin: 0 20px 48px; flex-direction: column; text-align: center; gap: 24px; padding: 30px 20px; }
  .hero-headline { font-size: 38px; }
}
</style>

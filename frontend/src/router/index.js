import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '../store/auth'

// Auth
const LoginView       = () => import('../views/auth/LoginView.vue')
const RegisterView    = () => import('../views/auth/RegisterView.vue')

// Public
const HomeView        = () => import('../views/HomeView.vue')
const TreksListView   = () => import('../views/TreksListView.vue')
const TrekDetailView  = () => import('../views/TrekDetailView.vue')

// Admin — screens 3,4,5,6,7
const AdminDashboard  = () => import('../views/admin/AdminDashboard.vue')
const AdminTreks      = () => import('../views/admin/AdminTreks.vue')
const AdminStaff      = () => import('../views/admin/AdminStaff.vue')
const AdminUsers      = () => import('../views/admin/AdminUsers.vue')
const AdminBookings   = () => import('../views/admin/AdminBookings.vue')
const AdminPartners   = () => import('../views/admin/AdminPartners.vue')

// Staff — screens 8,9
const StaffDashboard    = () => import('../views/staff/StaffDashboard.vue')
const StaffTreks        = () => import('../views/staff/StaffTreks.vue')
const StaffParticipants = () => import('../views/staff/StaffParticipants.vue')
const StaffProfile      = () => import('../views/staff/StaffProfile.vue')
const StaffTrekDetail   = () => import('../views/staff/StaffTrekDetail.vue')

// User/Trekker — screens 10,11,12
const UserDashboard   = () => import('../views/user/UserDashboard.vue')
const BrowseTreks     = () => import('../views/user/BrowseTreks.vue')
const TrekHistory     = () => import('../views/user/TrekHistory.vue')
const UserProfile     = () => import('../views/user/UserProfile.vue')

const routes = [
  // Public
  { path: '/',          name: 'home',         component: HomeView },
  { path: '/login',     name: 'login',        component: LoginView },
  { path: '/register',  name: 'register',     component: RegisterView },
  { path: '/treks',     name: 'treks',        component: TreksListView },
  { path: '/treks/:id', name: 'trek-detail',  component: TrekDetailView },

  // Admin (screens 3–7)
  {
    path: '/admin',
    meta: { requiresAuth: true, role: 'admin' },
    children: [
      { path: '',           name: 'admin-dashboard', component: AdminDashboard },
      { path: 'treks',      name: 'admin-treks',     component: AdminTreks },
      { path: 'staff',      name: 'admin-staff',     component: AdminStaff },
      { path: 'users',      name: 'admin-users',     component: AdminUsers },
      { path: 'bookings',   name: 'admin-bookings',  component: AdminBookings },
      { path: 'partners',   name: 'admin-partners',  component: AdminPartners },
    ],
  },

  // Staff (screens 8–9)
  {
    path: '/staff',
    meta: { requiresAuth: true, role: 'staff' },
    children: [
      { path: '',             name: 'staff-dashboard',    component: StaffDashboard },
      { path: 'treks',        name: 'staff-treks',        component: StaffTreks },
      { path: 'participants', name: 'staff-participants', component: StaffParticipants },
      { path: 'profile',      name: 'staff-profile',      component: StaffProfile },
      { path: 'trek/:id',     name: 'staff-trek',         component: StaffTrekDetail },
    ],
  },

  // User/Trekker (screens 10–12)
  {
    path: '/dashboard',
    meta: { requiresAuth: true, role: 'trekker' },
    children: [
      { path: '',         name: 'user-dashboard', component: UserDashboard },
      { path: 'browse',   name: 'browse-treks',   component: BrowseTreks },
      { path: 'history',  name: 'trek-history',   component: TrekHistory },
      { path: 'profile',  name: 'user-profile',   component: UserProfile },
    ],
  },

  // Catch-all
  { path: '/:pathMatch(.*)*', redirect: '/' },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior: () => ({ top: 0 }),
})

// Navigation guard
router.beforeEach((to, from, next) => {
  const auth = useAuthStore()

  if (to.meta.requiresAuth) {
    if (!auth.isLoggedIn) return next('/login')
    if (to.meta.role && auth.user?.role !== to.meta.role) {
      // Redirect to correct dashboard
      if (auth.isAdmin)   return next('/admin')
      if (auth.isStaff)   return next('/staff')
      if (auth.isTrekker) return next('/dashboard')
      return next('/login')
    }
  }

  // Already logged in — don't show login/register
  if ((to.name === 'login' || to.name === 'register') && auth.isLoggedIn) {
    if (auth.isAdmin)   return next('/admin')
    if (auth.isStaff)   return next('/staff')
    if (auth.isTrekker) return next('/dashboard')
  }

  next()
})

export default router

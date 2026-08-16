import api from './client'

// ── Auth ──────────────────────────────────────────────────────────
export const authAPI = {
  login:    (data) => api.post('/auth/login', data),
  register: (data) => api.post('/auth/register', data),
  me:       ()     => api.get('/auth/me'),
  refresh:  ()     => api.post('/auth/refresh'),
  updateProfile: (data) => api.put('/auth/profile', data),
}

// ── Treks (public) ────────────────────────────────────────────────
export const treksAPI = {
  list:       (params) => api.get('/treks/', { params }),
  get:        (id)     => api.get(`/treks/${id}`),
  categories: ()       => api.get('/treks/categories'),
  states:     ()       => api.get('/treks/states'),
  reviews:    (id)     => api.get(`/treks/${id}/reviews`),
}

// ── Admin ─────────────────────────────────────────────────────────
export const adminAPI = {
  dashboard:  ()             => api.get('/admin/dashboard'),

  listTreks:  (params)       => api.get('/admin/treks', { params }),
  createTrek: (data)         => api.post('/admin/treks', data),
  updateTrek: (id, data)     => api.put(`/admin/treks/${id}`, data),
  deleteTrek: (id)           => api.delete(`/admin/treks/${id}`),

  listStaff:      (params)   => api.get('/admin/staff', { params }),
  createStaff:    (data)     => api.post('/admin/staff', data),
  blacklistStaff: (id)       => api.post(`/admin/staff/${id}/blacklist`),
  whitelistStaff: (id)       => api.post(`/admin/staff/${id}/whitelist`),

  listUsers:      (params)   => api.get('/admin/users', { params }),
  blacklistUser:  (id)       => api.post(`/admin/users/${id}/blacklist`),
  whitelistUser:  (id)       => api.post(`/admin/users/${id}/whitelist`),

  listBookings:   (params)   => api.get('/admin/bookings', { params }),

  listRestaurants: (params)  => api.get('/restaurants/', { params }),
  approveRestaurant: (id)    => api.post(`/restaurants/${id}/approve`),
  rejectRestaurant:  (id)    => api.post(`/restaurants/${id}/reject`),
  deleteRestaurant:  (id)    => api.delete(`/restaurants/${id}`),

  listAgencies:   (params)   => api.get('/agencies/', { params }),
  approveAgency:  (id)       => api.post(`/agencies/${id}/approve`),
  rejectAgency:   (id)       => api.post(`/agencies/${id}/reject`),
  deleteAgency:   (id)       => api.delete(`/agencies/${id}`),

  exportBookings:         () => api.post('/admin/export-bookings'),
  triggerDailyReminders:  () => api.post('/admin/trigger-daily-reminders'),
  triggerMonthlyReport:   () => api.post('/admin/trigger-monthly-report'),
}

// ── Staff ─────────────────────────────────────────────────────────
export const staffAPI = {
  dashboard:       ()             => api.get('/staff/dashboard'),
  myTreks:         ()             => api.get('/staff/treks'),
  getTrek:         (id)           => api.get(`/staff/treks/${id}`),
  updateTrek:      (id, data)     => api.put(`/staff/treks/${id}`, data),
  completeTrek:    (id)           => api.post(`/staff/treks/${id}/complete`),
  participants:    (id)           => api.get(`/staff/treks/${id}/participants`),
  allParticipants: ()             => api.get('/staff/participants'),
  profile:         ()             => api.get('/staff/profile'),
}

// ── User / Trekker ────────────────────────────────────────────────
export const userAPI = {
  dashboard:     ()          => api.get('/user/dashboard'),
  myBookings:    (params)    => api.get('/user/bookings', { params }),
  bookTrek:      (data)      => api.post('/user/bookings', typeof data === 'object' ? data : { trek_id: data }),
  cancelBooking: (id, data)  => api.post(`/user/bookings/${id}/cancel`, data),
  history:       (params)    => api.get('/user/history', { params }),
  exportHistory: ()          => api.post('/user/export-history'),
  profile:       ()          => api.get('/user/profile'),
  submitReview:  (bookingId, data) => api.post(`/user/bookings/${bookingId}/review`, data),
}

// ── Restaurants ───────────────────────────────────────────────────
export const restaurantsAPI = {
  list:     (params) => api.get('/restaurants/', { params }),
  get:      (id)     => api.get(`/restaurants/${id}`),
  register: (data)   => api.post('/restaurants/', data),
}

// ── Agencies ──────────────────────────────────────────────────────
export const agenciesAPI = {
  list:     (params) => api.get('/agencies/', { params }),
  get:      (id)     => api.get(`/agencies/${id}`),
  register: (data)   => api.post('/agencies/', data),
}

// ── Food ──────────────────────────────────────────────────────────
export const foodAPI = {
  list:      (params)  => api.get('/food/', { params }),
  byRegion:  (region)  => api.get(`/food/region/${region}`),
}

# Jatayu (जटायु) - Trekking Management Application V2

> India's trekking soul. A culture-first trekking management platform built for Modern Application Development II (IIT Madras BS Degree).

Jatayu satisfies the full MAD-II Trekking Management Application V2 specification while layering in India-specific cultural depth: mythology, regional food trails, local restaurant partners, and travel agency integrations.

---

## 🛠️ Tech Stack

| Layer | Technology |
| :--- | :--- |
| **Backend** | Flask (REST API) |
| **Frontend** | VueJS 3 + Vite + Bootstrap 5 |
| **Database** | SQLite via SQLAlchemy ORM (code-created) |
| **Caching** | Redis (Flask-Caching) |
| **Jobs** | Celery + Redis broker, Celery Beat |
| **Auth** | JWT (Flask-JWT-Extended), role-based access |

---

## 📂 Project Structure

```text
jatayu/
├── backend/
│   ├── app/
│   │   ├── models/        # User, Trek, Booking, Restaurant, LocalFood, TravelAgency
│   │   ├── api/           # auth, admin, staff, user, treks, restaurants, agencies, food
│   │   ├── jobs/          # Celery tasks + beat schedule
│   │   └── utils/         # Auth decorators
│   ├── seed.py            # Creates admin + sample India treks/food/partners
│   └── run.py
└── frontend/
    └── src/
        ├── api/            # Axios client + all API calls
        ├── store/          # Pinia auth store
        ├── router/         # Vue Router with role guards
        └── views/          # All 12 wireframe screens + public pages
```

---

## 🚀 Setup & Installation

### Backend Setup
1. **Navigate to backend and create virtual environment**:
   ```bash
   cd backend
   python -m venv venv
   ```
2. **Activate the environment**:
   - Windows:
     ```bash
     venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source venv/bin/activate
     ```
3. **Install dependencies and configure environment**:
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   ```
4. **Seed database and run Flask backend**:
   ```bash
   python seed.py                   # Creates admin credentials + sample Indian treks/food/partners
   python run.py                    # Runs server on http://localhost:5000
   ```

* **Default Admin Credentials**: `admin@jatayu.in` / `Admin@123`

### Redis & Celery (Required for Background Jobs)
Make sure Redis server is running, then start the Celery worker and scheduler in separate terminals:
```bash
# Terminal 1: Start Redis
redis-server

# Terminal 2: Start Celery Worker
celery -A app.jobs.tasks worker --loglevel=info

# Terminal 3: Start Celery Beat Scheduler
celery -A app.jobs.tasks beat --loglevel=info
```

### Frontend Setup
1. **Navigate to frontend and install node packages**:
   ```bash
   cd frontend
   npm install
   ```
2. **Run Vue local server**:
   ```bash
   npm run dev          # Runs on http://localhost:5173, proxies /api to Flask backend
   ```

---

## 👥 Access Roles

| Role | Created By | Capabilities |
| :--- | :--- | :--- |
| **Admin** | `seed.py` (pre-created) | Full CRUD on treks, staff, and users; approve regional partners |
| **Staff** | Admin | Manage assigned treks, operational slots, and track participants |
| **Trekker** | Self-Registration | Browse treks, book slots, cancel bookings, view history, and export CSV reports |

---

## 📌 Specification Milestone Tracker

| # | Milestone | Status |
| :---: | :--- | :---: |
| 0 | GitHub Repository Setup | ✅ |
| 1 | Database Models and Schema | ✅ |
| 2 | Authentication and Role-Based Access | ✅ |
| 3 | Admin Dashboard and Management | ✅ |
| 4 | Trek Staff Dashboard and Trek Operations | ✅ |
| 5 | User Dashboard and Trek Booking System | ✅ |
| 6 | Trek Booking History and Status Tracking | ✅ |
| 7 | Backend Asynchronous Jobs (Reminders, Reports, CSV export) | ✅ |
| 8 | API Performance Optimization (Redis caching) | ✅ |

---

## ✨ Jatayu Extras (Beyond the Spec)

- **Cultural Trek Profiles**: Integrates mythology, local tribes, regional festivals, and the best seasons for each Indian trek.
- **Local Food Trails**: Showcases traditional regional dishes (like Siddu, Kafuli, Axone, etc.) mapped directly to each trek's geographic region.
- **Restaurant Partners**: Integrates verified local dhabas and homestays serving traditional food near the trailheads.
- **Travel Agency Partners**: Recommends regional transport, accommodation, and full-package local agency partners.
- **Region-Mapped Dark UI**: Implements a distinct CSS theme and color identity matching each trek category (Snow, Pilgrimage, Northeast, and Heritage).

---

## 📖 API Reference

All backend API endpoints are prefixed with `/api`.
Key endpoints:
- `POST /api/auth/login` / `POST /api/auth/register` — User authentication.
- `GET /api/treks/` — List all treks with search and filters.
- `GET /api/treks/:id` — Trek details containing mapped local food trail, restaurants, and agencies.
- `GET /api/user/bookings` — Fetch booking history for the logged-in user.

---

## 🤖 AI Usage Declaration

This project was built with AI assistance (Claude) for content architecture planning, UI/UX design, and modular helper functions. All core logical flows, databases, caching layers, and background tasks were implemented, reviewed, and tested manually.

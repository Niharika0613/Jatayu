from datetime import datetime
from .. import db


class Trek(db.Model):
    __tablename__ = "treks"

    id = db.Column(db.Integer, primary_key=True)

    # ── Required by doc + wireframe (screens 4, 9, 10, 11) ────────
    name = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(150), nullable=False)

    # 'Easy' | 'Moderate' | 'Hard'
    difficulty = db.Column(db.String(20), nullable=False)

    duration_days = db.Column(db.Integer, nullable=False)
    total_slots = db.Column(db.Integer, nullable=False)
    available_slots = db.Column(db.Integer, nullable=False)

    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)

    # FK to User with role='staff'
    staff_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=True)

    # 'Pending' | 'Approved' | 'Open' | 'Closed' | 'Completed'
    status = db.Column(db.String(20), nullable=False, default="Pending")

    # ── Jatayu: India cultural layer ───────────────────────────────
    # 'Pilgrimage' | 'Snow' | 'Northeast' | 'Tribal' | 'Heritage' |
    # 'Monsoon' | 'Wildlife' | 'General'
    category = db.Column(db.String(40), nullable=True, default="General")

    state = db.Column(db.String(60), nullable=True)
    region = db.Column(db.String(60), nullable=True)

    max_altitude_m = db.Column(db.Integer, nullable=True)
    nearest_railhead = db.Column(db.String(100), nullable=True)

    # Y/N — triggers permit info display on frontend
    permit_required = db.Column(db.Boolean, default=False)
    permit_info = db.Column(db.Text, nullable=True)

    # e.g. "October-November, March-April"
    best_season = db.Column(db.String(100), nullable=True)

    mythological_significance = db.Column(db.Text, nullable=True)
    cultural_notes = db.Column(db.Text, nullable=True)

    # Comma-separated local languages / tribal groups
    local_tribe_culture = db.Column(db.String(200), nullable=True)

    # Seasonal festivals along route
    festivals_enroute = db.Column(db.String(300), nullable=True)

    # Trek description / highlights
    description = db.Column(db.Text, nullable=True)

    # Hidden places / offbeat spots en route
    hidden_places = db.Column(db.Text, nullable=True)

    # Cover image path or URL
    cover_image = db.Column(db.String(300), nullable=True)

    # Price in INR (optional, for payment simulation)
    price_inr = db.Column(db.Float, nullable=True, default=0.0)

    # Route specs (from AllTrails features)
    route_type = db.Column(db.String(80), nullable=True, default="Out-and-Back")
    elevation_gain_m = db.Column(db.Integer, nullable=True, default=500)
    elevation_profile = db.Column(db.Text, nullable=True)

    # Komoot specs
    itinerary = db.Column(db.Text, nullable=True)
    safety_alerts = db.Column(db.Text, nullable=True)
    terrain_breakdown = db.Column(db.String(300), nullable=True)

    # ── Timestamps ─────────────────────────────────────────────────
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ── Relationships ───────────────────────────────────────────────
    bookings = db.relationship("Booking", backref="trek", lazy=True)
    reviews = db.relationship("Review", backref="trek", lazy=True, cascade="all, delete-orphan")

    def slots_left(self):
        return self.available_slots

    def is_bookable(self):
        return self.status == "Open" and self.available_slots > 0

    @property
    def avg_rating(self):
        if not self.reviews:
            return 0.0
        return round(sum(r.rating for r in self.reviews) / len(self.reviews), 1)

    @property
    def total_reviews(self):
        return len(self.reviews)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "location": self.location,
            "difficulty": self.difficulty,
            "duration_days": self.duration_days,
            "total_slots": self.total_slots,
            "available_slots": self.available_slots,
            "start_date": self.start_date.isoformat() if self.start_date else None,
            "end_date": self.end_date.isoformat() if self.end_date else None,
            "staff_id": self.staff_id,
            "status": self.status,
            "is_bookable": self.is_bookable(),
            # Jatayu fields
            "category": self.category,
            "state": self.state,
            "region": self.region,
            "max_altitude_m": self.max_altitude_m,
            "nearest_railhead": self.nearest_railhead,
            "permit_required": self.permit_required,
            "permit_info": self.permit_info,
            "best_season": self.best_season,
            "mythological_significance": self.mythological_significance,
            "cultural_notes": self.cultural_notes,
            "local_tribe_culture": self.local_tribe_culture,
            "festivals_enroute": self.festivals_enroute,
            "description": self.description,
            "hidden_places": self.hidden_places,
            "cover_image": self.cover_image,
            "price_inr": self.price_inr,
            "route_type": self.route_type,
            "elevation_gain_m": self.elevation_gain_m,
            "elevation_profile": self.elevation_profile,
            "itinerary": self.itinerary,
            "safety_alerts": self.safety_alerts,
            "terrain_breakdown": self.terrain_breakdown,
            "avg_rating": self.avg_rating,
            "total_reviews": self.total_reviews,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Trek {self.name} [{self.status}]>"

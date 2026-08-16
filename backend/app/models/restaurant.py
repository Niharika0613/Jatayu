from datetime import datetime
from .. import db


class Restaurant(db.Model):
    __tablename__ = "restaurants"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    owner_name = db.Column(db.String(120), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)

    # Location
    address = db.Column(db.String(300), nullable=True)
    village = db.Column(db.String(100), nullable=True)
    region = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(60), nullable=False)
    distance_from_trailhead_km = db.Column(db.Float, nullable=True)
    google_maps_link = db.Column(db.String(500), nullable=True)
    latitude = db.Column(db.Float, nullable=True)
    longitude = db.Column(db.Float, nullable=True)

    # Type: 'dhaba' | 'homestay_kitchen' | 'cafe' | 'tea_stall' | 'restaurant'
    type = db.Column(db.String(40), nullable=True, default="dhaba")

    # Open season e.g. "October to June"
    open_season = db.Column(db.String(100), nullable=True)

    # Payment
    accepts_upi = db.Column(db.Boolean, default=True)
    accepts_cash = db.Column(db.Boolean, default=True)

    # Media
    cover_photo = db.Column(db.String(300), nullable=True)
    photos = db.Column(db.Text, nullable=True)  # JSON list of URLs

    description = db.Column(db.Text, nullable=True)
    speciality = db.Column(db.String(300), nullable=True)

    # Admin approval
    # 'pending' | 'approved' | 'rejected' | 'suspended'
    status = db.Column(db.String(20), nullable=False, default="pending")
    is_verified = db.Column(db.Boolean, default=False)

    # Monthly listing fee paid
    listing_fee_paid = db.Column(db.Boolean, default=False)

    avg_rating = db.Column(db.Float, nullable=True, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    food_items = db.relationship("LocalFood", backref="restaurant", lazy=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_name": self.owner_name,
            "contact_number": self.contact_number,
            "email": self.email,
            "address": self.address,
            "village": self.village,
            "region": self.region,
            "state": self.state,
            "distance_from_trailhead_km": self.distance_from_trailhead_km,
            "google_maps_link": self.google_maps_link,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "type": self.type,
            "open_season": self.open_season,
            "accepts_upi": self.accepts_upi,
            "accepts_cash": self.accepts_cash,
            "cover_photo": self.cover_photo,
            "description": self.description,
            "speciality": self.speciality,
            "status": self.status,
            "is_verified": self.is_verified,
            "avg_rating": self.avg_rating,
            "total_reviews": self.total_reviews,
            "food_items": [f.to_dict() for f in self.food_items],
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<Restaurant {self.name} [{self.region}]>"

from datetime import datetime
from .. import db


class Booking(db.Model):
    __tablename__ = "bookings"

    id = db.Column(db.Integer, primary_key=True)

    # ── Core fields (doc + wireframe) ──────────────────────────────
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    travel_agency_id = db.Column(db.Integer, db.ForeignKey("travel_agencies.id"), nullable=True)

    # Relationship
    travel_agency = db.relationship("TravelAgency", backref="bookings")

    booking_date = db.Column(db.DateTime, default=datetime.utcnow)

    # 'Booked' | 'Cancelled' | 'Completed'
    status = db.Column(db.String(20), nullable=False, default="Booked")

    # ── Optional payment simulation ────────────────────────────────
    # 'Pending' | 'Paid' | 'Refunded' | 'Failed'
    payment_status = db.Column(db.String(20), nullable=True, default="Pending")
    amount_paid = db.Column(db.Float, nullable=True, default=0.0)
    # 'UPI' | 'Card' | 'NetBanking' | 'Simulated'
    payment_method = db.Column(db.String(30), nullable=True)

    # ── Jatayu extras ──────────────────────────────────────────────
    # Badge earned after trek completion
    badge_earned = db.Column(db.String(100), nullable=True)

    # When was the booking confirmed / cancelled
    confirmed_at = db.Column(db.DateTime, nullable=True)
    cancelled_at = db.Column(db.DateTime, nullable=True)
    cancellation_reason = db.Column(db.String(300), nullable=True)

    # Timestamps
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ── Unique constraint: no duplicate bookings per user per trek ──
    __table_args__ = (
        db.UniqueConstraint("user_id", "trek_id", name="unique_user_trek_booking"),
    )

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trek_id": self.trek_id,
            "booking_date": self.booking_date.isoformat() if self.booking_date else None,
            "status": self.status,
            "payment_status": self.payment_status,
            "amount_paid": self.amount_paid,
            "payment_method": self.payment_method,
            "badge_earned": self.badge_earned,
            "confirmed_at": self.confirmed_at.isoformat() if self.confirmed_at else None,
            "cancelled_at": self.cancelled_at.isoformat() if self.cancelled_at else None,
            "cancellation_reason": self.cancellation_reason,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            # Joined fields (populated in API layer)
            "trek_name": self.trek.name if self.trek else None,
            "trek_location": self.trek.location if self.trek else None,
            "trek_start_date": self.trek.start_date.isoformat() if self.trek and self.trek.start_date else None,
            "trek_end_date": self.trek.end_date.isoformat() if self.trek and self.trek.end_date else None,
            "trekker_name": self.trekker.full_name if self.trekker else None,
            "trekker_email": self.trekker.email if self.trekker else None,
            "travel_agency_id": self.travel_agency_id,
            "travel_agency_name": self.travel_agency.name if self.travel_agency else "Self Guided",
        }

    def __repr__(self):
        return f"<Booking user={self.user_id} trek={self.trek_id} [{self.status}]>"

from datetime import datetime
from .. import db


class Review(db.Model):
    __tablename__ = "reviews"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    trek_id = db.Column(db.Integer, db.ForeignKey("treks.id"), nullable=False)
    booking_id = db.Column(db.Integer, db.ForeignKey("bookings.id"), nullable=False)

    rating = db.Column(db.Integer, nullable=False)  # 1 to 5 stars
    comment = db.Column(db.Text, nullable=True)

    # Condition tags e.g. "Snowy, Muddy, Clear"
    trail_condition = db.Column(db.String(100), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    user = db.relationship("User", backref="reviews")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "trek_id": self.trek_id,
            "booking_id": self.booking_id,
            "rating": self.rating,
            "comment": self.comment,
            "trail_condition": self.trail_condition,
            "reviewer_name": self.user.full_name if self.user else "Anonymous",
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

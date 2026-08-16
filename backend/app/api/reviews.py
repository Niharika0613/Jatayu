from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from datetime import datetime
from .. import db
from ..models import Booking, Review, Trek
from ..utils.auth import trekker_required, get_current_user

reviews_bp = Blueprint("reviews", __name__)


@reviews_bp.route("/user/bookings/<int:booking_id>/review", methods=["POST"])
@trekker_required
def create_review(booking_id):
    """Submit a verified review for a booking."""
    user = get_current_user()
    booking = Booking.query.get_or_404(booking_id)

    # 1. Security Check: Must be the user's booking
    if booking.user_id != user.id:
        return jsonify({"error": "Unauthorized"}), 403

    # 2. Check if booking is cancelled
    if booking.status == "Cancelled":
        return jsonify({"error": "Cannot review a cancelled booking"}), 400

    # 3. Check for duplicates
    existing = Review.query.filter_by(booking_id=booking_id).first()
    if existing:
        return jsonify({"error": "You have already reviewed this booking"}), 400

    data = request.get_json() or {}
    rating = data.get("rating")
    comment = data.get("comment", "")
    trail_condition = data.get("trail_condition", "")

    # Validation
    if not rating or not (1 <= int(rating) <= 5):
        return jsonify({"error": "Rating is required and must be between 1 and 5"}), 400

    review = Review(
        user_id=user.id,
        trek_id=booking.trek_id,
        booking_id=booking.id,
        rating=int(rating),
        comment=comment,
        trail_condition=trail_condition,
        created_at=datetime.utcnow()
    )

    db.session.add(review)
    db.session.commit()

    return jsonify({
        "message": "Review submitted successfully!",
        "review": review.to_dict()
    }), 201


@reviews_bp.route("/treks/<int:trek_id>/reviews", methods=["GET"])
def list_reviews(trek_id):
    """Get all reviews for a specific trek."""
    trek = Trek.query.get_or_404(trek_id)
    reviews = Review.query.filter_by(trek_id=trek_id).order_by(Review.created_at.desc()).all()

    return jsonify({
        "reviews": [r.to_dict() for r in reviews]
    }), 200

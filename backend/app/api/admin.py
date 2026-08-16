from flask import Blueprint, request, jsonify
from .. import db, cache
from ..models import User, Trek, Booking
from ..utils.auth import admin_required, hash_password

admin_bp = Blueprint("admin", __name__)


# ── Dashboard ──────────────────────────────────────────────────────

@admin_bp.route("/dashboard", methods=["GET"])
@admin_required
def dashboard():
    total_treks = Trek.query.count()
    total_users = User.query.filter_by(role="trekker").count()
    total_staff = User.query.filter_by(role="staff").count()
    total_bookings = Booking.query.count()

    recent_bookings = (
        Booking.query
        .order_by(Booking.created_at.desc())
        .limit(10)
        .all()
    )

    # Analytics for ChartJS
    popular_query = db.session.execute(
        db.text("""
            SELECT t.name, COUNT(b.id) as count
            FROM treks t
            LEFT JOIN bookings b ON t.id = b.trek_id
            GROUP BY t.id, t.name
            ORDER BY count DESC
            LIMIT 5
        """)
    ).fetchall()
    popular_treks = [{"name": row[0], "count": row[1]} for row in popular_query]

    category_query = db.session.execute(
        db.text("""
            SELECT t.category, COUNT(b.id) as count
            FROM treks t
            JOIN bookings b ON t.id = b.trek_id
            GROUP BY t.category
            ORDER BY count DESC
        """)
    ).fetchall()
    category_distribution = [{"category": row[0] or "General", "count": row[1]} for row in category_query]

    return jsonify({
        "stats": {
            "total_treks": total_treks,
            "total_users": total_users,
            "total_staff": total_staff,
            "total_bookings": total_bookings,
        },
        "recent_bookings": [b.to_dict() for b in recent_bookings],
        "analytics": {
            "popular_treks": popular_treks,
            "category_distribution": category_distribution,
        }
    }), 200


# ── Trek Management ────────────────────────────────────────────────

@admin_bp.route("/treks", methods=["GET"])
@admin_required
def list_treks():
    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = Trek.query
    if q:
        query = query.filter(
            Trek.name.ilike(f"%{q}%") |
            Trek.location.ilike(f"%{q}%")
        )

    pagination = query.order_by(Trek.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "treks": [t.to_dict() for t in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@admin_bp.route("/treks", methods=["POST"])
@admin_required
def create_trek():
    data = request.get_json() or {}

    required = ["name", "location", "difficulty", "duration_days",
                "total_slots", "start_date", "end_date"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"{f} is required"}), 400

    from datetime import date as dt_date
    trek = Trek(
        name=data["name"],
        location=data["location"],
        difficulty=data["difficulty"],
        duration_days=int(data["duration_days"]),
        total_slots=int(data["total_slots"]),
        available_slots=int(data.get("available_slots", data["total_slots"])),
        start_date=dt_date.fromisoformat(data["start_date"]),
        end_date=dt_date.fromisoformat(data["end_date"]),
        staff_id=data.get("staff_id"),
        status=data.get("status", "Pending"),
        # Jatayu extras
        category=data.get("category", "General"),
        state=data.get("state"),
        region=data.get("region"),
        max_altitude_m=data.get("max_altitude_m"),
        nearest_railhead=data.get("nearest_railhead"),
        permit_required=data.get("permit_required", False),
        permit_info=data.get("permit_info"),
        best_season=data.get("best_season"),
        mythological_significance=data.get("mythological_significance"),
        cultural_notes=data.get("cultural_notes"),
        local_tribe_culture=data.get("local_tribe_culture"),
        festivals_enroute=data.get("festivals_enroute"),
        description=data.get("description"),
        cover_image=data.get("cover_image"),
        price_inr=data.get("price_inr", 0.0),
    )

    db.session.add(trek)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Trek created", "trek": trek.to_dict()}), 201


@admin_bp.route("/treks/<int:trek_id>", methods=["PUT"])
@admin_required
def update_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    data = request.get_json() or {}

    updatable = [
        "name", "location", "difficulty", "duration_days", "total_slots",
        "available_slots", "staff_id", "status", "category", "state",
        "region", "max_altitude_m", "nearest_railhead", "permit_required",
        "permit_info", "best_season", "mythological_significance",
        "cultural_notes", "local_tribe_culture", "festivals_enroute",
        "description", "cover_image", "price_inr",
    ]
    date_fields = ["start_date", "end_date"]

    for field in updatable:
        if field in data:
            setattr(trek, field, data[field])

    from datetime import date as dt_date
    for field in date_fields:
        if field in data:
            setattr(trek, field, dt_date.fromisoformat(data[field]))

    db.session.commit()
    cache.clear()
    return jsonify({"message": "Trek updated", "trek": trek.to_dict()}), 200


@admin_bp.route("/treks/<int:trek_id>", methods=["DELETE"])
@admin_required
def delete_trek(trek_id):
    trek = Trek.query.get_or_404(trek_id)
    db.session.delete(trek)
    db.session.commit()
    cache.clear()
    return jsonify({"message": "Trek deleted"}), 200


# ── Staff Management ───────────────────────────────────────────────

@admin_bp.route("/staff", methods=["GET"])
@admin_required
def list_staff():
    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = User.query.filter_by(role="staff")
    if q:
        query = query.filter(
            User.full_name.ilike(f"%{q}%") |
            User.email.ilike(f"%{q}%")
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "staff": [s.to_dict() for s in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@admin_bp.route("/staff", methods=["POST"])
@admin_required
def create_staff():
    data = request.get_json() or {}

    required = ["full_name", "email", "password", "confirm_password", "contact_number"]
    for f in required:
        if not data.get(f):
            return jsonify({"error": f"{f} is required"}), 400

    if data["password"] != data["confirm_password"]:
        return jsonify({"error": "Passwords do not match"}), 400

    email = data["email"].strip().lower()
    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already registered"}), 409

    staff = User(
        role="staff",
        full_name=data["full_name"].strip(),
        email=email,
        password_hash=hash_password(data["password"]),
        contact_number=data.get("contact_number", "").strip(),
        status="active",
        is_active=True,
        specialization=data.get("specialization"),
        experience_years=data.get("experience_years"),
        languages_spoken=data.get("languages_spoken"),
        regions_expertise=data.get("regions_expertise"),
        certifications=data.get("certifications"),
    )

    db.session.add(staff)
    db.session.commit()
    return jsonify({"message": "Staff created. Credentials sent via email.", "staff": staff.to_dict()}), 201


@admin_bp.route("/staff/<int:staff_id>/blacklist", methods=["POST"])
@admin_required
def blacklist_staff(staff_id):
    staff = User.query.filter_by(id=staff_id, role="staff").first_or_404()
    staff.status = "blacklisted"
    staff.is_active = False
    db.session.commit()
    return jsonify({"message": f"{staff.full_name} has been blacklisted"}), 200


@admin_bp.route("/staff/<int:staff_id>/whitelist", methods=["POST"])
@admin_required
def whitelist_staff(staff_id):
    staff = User.query.filter_by(id=staff_id, role="staff").first_or_404()
    staff.status = "active"
    staff.is_active = True
    db.session.commit()
    return jsonify({"message": f"{staff.full_name} has been reinstated"}), 200


# ── User Management ────────────────────────────────────────────────

@admin_bp.route("/users", methods=["GET"])
@admin_required
def list_users():
    q = request.args.get("q", "")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))

    query = User.query.filter_by(role="trekker")
    if q:
        query = query.filter(
            User.full_name.ilike(f"%{q}%") |
            User.email.ilike(f"%{q}%")
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    return jsonify({
        "users": [u.to_dict() for u in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@admin_bp.route("/users/<int:user_id>/blacklist", methods=["POST"])
@admin_required
def blacklist_user(user_id):
    user = User.query.filter_by(id=user_id, role="trekker").first_or_404()
    user.status = "blacklisted"
    user.is_active = False
    db.session.commit()
    return jsonify({"message": f"{user.full_name} has been blacklisted"}), 200


@admin_bp.route("/users/<int:user_id>/whitelist", methods=["POST"])
@admin_required
def whitelist_user(user_id):
    user = User.query.filter_by(id=user_id, role="trekker").first_or_404()
    user.status = "active"
    user.is_active = True
    db.session.commit()
    return jsonify({"message": f"{user.full_name} has been reinstated"}), 200


# ── Bookings ───────────────────────────────────────────────────────

@admin_bp.route("/bookings", methods=["GET"])
@admin_required
def list_bookings():
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 10))
    pagination = Booking.query.order_by(Booking.created_at.desc()).paginate(
        page=page, per_page=per_page, error_out=False
    )
    return jsonify({
        "bookings": [b.to_dict() for b in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@admin_bp.route("/trigger-daily-reminders", methods=["POST"])
@admin_required
def trigger_daily_reminders():
    from ..jobs.tasks import send_daily_reminders
    task = send_daily_reminders.delay()
    return jsonify({"message": "Daily reminders queued via Celery", "task_id": task.id}), 200


@admin_bp.route("/trigger-monthly-report", methods=["POST"])
@admin_required
def trigger_monthly_report():
    from ..jobs.tasks import send_monthly_admin_report
    task = send_monthly_admin_report.delay()
    return jsonify({"message": "Monthly report queued via Celery", "task_id": task.id}), 200


@admin_bp.route("/export-bookings", methods=["POST"])
@admin_required
def export_bookings():
    """Trigger async CSV export of all bookings via Celery."""
    from ..jobs.tasks import export_all_bookings_csv
    task = export_all_bookings_csv.delay()
    return jsonify({
        "message": "All bookings export started successfully.",
        "task_id": task.id
    }), 202


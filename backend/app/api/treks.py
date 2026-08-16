from flask import Blueprint, request, jsonify
from .. import cache
from ..models import Trek, Restaurant, TravelAgency, LocalFood

treks_bp = Blueprint("treks", __name__)


@treks_bp.route("/", methods=["GET"])
@cache.cached(timeout=120, query_string=True)
def list_treks():
    """Public — browse and filter all open treks."""
    q = request.args.get("q", "")
    difficulty = request.args.get("difficulty", "")
    category = request.args.get("category", "")
    state = request.args.get("state", "")
    season = request.args.get("season", "")
    status = request.args.get("status", "Open")
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))

    query = Trek.query

    if status:
        query = query.filter(Trek.status == status)
    if q:
        query = query.filter(
            Trek.name.ilike(f"%{q}%") |
            Trek.location.ilike(f"%{q}%") |
            Trek.state.ilike(f"%{q}%")
        )
    if difficulty:
        query = query.filter(Trek.difficulty == difficulty)
    if category:
        query = query.filter(Trek.category == category)
    if state:
        query = query.filter(Trek.state.ilike(f"%{state}%"))
    if season:
        if season == "winter":
            query = query.filter(Trek.best_season.ilike("%winter%"))
        elif season == "monsoon":
            query = query.filter(Trek.best_season.ilike("%monsoon%"))
        elif season == "summer":
            query = query.filter(Trek.best_season.ilike("%summer%"))
        elif season == "autumn":
            query = query.filter(Trek.best_season.ilike("%autumn%") | Trek.best_season.ilike("%post-monsoon%"))

    pagination = query.order_by(Trek.start_date.asc()).paginate(
        page=page, per_page=per_page, error_out=False
    )

    return jsonify({
        "treks": [t.to_dict() for t in pagination.items],
        "total": pagination.total,
        "pages": pagination.pages,
        "page": page,
    }), 200


@treks_bp.route("/<int:trek_id>", methods=["GET"])
@cache.cached(timeout=180)
def get_trek(trek_id):
    """Full trek detail — includes food, restaurants, agencies for that region."""
    trek = Trek.query.get_or_404(trek_id)

    # Fetch regional food
    food = LocalFood.query.filter_by(trek_region=trek.region).all()
    if not food:
        food = LocalFood.query.filter_by(state=trek.state).all()

    # Fetch nearby restaurants (same region/state)
    restaurants = Restaurant.query.filter_by(
        status="approved", region=trek.region
    ).all()
    if not restaurants:
        restaurants = Restaurant.query.filter_by(
            status="approved", state=trek.state
        ).limit(4).all()

    # Fetch agencies that cover this region
    agencies = TravelAgency.query.filter(
        TravelAgency.status == "approved",
        TravelAgency.regions_covered.ilike(f"%{trek.region}%")
    ).all()
    if not agencies:
        agencies = TravelAgency.query.filter_by(
            status="approved", state=trek.state
        ).limit(3).all()

    return jsonify({
        "trek": trek.to_dict(),
        "local_food": [f.to_dict() for f in food],
        "restaurants": [r.to_dict() for r in restaurants],
        "agencies": [a.to_dict() for a in agencies],
    }), 200


@treks_bp.route("/categories", methods=["GET"])
@cache.cached(timeout=600)
def categories():
    cats = [
        {"key": "Snow",      "label": "Snow treks",        "emoji": "❄"},
        {"key": "Pilgrimage","label": "Pilgrimage treks",   "emoji": "🪔"},
        {"key": "Northeast", "label": "Northeast India",    "emoji": "🌿"},
        {"key": "Tribal",    "label": "Tribal trails",      "emoji": "🪘"},
        {"key": "Heritage",  "label": "Heritage walks",     "emoji": "🏛"},
        {"key": "Monsoon",   "label": "Monsoon treks",      "emoji": "🌧"},
        {"key": "Wildlife",  "label": "Wildlife treks",     "emoji": "🐾"},
        {"key": "General",   "label": "All treks",          "emoji": "🏔"},
    ]
    return jsonify({"categories": cats}), 200


@treks_bp.route("/states", methods=["GET"])
@cache.cached(timeout=600)
def states():
    rows = Trek.query.with_entities(Trek.state).distinct().all()
    states = sorted([r[0] for r in rows if r[0]])
    return jsonify({"states": states}), 200

from datetime import datetime
from .. import db


class LocalFood(db.Model):
    __tablename__ = "local_food"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(120), nullable=False)
    hindi_name = db.Column(db.String(120), nullable=True)
    local_language_name = db.Column(db.String(120), nullable=True)

    region = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(60), nullable=False)

    # 'bread' | 'curry' | 'dal' | 'rice' | 'sweet' | 'snack' | 'drink' | 'pickle'
    category = db.Column(db.String(40), nullable=True)

    description = db.Column(db.Text, nullable=True)
    cultural_significance = db.Column(db.Text, nullable=True)

    # Best eaten at — free text e.g. "Sankri village homestays, winter mornings"
    best_eaten_at = db.Column(db.String(300), nullable=True)

    # Season: 'year-round' | 'winter' | 'summer' | 'monsoon' | 'festival'
    season = db.Column(db.String(40), nullable=True, default="year-round")

    is_vegetarian = db.Column(db.Boolean, default=True)
    allergens = db.Column(db.String(200), nullable=True)

    # Key ingredients (comma-separated)
    key_ingredients = db.Column(db.String(300), nullable=True)

    photo_url = db.Column(db.String(500), nullable=True)

    # Optional FK to a restaurant that serves this dish
    restaurant_id = db.Column(db.Integer, db.ForeignKey("restaurants.id"), nullable=True)

    # Trek association — which treks show this food
    trek_region = db.Column(db.String(80), nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "hindi_name": self.hindi_name,
            "local_language_name": self.local_language_name,
            "region": self.region,
            "state": self.state,
            "category": self.category,
            "description": self.description,
            "cultural_significance": self.cultural_significance,
            "best_eaten_at": self.best_eaten_at,
            "season": self.season,
            "is_vegetarian": self.is_vegetarian,
            "allergens": self.allergens,
            "key_ingredients": self.key_ingredients,
            "photo_url": self.photo_url,
            "restaurant_id": self.restaurant_id,
            "trek_region": self.trek_region,
        }

    def __repr__(self):
        return f"<LocalFood {self.name} [{self.region}]>"

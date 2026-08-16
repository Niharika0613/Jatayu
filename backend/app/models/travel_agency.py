from datetime import datetime
from .. import db


class TravelAgency(db.Model):
    __tablename__ = "travel_agencies"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(150), nullable=False)
    owner_name = db.Column(db.String(120), nullable=True)
    contact_number = db.Column(db.String(20), nullable=True)
    email = db.Column(db.String(120), nullable=True)
    website = db.Column(db.String(300), nullable=True)

    # Location / operations base
    base_city = db.Column(db.String(80), nullable=True)
    state = db.Column(db.String(60), nullable=False)

    # Regions covered e.g. "Garhwal, Kumaon, Ladakh"
    regions_covered = db.Column(db.String(300), nullable=True)

    # Services: comma-separated
    # 'transport' | 'accommodation' | 'full_package' | 'gear_rental' | 'insurance'
    services = db.Column(db.String(200), nullable=True)

    # Certifications e.g. "IIPT, IMF certified, ATTA member"
    certifications = db.Column(db.String(300), nullable=True)

    year_founded = db.Column(db.Integer, nullable=True)

    # Fleet / capacity
    vehicle_types = db.Column(db.String(200), nullable=True)  # "Tempo Traveller, Innova, Bolero"
    max_group_size = db.Column(db.Integer, nullable=True)

    # Insurance offered
    offers_insurance = db.Column(db.Boolean, default=False)
    insurance_details = db.Column(db.String(300), nullable=True)

    # Pricing tier: 'budget' | 'mid' | 'premium'
    pricing_tier = db.Column(db.String(20), nullable=True)

    # Starting price INR for a standard trek package
    package_starting_price_inr = db.Column(db.Float, nullable=True)

    description = db.Column(db.Text, nullable=True)
    cover_photo = db.Column(db.String(300), nullable=True)

    # Admin approval
    # 'pending' | 'approved' | 'rejected' | 'suspended'
    status = db.Column(db.String(20), nullable=False, default="pending")
    is_verified = db.Column(db.Boolean, default=False)

    avg_rating = db.Column(db.Float, nullable=True, default=0.0)
    total_reviews = db.Column(db.Integer, default=0)

    # Jatayu commission % on packages booked through us
    commission_percent = db.Column(db.Float, nullable=True, default=10.0)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "owner_name": self.owner_name,
            "contact_number": self.contact_number,
            "email": self.email,
            "website": self.website,
            "base_city": self.base_city,
            "state": self.state,
            "regions_covered": self.regions_covered,
            "services": self.services,
            "certifications": self.certifications,
            "year_founded": self.year_founded,
            "vehicle_types": self.vehicle_types,
            "max_group_size": self.max_group_size,
            "offers_insurance": self.offers_insurance,
            "insurance_details": self.insurance_details,
            "pricing_tier": self.pricing_tier,
            "package_starting_price_inr": self.package_starting_price_inr,
            "description": self.description,
            "cover_photo": self.cover_photo,
            "status": self.status,
            "is_verified": self.is_verified,
            "avg_rating": self.avg_rating,
            "total_reviews": self.total_reviews,
            "commission_percent": self.commission_percent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }

    def __repr__(self):
        return f"<TravelAgency {self.name} [{self.state}]>"

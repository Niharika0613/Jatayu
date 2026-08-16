from datetime import datetime
from .. import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    # role: 'admin' | 'staff' | 'trekker'
    role = db.Column(db.String(20), nullable=False, default="trekker")

    # ── Core (wireframe screens 1, 2) ──────────────────────────────
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    contact_number = db.Column(db.String(20), nullable=True)

    # ── Status (wireframe screens 6, 7) ────────────────────────────
    # 'active' | 'blacklisted' | 'inactive'
    status = db.Column(db.String(20), nullable=False, default="active")
    is_active = db.Column(db.Boolean, default=True)

    # ── Staff-only fields (wireframe screen 5) ─────────────────────
    specialization = db.Column(db.String(200), nullable=True)
    experience_years = db.Column(db.Integer, nullable=True)

    # ── Jatayu extras: trekker profile ─────────────────────────────
    state = db.Column(db.String(60), nullable=True)
    home_city = db.Column(db.String(60), nullable=True)
    # 'beginner' | 'intermediate' | 'experienced' | 'expert'
    experience_level = db.Column(db.String(30), nullable=True)
    blood_group = db.Column(db.String(10), nullable=True)
    emergency_contact_name = db.Column(db.String(120), nullable=True)
    emergency_contact_number = db.Column(db.String(20), nullable=True)

    # ── Jatayu extras: staff profile ───────────────────────────────
    languages_spoken = db.Column(db.String(200), nullable=True)
    regions_expertise = db.Column(db.String(200), nullable=True)
    certifications = db.Column(db.String(300), nullable=True)

    # ── Timestamps ─────────────────────────────────────────────────
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # ── Relationships ───────────────────────────────────────────────
    bookings = db.relationship("Booking", backref="trekker", lazy=True,
                               foreign_keys="Booking.user_id")
    assigned_treks = db.relationship("Trek", backref="assigned_staff", lazy=True,
                                     foreign_keys="Trek.staff_id")

    def to_dict(self, include_sensitive=False):
        data = {
            "id": self.id,
            "role": self.role,
            "full_name": self.full_name,
            "email": self.email,
            "contact_number": self.contact_number,
            "status": self.status,
            "is_active": self.is_active,
            "state": self.state,
            "home_city": self.home_city,
            "experience_level": self.experience_level,
            "blood_group": self.blood_group,
            "emergency_contact_name": self.emergency_contact_name,
            "emergency_contact_number": self.emergency_contact_number,
            "specialization": self.specialization,
            "experience_years": self.experience_years,
            "languages_spoken": self.languages_spoken,
            "regions_expertise": self.regions_expertise,
            "certifications": self.certifications,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
        return data

    def __repr__(self):
        return f"<User {self.email} [{self.role}]>"

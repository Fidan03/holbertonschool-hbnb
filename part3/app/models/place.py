from app import db
from app.models.base_model import BaseModel
from app.models.amenity import place_amenity


class Place(BaseModel):
    """Place entity representing a rental property."""
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True,
                              cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary=place_amenity,
                                lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(self, **kwargs):
        """Initialize Place with validation."""
        super().__init__(**kwargs)
        self.validate()

    def validate(self):
        """Validate place attributes."""
        if not self.title or len(self.title) > 100:
            raise ValueError("Title is required and must be at most 100 characters")
        if self.price is None or self.price < 0:
            raise ValueError("Price must be a non-negative value")
        if self.latitude is None or not (-90.0 <= self.latitude <= 90.0):
            raise ValueError("Latitude must be between -90 and 90")
        if self.longitude is None or not (-180.0 <= self.longitude <= 180.0):
            raise ValueError("Longitude must be between -180 and 180")

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        if amenity not in self.amenities:
            self.amenities.append(amenity)

    def to_dict(self):
        """Return a dictionary representation of the place."""
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'owner': self.owner.to_dict() if self.owner else None,
            'amenities': [a.to_dict() for a in self.amenities],
            'reviews': [r.to_dict() for r in self.reviews],
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

from app import db
from app.models.base_model import BaseModel

# Many-to-many association table for Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)


class Amenity(BaseModel):
    """Amenity entity representing a feature available at a place."""
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False)
    description = db.Column(db.String(255), default="")

    def __init__(self, **kwargs):
        """Initialize Amenity with validation."""
        super().__init__(**kwargs)
        self.validate()

    def validate(self):
        """Validate amenity attributes."""
        if not self.name or len(self.name) > 50:
            raise ValueError("Amenity name is required and must be at most 50 characters")
        if self.description and len(self.description) > 255:
            raise ValueError("Description must be at most 255 characters")

    def to_dict(self):
        """Return a dictionary representation of the amenity."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

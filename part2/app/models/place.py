from app.models.base_model import BaseModel


class Place(BaseModel):
    """Place entity representing a rental property."""

    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # User object
        self.reviews = []  # List of Review objects
        self.amenities = []  # List of Amenity objects
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
            'owner_id': self.owner.id,
            'owner': self.owner.to_dict(),
            'amenities': [a.to_dict() for a in self.amenities],
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

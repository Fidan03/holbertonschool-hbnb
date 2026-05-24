from app.models.base_model import BaseModel


class Amenity(BaseModel):
    """Amenity entity representing a feature available at a place."""

    def __init__(self, name, description=""):
        super().__init__()
        self.name = name
        self.description = description
        self.validate()

    def validate(self):
        """Validate amenity attributes."""
        if not self.name or len(self.name) > 50:
            raise ValueError("Amenity name is required and must be at most 50 characters")
        if len(self.description) > 255:
            raise ValueError("Description must be at most 255 characters")

    def to_dict(self):
        """Return a dictionary representation of the amenity."""
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

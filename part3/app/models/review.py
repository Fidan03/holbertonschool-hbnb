from app import db
from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review entity representing a user's review of a place."""
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)

    def __init__(self, **kwargs):
        """Initialize Review with validation."""
        super().__init__(**kwargs)
        self.validate()

    def validate(self):
        """Validate review attributes."""
        if not self.text:
            raise ValueError("Review text is required")
        if self.rating is None or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not self.place_id:
            raise ValueError("Place is required")
        if not self.user_id:
            raise ValueError("User is required")

    def to_dict(self):
        """Return a dictionary representation of the review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user_id,
            'place_id': self.place_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

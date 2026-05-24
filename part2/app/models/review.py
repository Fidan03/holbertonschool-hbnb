from app.models.base_model import BaseModel


class Review(BaseModel):
    """Review entity representing a user's review of a place."""

    def __init__(self, text, rating, place, user):
        super().__init__()
        self.text = text
        self.rating = rating
        self.place = place  # Place object
        self.user = user  # User object
        self.validate()

    def validate(self):
        """Validate review attributes."""
        if not self.text:
            raise ValueError("Review text is required")
        if self.rating is None or not (1 <= self.rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not self.place:
            raise ValueError("Place is required")
        if not self.user:
            raise ValueError("User is required")

    def to_dict(self):
        """Return a dictionary representation of the review."""
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

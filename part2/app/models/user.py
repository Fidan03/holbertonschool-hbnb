import re
from app.models.base_model import BaseModel


class User(BaseModel):
    """User entity representing a registered user."""

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
        self.is_admin = is_admin
        self.places = []  # List of places owned by the user
        self.reviews = []  # List of reviews written by the user
        self.validate()

    def validate(self):
        """Validate user attributes."""
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be at most 50 characters")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be at most 50 characters")
        if not self.email or not self._is_valid_email(self.email):
            raise ValueError("Valid email is required")
        if not self.password or len(self.password) < 1:
            raise ValueError("Password is required")

    @staticmethod
    def _is_valid_email(email):
        """Check if an email address is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def to_dict(self):
        """Return a dictionary representation of the user (without password)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }

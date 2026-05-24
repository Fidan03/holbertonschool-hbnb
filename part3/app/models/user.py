import re
from app import bcrypt, db
from app.models.base_model import BaseModel


class User(BaseModel):
    """User entity representing a registered user."""
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    # Relationships
    places = db.relationship('Place', backref='owner', lazy=True)
    reviews = db.relationship('Review', backref='user', lazy=True)

    def __init__(self, **kwargs):
        """Initialize User with validation."""
        super().__init__(**kwargs)
        if 'password' in kwargs:
            self.hash_password(kwargs['password'])
        self.validate()

    def validate(self):
        """Validate user attributes."""
        if not self.first_name or len(self.first_name) > 50:
            raise ValueError("First name is required and must be at most 50 characters")
        if not self.last_name or len(self.last_name) > 50:
            raise ValueError("Last name is required and must be at most 50 characters")
        if not self.email or not self._is_valid_email(self.email):
            raise ValueError("Valid email is required")

    @staticmethod
    def _is_valid_email(email):
        """Check if an email address is valid."""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the provided password against the stored hash."""
        return bcrypt.check_password_hash(self.password, password)

    def to_dict(self):
        """Return a dictionary representation of the user (without password)."""
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

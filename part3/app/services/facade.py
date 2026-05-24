from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    """Facade class for the HBnB application."""

    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)
        self.amenity_repo = SQLAlchemyRepository(Amenity)

    # ==================== User Operations ====================

    def create_user(self, user_data):
        """Create a new user."""
        existing_user = self.user_repo.get_by_attribute('email', user_data['email'])
        if existing_user:
            raise ValueError("Email already registered")
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID."""
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        """Get a user by email."""
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        """Get all users."""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Update a user."""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Check email uniqueness if email is being updated
        if 'email' in user_data and user_data['email'] != user.email:
            existing = self.user_repo.get_by_attribute('email', user_data['email'])
            if existing:
                raise ValueError("Email already registered")

        # Validate updated data
        if 'first_name' in user_data:
            if not user_data['first_name'] or len(user_data['first_name']) > 50:
                raise ValueError("First name is required and must be at most 50 characters")
        if 'last_name' in user_data:
            if not user_data['last_name'] or len(user_data['last_name']) > 50:
                raise ValueError("Last name is required and must be at most 50 characters")
        if 'email' in user_data:
            if not user_data['email'] or not User._is_valid_email(user_data['email']):
                raise ValueError("Valid email is required")
        if 'password' in user_data:
            from app import bcrypt
            user_data['password'] = bcrypt.generate_password_hash(
                user_data['password']).decode('utf-8')

        return self.user_repo.update(user_id, user_data)

    # ==================== Amenity Operations ====================

    def create_amenity(self, amenity_data):
        """Create a new amenity."""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID."""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities."""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity."""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            if not amenity_data['name'] or len(amenity_data['name']) > 50:
                raise ValueError("Amenity name is required and must be at most 50 characters")

        return self.amenity_repo.update(amenity_id, amenity_data)

    # ==================== Place Operations ====================

    def create_place(self, place_data):
        """Create a new place."""
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # Extract amenity IDs if provided
        amenity_ids = place_data.pop('amenities', [])

        # Validate place data
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )

        # Add amenities to the place
        for amenity_id in amenity_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity:
                place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID."""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places."""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place."""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Validate fields
        if 'title' in place_data:
            if not place_data['title'] or len(place_data['title']) > 100:
                raise ValueError("Title is required and must be at most 100 characters")
        if 'price' in place_data:
            if place_data['price'] is None or place_data['price'] < 0:
                raise ValueError("Price must be a non-negative value")
        if 'latitude' in place_data:
            if not (-90.0 <= place_data['latitude'] <= 90.0):
                raise ValueError("Latitude must be between -90 and 90")
        if 'longitude' in place_data:
            if not (-180.0 <= place_data['longitude'] <= 180.0):
                raise ValueError("Longitude must be between -180 and 180")

        # Handle amenities update
        if 'amenities' in place_data:
            amenity_ids = place_data.pop('amenities')
            place.amenities = []
            for amenity_id in amenity_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.add_amenity(amenity)

        # Remove owner_id from data before update
        place_data.pop('owner_id', None)

        return self.place_repo.update(place_id, place_data)

    # ==================== Review Operations ====================

    def create_review(self, review_data):
        """Create a new review."""
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        # Prevent users from reviewing their own places
        if place.owner_id == review_data['user_id']:
            raise ValueError("You cannot review your own place")

        # Prevent duplicate reviews
        existing_review = Review.query.filter_by(
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        ).first()
        if existing_review:
            raise ValueError("You have already reviewed this place")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            place_id=review_data['place_id'],
            user_id=review_data['user_id']
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID."""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews."""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place."""
        place = self.place_repo.get(place_id)
        if not place:
            raise ValueError("Place not found")
        return place.reviews

    def update_review(self, review_id, review_data):
        """Update a review."""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        if 'text' in review_data:
            if not review_data['text']:
                raise ValueError("Review text is required")
        if 'rating' in review_data:
            if not (1 <= review_data['rating'] <= 5):
                raise ValueError("Rating must be between 1 and 5")

        return self.review_repo.update(review_id, review_data)

    def delete_review(self, review_id):
        """Delete a review."""
        return self.review_repo.delete(review_id)

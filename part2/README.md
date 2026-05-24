# HBnB - Part 2: Implementation

## Project Structure

```
part2/
├── app/
│   ├── __init__.py              # Flask app factory
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── users.py         # User endpoints
│   │       ├── places.py        # Place endpoints
│   │       ├── reviews.py       # Review endpoints
│   │       └── amenities.py     # Amenity endpoints
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py        # Base model with common attributes
│   │   ├── user.py              # User model
│   │   ├── place.py             # Place model
│   │   ├── review.py            # Review model
│   │   └── amenity.py           # Amenity model
│   ├── services/
│   │   ├── __init__.py          # Shared facade instance
│   │   └── facade.py            # HBnB Facade (Business Logic)
│   └── persistence/
│       ├── __init__.py
│       └── repository.py        # In-memory repository
├── tests/
│   ├── __init__.py
│   ├── test_users.py
│   ├── test_amenities.py
│   ├── test_places.py
│   └── test_reviews.py
├── config.py                    # Application configuration
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md
```

## Setup

```bash
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

The application will be available at `http://localhost:5000`.
Swagger documentation is auto-generated at the root URL.

## Running Tests

```bash
python -m pytest tests/ -v
```

## API Endpoints

### Users
- `POST /api/v1/users/` - Create a new user
- `GET /api/v1/users/` - Get all users
- `GET /api/v1/users/<user_id>` - Get user by ID
- `PUT /api/v1/users/<user_id>` - Update user

### Amenities
- `POST /api/v1/amenities/` - Create a new amenity
- `GET /api/v1/amenities/` - Get all amenities
- `GET /api/v1/amenities/<amenity_id>` - Get amenity by ID
- `PUT /api/v1/amenities/<amenity_id>` - Update amenity

### Places
- `POST /api/v1/places/` - Create a new place
- `GET /api/v1/places/` - Get all places
- `GET /api/v1/places/<place_id>` - Get place by ID
- `PUT /api/v1/places/<place_id>` - Update place

### Reviews
- `POST /api/v1/reviews/` - Create a new review
- `GET /api/v1/reviews/` - Get all reviews
- `GET /api/v1/reviews/<review_id>` - Get review by ID
- `PUT /api/v1/reviews/<review_id>` - Update review
- `DELETE /api/v1/reviews/<review_id>` - Delete review
- `GET /api/v1/reviews/places/<place_id>/reviews` - Get reviews for a place

## Architecture

The application follows a **layered architecture** with:

1. **Presentation Layer** (`app/api/`) - Flask-RESTx API endpoints
2. **Business Logic Layer** (`app/models/`, `app/services/`) - Core models and facade
3. **Persistence Layer** (`app/persistence/`) - In-memory repository (to be replaced with SQLAlchemy in Part 3)

Communication between layers is managed through the **Facade pattern** (`HBnBFacade`), which provides a unified interface for the presentation layer to interact with business logic and persistence.

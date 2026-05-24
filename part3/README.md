# HBnB - Part 3: Authentication, Authorization & Database Persistence

## Project Structure

```
part3/
├── app/
│   ├── __init__.py              # Flask app factory with extensions
│   ├── api/
│   │   ├── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       ├── auth.py          # Authentication (login) endpoint
│   │       ├── users.py         # User endpoints (admin-protected)
│   │       ├── places.py        # Place endpoints (auth + ownership)
│   │       ├── reviews.py       # Review endpoints (auth + ownership)
│   │       └── amenities.py     # Amenity endpoints (admin-protected)
│   ├── models/
│   │   ├── __init__.py
│   │   ├── base_model.py        # SQLAlchemy base model
│   │   ├── user.py              # User model with bcrypt hashing
│   │   ├── place.py             # Place model with relationships
│   │   ├── review.py            # Review model with relationships
│   │   └── amenity.py           # Amenity model with M2M relationship
│   ├── services/
│   │   ├── __init__.py          # Shared facade instance
│   │   └── facade.py            # HBnB Facade (Business Logic)
│   └── persistence/
│       ├── __init__.py
│       └── repository.py        # Repository pattern (InMemory + SQLAlchemy)
├── sql/
│   ├── schema.sql               # Database schema creation script
│   └── seed.sql                 # Initial data (admin user + amenities)
├── tests/
│   ├── __init__.py
│   ├── test_auth.py
│   ├── test_users.py
│   ├── test_amenities.py
│   ├── test_places.py
│   └── test_reviews.py
├── config.py                    # Multi-environment configuration
├── run.py                       # Application entry point
├── requirements.txt             # Python dependencies
└── README.md
```

## Setup

```bash
cd part3
pip install -r requirements.txt
```

## Running the Application

```bash
python run.py
```

The API is available at `http://localhost:5000`. Swagger docs at root URL.

## Running Tests

```bash
python -m pytest tests/ -v
```

## Key Features (Part 3)

### 0. Application Factory with Configuration
- `create_app()` accepts a config class (Development, Testing, Production)
- All extensions (Bcrypt, JWT, SQLAlchemy) initialized via factory pattern

### 1. Password Hashing (Bcrypt)
- Passwords hashed with bcrypt before storage
- `verify_password()` method on User model
- Passwords never returned in API responses

### 2. JWT Authentication
- `POST /api/v1/auth/login` — returns JWT access token
- Token includes `is_admin` and `email` claims
- Protected endpoints require `Authorization: Bearer <token>` header

### 3. Authenticated User Access
- Users can only modify their own places and reviews
- Users cannot review places they own
- Users cannot review the same place twice
- Public GET endpoints remain accessible without auth

### 4. Administrator Access (RBAC)
- Admins can create users (`POST /api/v1/users/`)
- Admins can modify any user's data (including email/password)
- Admins can create/modify amenities
- Admins bypass ownership restrictions on places/reviews

### 5–8. SQLAlchemy Persistence
- `SQLAlchemyRepository` implements the `Repository` interface
- All entities mapped to SQLAlchemy models
- Relationships:
  - **User → Place**: one-to-many (owner)
  - **User → Review**: one-to-many (author)
  - **Place → Review**: one-to-many (cascade delete)
  - **Place ↔ Amenity**: many-to-many (via `place_amenity` table)

### 9. SQL Scripts
- `sql/schema.sql` — creates all tables with constraints
- `sql/seed.sql` — inserts admin user and initial amenities

## API Endpoints

| Method | Endpoint | Auth | Access |
|--------|----------|------|--------|
| POST | `/api/v1/auth/login` | No | Public |
| GET | `/api/v1/users/` | No | Public |
| GET | `/api/v1/users/<id>` | No | Public |
| POST | `/api/v1/users/` | Yes | Admin only |
| PUT | `/api/v1/users/<id>` | Yes | Self or Admin |
| GET | `/api/v1/amenities/` | No | Public |
| GET | `/api/v1/amenities/<id>` | No | Public |
| POST | `/api/v1/amenities/` | Yes | Admin only |
| PUT | `/api/v1/amenities/<id>` | Yes | Admin only |
| GET | `/api/v1/places/` | No | Public |
| GET | `/api/v1/places/<id>` | No | Public |
| POST | `/api/v1/places/` | Yes | Authenticated |
| PUT | `/api/v1/places/<id>` | Yes | Owner or Admin |
| GET | `/api/v1/reviews/` | No | Public |
| GET | `/api/v1/reviews/<id>` | No | Public |
| POST | `/api/v1/reviews/` | Yes | Authenticated |
| PUT | `/api/v1/reviews/<id>` | Yes | Author or Admin |
| DELETE | `/api/v1/reviews/<id>` | Yes | Author or Admin |
| GET | `/api/v1/reviews/places/<id>/reviews` | No | Public |

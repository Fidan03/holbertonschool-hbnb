-- HBnB Initial Data
-- This script inserts the administrator user and initial amenities

-- Insert administrator user
-- Password: admin1234 (bcrypt hashed)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$LQv3c1yqBo9SkvXS7QTJp.eQ5eOqGZ7x0V0G7dZl1fO0x1GQk/G0a',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert initial amenities
INSERT INTO amenities (id, name, description, created_at, updated_at)
VALUES
    ('a1b2c3d4-e5f6-7890-abcd-ef1234567890', 'WiFi', 'High-speed wireless internet', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('b2c3d4e5-f6a7-8901-bcde-f12345678901', 'Swimming Pool', 'Outdoor swimming pool', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP),
    ('c3d4e5f6-a7b8-9012-cdef-123456789012', 'Air Conditioning', 'Central air conditioning', CURRENT_TIMESTAMP, CURRENT_TIMESTAMP);

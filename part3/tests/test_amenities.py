import unittest
from app import create_app, db


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity API endpoints."""

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            from app.models.user import User
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@example.com',
                password='adminpassword',
                is_admin=True
            )
            regular = User(
                first_name='Regular',
                last_name='User',
                email='regular@example.com',
                password='regularpassword',
                is_admin=False
            )
            db.session.add(admin)
            db.session.add(regular)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_token(self, email, password):
        """Helper to get JWT token."""
        response = self.client.post('/api/v1/auth/login', json={
            'email': email,
            'password': password
        })
        return response.get_json()['access_token']

    def test_create_amenity_as_admin(self):
        """Test creating an amenity as admin."""
        token = self._get_token('admin@example.com', 'adminpassword')
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'WiFi',
            'description': 'High-speed internet'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'WiFi')

    def test_create_amenity_as_regular_user(self):
        """Test creating an amenity as regular user (should fail)."""
        token = self._get_token('regular@example.com', 'regularpassword')
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'Pool',
            'description': 'Swimming pool'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 403)

    def test_get_all_amenities(self):
        """Test getting all amenities (public endpoint)."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_amenity_as_admin(self):
        """Test updating an amenity as admin."""
        token = self._get_token('admin@example.com', 'adminpassword')
        # Create first
        create_resp = self.client.post('/api/v1/amenities/', json={
            'name': 'Parking',
            'description': 'Free parking'
        }, headers={'Authorization': f'Bearer {token}'})
        amenity_id = create_resp.get_json()['id']

        # Update
        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': 'Covered Parking',
            'description': 'Covered free parking'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['name'], 'Covered Parking')


if __name__ == '__main__':
    unittest.main()

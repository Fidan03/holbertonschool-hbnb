import unittest
from app import create_app, db


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place API endpoints."""

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            from app.models.user import User
            owner = User(
                first_name='Owner',
                last_name='User',
                email='owner@example.com',
                password='ownerpassword',
                is_admin=False
            )
            other = User(
                first_name='Other',
                last_name='User',
                email='other@example.com',
                password='otherpassword',
                is_admin=False
            )
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@example.com',
                password='adminpassword',
                is_admin=True
            )
            db.session.add_all([owner, other, admin])
            db.session.commit()
            self.owner_id = owner.id
            self.other_id = other.id

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

    def test_create_place(self):
        """Test creating a new place."""
        token = self._get_token('owner@example.com', 'ownerpassword')
        response = self.client.post('/api/v1/places/', json={
            'title': 'Cozy Apartment',
            'description': 'A nice place',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': self.owner_id
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Cozy Apartment')

    def test_create_place_without_auth(self):
        """Test creating a place without authentication."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Test',
            'description': 'Test',
            'price': 50.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': self.owner_id
        })
        self.assertEqual(response.status_code, 401)

    def test_get_all_places(self):
        """Test getting all places (public)."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)

    def test_update_place_as_owner(self):
        """Test updating a place as the owner."""
        token = self._get_token('owner@example.com', 'ownerpassword')
        # Create a place
        create_resp = self.client.post('/api/v1/places/', json={
            'title': 'My Place',
            'description': 'Desc',
            'price': 80.0,
            'latitude': 35.0,
            'longitude': -80.0,
            'owner_id': self.owner_id
        }, headers={'Authorization': f'Bearer {token}'})
        place_id = create_resp.get_json()['id']

        # Update
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            'title': 'Updated Place',
            'price': 120.0
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()['title'], 'Updated Place')

    def test_update_place_as_non_owner(self):
        """Test updating a place as a non-owner (should fail)."""
        owner_token = self._get_token('owner@example.com', 'ownerpassword')
        other_token = self._get_token('other@example.com', 'otherpassword')

        # Create as owner
        create_resp = self.client.post('/api/v1/places/', json={
            'title': 'Owner Place',
            'description': 'Desc',
            'price': 80.0,
            'latitude': 35.0,
            'longitude': -80.0,
            'owner_id': self.owner_id
        }, headers={'Authorization': f'Bearer {owner_token}'})
        place_id = create_resp.get_json()['id']

        # Try to update as other user
        response = self.client.put(f'/api/v1/places/{place_id}', json={
            'title': 'Hacked'
        }, headers={'Authorization': f'Bearer {other_token}'})
        self.assertEqual(response.status_code, 403)

    def test_create_place_invalid_price(self):
        """Test creating a place with negative price."""
        token = self._get_token('owner@example.com', 'ownerpassword')
        response = self.client.post('/api/v1/places/', json={
            'title': 'Bad Place',
            'description': 'Invalid',
            'price': -50.0,
            'latitude': 40.0,
            'longitude': -74.0,
            'owner_id': self.owner_id
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

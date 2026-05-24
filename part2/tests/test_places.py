import unittest
from app import create_app


class TestPlaceEndpoints(unittest.TestCase):
    """Test cases for Place API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def _create_user(self):
        """Helper to create a user and return its ID."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Owner',
            'last_name': 'User',
            'email': f'owner{id(self)}@example.com',
            'password': 'password123'
        })
        return response.get_json()['id']

    def test_create_place(self):
        """Test creating a new place."""
        owner_id = self._create_user()
        response = self.client.post('/api/v1/places/', json={
            'title': 'Cozy Apartment',
            'description': 'A nice place to stay',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': owner_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['title'], 'Cozy Apartment')
        self.assertEqual(data['price'], 100.0)
        self.assertIn('id', data)

    def test_create_place_invalid_price(self):
        """Test creating a place with negative price."""
        owner_id = self._create_user()
        response = self.client.post('/api/v1/places/', json={
            'title': 'Bad Place',
            'description': 'Invalid',
            'price': -50.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_latitude(self):
        """Test creating a place with invalid latitude."""
        owner_id = self._create_user()
        response = self.client.post('/api/v1/places/', json={
            'title': 'Bad Place',
            'description': 'Invalid',
            'price': 50.0,
            'latitude': 100.0,
            'longitude': -74.0060,
            'owner_id': owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_longitude(self):
        """Test creating a place with invalid longitude."""
        owner_id = self._create_user()
        response = self.client.post('/api/v1/places/', json={
            'title': 'Bad Place',
            'description': 'Invalid',
            'price': 50.0,
            'latitude': 40.7128,
            'longitude': -200.0,
            'owner_id': owner_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_place_invalid_owner(self):
        """Test creating a place with non-existent owner."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Orphan Place',
            'description': 'No owner',
            'price': 50.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': 'nonexistent-id'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_place(self):
        """Test getting a place by ID."""
        owner_id = self._create_user()
        create_response = self.client.post('/api/v1/places/', json={
            'title': 'Beach House',
            'description': 'Ocean view',
            'price': 200.0,
            'latitude': 34.0195,
            'longitude': -118.4912,
            'owner_id': owner_id
        })
        place_id = create_response.get_json()['id']

        response = self.client.get(f'/api/v1/places/{place_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Beach House')
        self.assertIn('owner', data)

    def test_get_place_not_found(self):
        """Test getting a non-existent place."""
        response = self.client.get('/api/v1/places/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_all_places(self):
        """Test getting all places."""
        response = self.client.get('/api/v1/places/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_place(self):
        """Test updating a place."""
        owner_id = self._create_user()
        create_response = self.client.post('/api/v1/places/', json={
            'title': 'Mountain Cabin',
            'description': 'Peaceful retreat',
            'price': 150.0,
            'latitude': 39.7392,
            'longitude': -104.9903,
            'owner_id': owner_id
        })
        place_id = create_response.get_json()['id']

        response = self.client.put(f'/api/v1/places/{place_id}', json={
            'title': 'Luxury Mountain Cabin',
            'price': 250.0
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['title'], 'Luxury Mountain Cabin')
        self.assertEqual(data['price'], 250.0)


if __name__ == '__main__':
    unittest.main()

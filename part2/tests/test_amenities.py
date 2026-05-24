import unittest
from app import create_app


class TestAmenityEndpoints(unittest.TestCase):
    """Test cases for Amenity API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_amenity(self):
        """Test creating a new amenity."""
        response = self.client.post('/api/v1/amenities/', json={
            'name': 'WiFi',
            'description': 'High-speed internet access'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['name'], 'WiFi')
        self.assertIn('id', data)

    def test_create_amenity_missing_name(self):
        """Test creating an amenity without a name."""
        response = self.client.post('/api/v1/amenities/', json={
            'description': 'Some description'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_amenity(self):
        """Test getting an amenity by ID."""
        create_response = self.client.post('/api/v1/amenities/', json={
            'name': 'Pool',
            'description': 'Swimming pool'
        })
        amenity_id = create_response.get_json()['id']

        response = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Pool')

    def test_get_amenity_not_found(self):
        """Test getting a non-existent amenity."""
        response = self.client.get('/api/v1/amenities/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_all_amenities(self):
        """Test getting all amenities."""
        response = self.client.get('/api/v1/amenities/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_amenity(self):
        """Test updating an amenity."""
        create_response = self.client.post('/api/v1/amenities/', json={
            'name': 'Parking',
            'description': 'Free parking'
        })
        amenity_id = create_response.get_json()['id']

        response = self.client.put(f'/api/v1/amenities/{amenity_id}', json={
            'name': 'Covered Parking',
            'description': 'Covered free parking'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['name'], 'Covered Parking')

    def test_update_amenity_not_found(self):
        """Test updating a non-existent amenity."""
        response = self.client.put('/api/v1/amenities/nonexistent-id', json={
            'name': 'Updated',
            'description': 'Updated description'
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

import unittest
from app import create_app


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        """Test creating a new user."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'John')
        self.assertEqual(data['last_name'], 'Doe')
        self.assertEqual(data['email'], 'john.doe@example.com')
        self.assertNotIn('password', data)
        self.assertIn('id', data)

    def test_create_user_invalid_email(self):
        """Test creating a user with invalid email."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'invalid-email',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 400)

    def test_create_user_missing_fields(self):
        """Test creating a user with missing required fields."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_user(self):
        """Test getting a user by ID."""
        # First create a user
        create_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'password': 'password123'
        })
        user_id = create_response.get_json()['id']

        # Get the user
        response = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Jane')
        self.assertNotIn('password', data)

    def test_get_user_not_found(self):
        """Test getting a non-existent user."""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_all_users(self):
        """Test getting all users."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_user(self):
        """Test updating a user."""
        # Create a user
        create_response = self.client.post('/api/v1/users/', json={
            'first_name': 'Bob',
            'last_name': 'Jones',
            'email': 'bob.jones@example.com',
            'password': 'password123'
        })
        user_id = create_response.get_json()['id']

        # Update the user
        response = self.client.put(f'/api/v1/users/{user_id}', json={
            'first_name': 'Robert',
            'last_name': 'Jones',
            'email': 'bob.jones@example.com'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Robert')

    def test_update_user_not_found(self):
        """Test updating a non-existent user."""
        response = self.client.put('/api/v1/users/nonexistent-id', json={
            'first_name': 'Updated',
            'last_name': 'User',
            'email': 'updated@example.com'
        })
        self.assertEqual(response.status_code, 404)


if __name__ == '__main__':
    unittest.main()

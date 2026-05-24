import unittest
from app import create_app, db


class TestUserEndpoints(unittest.TestCase):
    """Test cases for User API endpoints."""

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create an admin user
            from app.models.user import User
            admin = User(
                first_name='Admin',
                last_name='User',
                email='admin@example.com',
                password='adminpassword',
                is_admin=True
            )
            db.session.add(admin)
            db.session.commit()
            self.admin_id = admin.id

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def _get_admin_token(self):
        """Helper to get admin JWT token."""
        response = self.client.post('/api/v1/auth/login', json={
            'email': 'admin@example.com',
            'password': 'adminpassword'
        })
        return response.get_json()['access_token']

    def test_create_user_as_admin(self):
        """Test creating a new user as admin."""
        token = self._get_admin_token()
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'password': 'securepassword'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'John')
        self.assertNotIn('password', data)

    def test_create_user_without_auth(self):
        """Test creating a user without authentication."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john2@example.com',
            'password': 'securepassword'
        })
        self.assertEqual(response.status_code, 401)

    def test_get_all_users(self):
        """Test getting all users (public endpoint)."""
        response = self.client.get('/api/v1/users/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_get_user_by_id(self):
        """Test getting a user by ID."""
        response = self.client.get(f'/api/v1/users/{self.admin_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['email'], 'admin@example.com')

    def test_get_user_not_found(self):
        """Test getting a non-existent user."""
        response = self.client.get('/api/v1/users/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_update_user_as_admin(self):
        """Test updating a user as admin."""
        token = self._get_admin_token()
        response = self.client.put(f'/api/v1/users/{self.admin_id}', json={
            'first_name': 'Updated'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['first_name'], 'Updated')

    def test_duplicate_email(self):
        """Test creating user with duplicate email."""
        token = self._get_admin_token()
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Dup',
            'last_name': 'User',
            'email': 'admin@example.com',
            'password': 'password'
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)


if __name__ == '__main__':
    unittest.main()

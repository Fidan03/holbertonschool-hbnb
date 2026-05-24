import unittest
from app import create_app, db


class TestAuthEndpoints(unittest.TestCase):
    """Test cases for Authentication API endpoints."""

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            # Create a test user directly
            from app.models.user import User
            user = User(
                first_name='Test',
                last_name='User',
                email='test@example.com',
                password='testpassword'
            )
            db.session.add(user)
            db.session.commit()

    def tearDown(self):
        with self.app.app_context():
            db.session.remove()
            db.drop_all()

    def test_login_success(self):
        """Test successful login."""
        response = self.client.post('/api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIn('access_token', data)

    def test_login_invalid_email(self):
        """Test login with invalid email."""
        response = self.client.post('/api/v1/auth/login', json={
            'email': 'wrong@example.com',
            'password': 'testpassword'
        })
        self.assertEqual(response.status_code, 401)

    def test_login_invalid_password(self):
        """Test login with wrong password."""
        response = self.client.post('/api/v1/auth/login', json={
            'email': 'test@example.com',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 401)


if __name__ == '__main__':
    unittest.main()

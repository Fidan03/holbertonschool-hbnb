import unittest
from app import create_app, db


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review API endpoints."""

    def setUp(self):
        self.app = create_app('config.TestingConfig')
        self.client = self.app.test_client()
        with self.app.app_context():
            db.create_all()
            from app.models.user import User
            from app.models.place import Place

            owner = User(
                first_name='Owner',
                last_name='User',
                email='owner@example.com',
                password='ownerpassword',
                is_admin=False
            )
            reviewer = User(
                first_name='Reviewer',
                last_name='User',
                email='reviewer@example.com',
                password='reviewerpassword',
                is_admin=False
            )
            db.session.add_all([owner, reviewer])
            db.session.commit()

            place = Place(
                title='Test Place',
                description='A test place',
                price=100.0,
                latitude=40.7128,
                longitude=-74.0060,
                owner_id=owner.id
            )
            db.session.add(place)
            db.session.commit()

            self.owner_id = owner.id
            self.reviewer_id = reviewer.id
            self.place_id = place.id

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

    def test_create_review(self):
        """Test creating a new review."""
        token = self._get_token('reviewer@example.com', 'reviewerpassword')
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.reviewer_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], 'Great place!')
        self.assertEqual(data['rating'], 5)

    def test_create_review_own_place(self):
        """Test creating a review on own place (should fail)."""
        token = self._get_token('owner@example.com', 'ownerpassword')
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'My own place',
            'rating': 5,
            'user_id': self.owner_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)

    def test_create_duplicate_review(self):
        """Test creating a duplicate review (should fail)."""
        token = self._get_token('reviewer@example.com', 'reviewerpassword')
        # First review
        self.client.post('/api/v1/reviews/', json={
            'text': 'Great place!',
            'rating': 5,
            'user_id': self.reviewer_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {token}'})

        # Duplicate review
        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Another review',
            'rating': 4,
            'user_id': self.reviewer_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {token}'})
        self.assertEqual(response.status_code, 400)

    def test_delete_review(self):
        """Test deleting a review."""
        token = self._get_token('reviewer@example.com', 'reviewerpassword')
        # Create review
        create_resp = self.client.post('/api/v1/reviews/', json={
            'text': 'To delete',
            'rating': 3,
            'user_id': self.reviewer_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {token}'})
        review_id = create_resp.get_json()['id']

        # Delete
        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers={'Authorization': f'Bearer {token}'}
        )
        self.assertEqual(response.status_code, 200)

    def test_delete_review_unauthorized(self):
        """Test deleting someone else's review (should fail)."""
        reviewer_token = self._get_token('reviewer@example.com', 'reviewerpassword')
        owner_token = self._get_token('owner@example.com', 'ownerpassword')

        # Create review as reviewer
        create_resp = self.client.post('/api/v1/reviews/', json={
            'text': 'Reviewer review',
            'rating': 4,
            'user_id': self.reviewer_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {reviewer_token}'})
        review_id = create_resp.get_json()['id']

        # Try to delete as owner (not admin, not author)
        response = self.client.delete(
            f'/api/v1/reviews/{review_id}',
            headers={'Authorization': f'Bearer {owner_token}'}
        )
        self.assertEqual(response.status_code, 403)

    def test_get_reviews_by_place(self):
        """Test getting reviews for a place."""
        token = self._get_token('reviewer@example.com', 'reviewerpassword')
        self.client.post('/api/v1/reviews/', json={
            'text': 'Place review',
            'rating': 4,
            'user_id': self.reviewer_id,
            'place_id': self.place_id
        }, headers={'Authorization': f'Bearer {token}'})

        response = self.client.get(f'/api/v1/reviews/places/{self.place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()

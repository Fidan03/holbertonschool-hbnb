import unittest
from app import create_app


class TestReviewEndpoints(unittest.TestCase):
    """Test cases for Review API endpoints."""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def _create_user(self, email='reviewer@example.com'):
        """Helper to create a user."""
        response = self.client.post('/api/v1/users/', json={
            'first_name': 'Review',
            'last_name': 'User',
            'email': email,
            'password': 'password123'
        })
        return response.get_json()['id']

    def _create_place(self, owner_id):
        """Helper to create a place."""
        response = self.client.post('/api/v1/places/', json={
            'title': 'Test Place',
            'description': 'A test place',
            'price': 100.0,
            'latitude': 40.7128,
            'longitude': -74.0060,
            'owner_id': owner_id
        })
        return response.get_json()['id']

    def test_create_review(self):
        """Test creating a new review."""
        user_id = self._create_user('review_create@example.com')
        place_id = self._create_place(user_id)

        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Great place to stay!',
            'rating': 5,
            'user_id': user_id,
            'place_id': place_id
        })
        self.assertEqual(response.status_code, 201)
        data = response.get_json()
        self.assertEqual(data['text'], 'Great place to stay!')
        self.assertEqual(data['rating'], 5)
        self.assertIn('id', data)

    def test_create_review_invalid_rating(self):
        """Test creating a review with invalid rating."""
        user_id = self._create_user('review_rating@example.com')
        place_id = self._create_place(user_id)

        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Bad rating',
            'rating': 6,
            'user_id': user_id,
            'place_id': place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_empty_text(self):
        """Test creating a review with empty text."""
        user_id = self._create_user('review_empty@example.com')
        place_id = self._create_place(user_id)

        response = self.client.post('/api/v1/reviews/', json={
            'text': '',
            'rating': 3,
            'user_id': user_id,
            'place_id': place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_user(self):
        """Test creating a review with non-existent user."""
        user_id = self._create_user('review_user@example.com')
        place_id = self._create_place(user_id)

        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Nice place',
            'rating': 4,
            'user_id': 'nonexistent-id',
            'place_id': place_id
        })
        self.assertEqual(response.status_code, 400)

    def test_create_review_invalid_place(self):
        """Test creating a review with non-existent place."""
        user_id = self._create_user('review_place@example.com')

        response = self.client.post('/api/v1/reviews/', json={
            'text': 'Nice place',
            'rating': 4,
            'user_id': user_id,
            'place_id': 'nonexistent-id'
        })
        self.assertEqual(response.status_code, 400)

    def test_get_review(self):
        """Test getting a review by ID."""
        user_id = self._create_user('review_get@example.com')
        place_id = self._create_place(user_id)

        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Wonderful stay!',
            'rating': 4,
            'user_id': user_id,
            'place_id': place_id
        })
        review_id = create_response.get_json()['id']

        response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], 'Wonderful stay!')

    def test_get_review_not_found(self):
        """Test getting a non-existent review."""
        response = self.client.get('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_all_reviews(self):
        """Test getting all reviews."""
        response = self.client.get('/api/v1/reviews/')
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.get_json(), list)

    def test_update_review(self):
        """Test updating a review."""
        user_id = self._create_user('review_update@example.com')
        place_id = self._create_place(user_id)

        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'Good place',
            'rating': 3,
            'user_id': user_id,
            'place_id': place_id
        })
        review_id = create_response.get_json()['id']

        response = self.client.put(f'/api/v1/reviews/{review_id}', json={
            'text': 'Amazing place!',
            'rating': 5
        })
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data['text'], 'Amazing place!')
        self.assertEqual(data['rating'], 5)

    def test_delete_review(self):
        """Test deleting a review."""
        user_id = self._create_user('review_delete@example.com')
        place_id = self._create_place(user_id)

        create_response = self.client.post('/api/v1/reviews/', json={
            'text': 'To be deleted',
            'rating': 2,
            'user_id': user_id,
            'place_id': place_id
        })
        review_id = create_response.get_json()['id']

        response = self.client.delete(f'/api/v1/reviews/{review_id}')
        self.assertEqual(response.status_code, 200)

        # Verify it's deleted
        get_response = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_response.status_code, 404)

    def test_delete_review_not_found(self):
        """Test deleting a non-existent review."""
        response = self.client.delete('/api/v1/reviews/nonexistent-id')
        self.assertEqual(response.status_code, 404)

    def test_get_reviews_by_place(self):
        """Test getting all reviews for a specific place."""
        user_id = self._create_user('review_byplace@example.com')
        place_id = self._create_place(user_id)

        # Create a review
        self.client.post('/api/v1/reviews/', json={
            'text': 'Place review',
            'rating': 4,
            'user_id': user_id,
            'place_id': place_id
        })

        response = self.client.get(f'/api/v1/reviews/places/{place_id}/reviews')
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertIsInstance(data, list)
        self.assertGreater(len(data), 0)


if __name__ == '__main__':
    unittest.main()

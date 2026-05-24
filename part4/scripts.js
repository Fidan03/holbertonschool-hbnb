/* ===== HBnB Front-End Scripts ===== */

const API_URL = 'http://localhost:5000/api/v1';

// ===== Utility Functions =====

function getCookie(name) {
    const value = `; ${document.cookie}`;
    const parts = value.split(`; ${name}=`);
    if (parts.length === 2) return parts.pop().split(';').shift();
    return null;
}

function getPlaceIdFromURL() {
    const params = new URLSearchParams(window.location.search);
    return params.get('id');
}

function checkAuthentication() {
    const token = getCookie('token');
    const loginLink = document.getElementById('login-link');

    if (loginLink) {
        if (!token) {
            loginLink.style.display = 'block';
        } else {
            loginLink.style.display = 'none';
        }
    }

    return token;
}

// ===== Login Page =====

function setupLoginForm() {
    const loginForm = document.getElementById('login-form');

    if (loginForm) {
        loginForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const email = document.getElementById('email').value;
            const password = document.getElementById('password').value;
            const errorElement = document.getElementById('login-error');

            try {
                const response = await fetch(`${API_URL}/auth/login`, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({ email, password })
                });

                if (response.ok) {
                    const data = await response.json();
                    document.cookie = `token=${data.access_token}; path=/`;
                    window.location.href = 'index.html';
                } else {
                    errorElement.style.display = 'block';
                    errorElement.textContent = 'Login failed: Invalid email or password.';
                }
            } catch (error) {
                errorElement.style.display = 'block';
                errorElement.textContent = 'Login failed: Could not connect to server.';
            }
        });
    }
}

// ===== Index Page - Places List =====

async function fetchPlaces(token) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/`, { headers });

        if (response.ok) {
            const places = await response.json();
            displayPlaces(places);
        }
    } catch (error) {
        console.error('Error fetching places:', error);
    }
}

function displayPlaces(places) {
    const placesList = document.getElementById('places-list');
    if (!placesList) return;

    placesList.innerHTML = '';

    places.forEach(place => {
        const placeCard = document.createElement('div');
        placeCard.className = 'place-card';
        placeCard.dataset.price = place.price;

        placeCard.innerHTML = `
            <h3>${place.title}</h3>
            <p class="price">$${place.price} per night</p>
            <p>${place.description || 'No description available.'}</p>
            <a href="place.html?id=${place.id}" class="details-button">View Details</a>
        `;

        placesList.appendChild(placeCard);
    });
}

function setupPriceFilter() {
    const priceFilter = document.getElementById('price-filter');

    if (priceFilter) {
        priceFilter.addEventListener('change', (event) => {
            const selectedPrice = event.target.value;
            const placeCards = document.querySelectorAll('.place-card');

            placeCards.forEach(card => {
                const cardPrice = parseFloat(card.dataset.price);

                if (selectedPrice === 'all' || cardPrice <= parseFloat(selectedPrice)) {
                    card.style.display = 'block';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    }
}

// ===== Place Details Page =====

async function fetchPlaceDetails(token, placeId) {
    try {
        const headers = {};
        if (token) {
            headers['Authorization'] = `Bearer ${token}`;
        }

        const response = await fetch(`${API_URL}/places/${placeId}`, { headers });

        if (response.ok) {
            const place = await response.json();
            displayPlaceDetails(place);
        } else {
            const placeDetails = document.getElementById('place-details');
            if (placeDetails) {
                placeDetails.innerHTML = '<p>Place not found.</p>';
            }
        }
    } catch (error) {
        console.error('Error fetching place details:', error);
    }
}

function displayPlaceDetails(place) {
    const placeDetails = document.getElementById('place-details');
    if (!placeDetails) return;

    let amenitiesHTML = '';
    if (place.amenities && place.amenities.length > 0) {
        amenitiesHTML = `
            <p><span class="label">Amenities:</span></p>
            <ul class="amenities-list">
                ${place.amenities.map(a => `<li>${a.name}</li>`).join('')}
            </ul>
        `;
    }

    placeDetails.innerHTML = `
        <h1>${place.title}</h1>
        <div class="place-info">
            <p><span class="label">Host:</span> ${place.owner ? place.owner.first_name + ' ' + place.owner.last_name : 'Unknown'}</p>
            <p><span class="label">Price:</span> $${place.price} per night</p>
            <p><span class="label">Description:</span> ${place.description || 'No description available.'}</p>
            <p><span class="label">Location:</span> ${place.latitude}, ${place.longitude}</p>
            ${amenitiesHTML}
        </div>
    `;

    // Display reviews
    const reviewsList = document.getElementById('reviews-list');
    if (reviewsList && place.reviews && place.reviews.length > 0) {
        reviewsList.innerHTML = '';
        place.reviews.forEach(review => {
            const reviewCard = document.createElement('div');
            reviewCard.className = 'review-card';
            reviewCard.innerHTML = `
                <p class="reviewer">User: ${review.user_id}</p>
                <p class="rating">${'★'.repeat(review.rating)}${'☆'.repeat(5 - review.rating)}</p>
                <p class="comment">${review.text}</p>
            `;
            reviewsList.appendChild(reviewCard);
        });
    } else if (reviewsList) {
        reviewsList.innerHTML = '<p>No reviews yet.</p>';
    }
}

// ===== Add Review Page & Form =====

async function submitReview(token, placeId, reviewText, rating) {
    try {
        const response = await fetch(`${API_URL}/reviews/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            },
            body: JSON.stringify({
                text: reviewText,
                rating: parseInt(rating),
                place_id: placeId,
                user_id: ''
            })
        });

        return response;
    } catch (error) {
        console.error('Error submitting review:', error);
        return null;
    }
}

function setupReviewForm(token, placeId) {
    const reviewForm = document.getElementById('review-form');

    if (reviewForm) {
        reviewForm.addEventListener('submit', async (event) => {
            event.preventDefault();

            const reviewText = document.getElementById('review-text').value;
            const rating = document.getElementById('review-rating').value;
            const messageElement = document.getElementById('review-message');

            if (!rating) {
                messageElement.textContent = 'Please select a rating.';
                messageElement.className = 'error';
                return;
            }

            const response = await submitReview(token, placeId, reviewText, rating);

            if (response && response.ok) {
                messageElement.textContent = 'Review submitted successfully!';
                messageElement.className = 'success';
                reviewForm.reset();
            } else {
                messageElement.textContent = 'Failed to submit review. Please try again.';
                messageElement.className = 'error';
            }
        });
    }
}

// ===== Page Initialization =====

document.addEventListener('DOMContentLoaded', () => {
    const token = checkAuthentication();
    const currentPage = window.location.pathname.split('/').pop();

    // Login page
    if (currentPage === 'login.html' || currentPage === '') {
        setupLoginForm();
    }

    // Index page
    if (currentPage === 'index.html' || currentPage === '' || currentPage === '/') {
        fetchPlaces(token);
        setupPriceFilter();
    }

    // Place details page
    if (currentPage === 'place.html') {
        const placeId = getPlaceIdFromURL();
        if (placeId) {
            fetchPlaceDetails(token, placeId);

            // Show/hide add review section
            const addReviewSection = document.getElementById('add-review');
            if (addReviewSection) {
                if (token) {
                    addReviewSection.style.display = 'block';
                    setupReviewForm(token, placeId);
                } else {
                    addReviewSection.style.display = 'none';
                }
            }
        }
    }

    // Add review page (standalone)
    if (currentPage === 'add_review.html') {
        if (!token) {
            window.location.href = 'index.html';
            return;
        }

        const placeId = getPlaceIdFromURL();
        if (placeId) {
            setupReviewForm(token, placeId);
        }
    }
});

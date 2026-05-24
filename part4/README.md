# HBnB - Part 4: Front-End (HTML/CSS/JavaScript)

## Project Structure

```
part4/
├── index.html           # Main page - list of places with price filter
├── login.html           # Login form page
├── place.html           # Place details page with reviews
├── add_review.html      # Standalone add review form page
├── styles.css           # All CSS styles
├── scripts.js           # All JavaScript functionality
└── README.md
```

## Pages

### Login (`login.html`)
- Email and password form
- AJAX POST to `/api/v1/auth/login`
- Stores JWT token in cookie on success
- Redirects to `index.html`

### Places List (`index.html`)
- Fetches all places from API
- Displays place cards (name, price, View Details button)
- Client-side price filter (All, $10, $50, $100)
- Shows/hides login link based on authentication

### Place Details (`place.html`)
- Fetches place by ID from URL query param (`?id=<place_id>`)
- Displays host, price, description, amenities, reviews
- Shows add review form only for authenticated users

### Add Review (`add_review.html`)
- Standalone review submission form
- Redirects unauthenticated users to index
- Submits review via POST to `/api/v1/reviews/`

## Setup

1. Place `logo.png` and `icon.png` in this directory
2. Ensure the Part 3 API server is running at `http://localhost:5000`
3. Open `index.html` in a browser (or serve via a local HTTP server)

## API Integration

The front-end connects to the Part 3 Flask API at `http://localhost:5000/api/v1`.
Update the `API_URL` variable in `scripts.js` if your API runs on a different host/port.

## Design Specs

- **Margin**: 20px for place and review cards
- **Padding**: 10px within place and review cards
- **Border**: 1px solid #ddd
- **Border Radius**: 10px
- **Color palette**: Blue (#3498db), Dark (#2c3e50), Green (#27ae60)
- **Font**: Segoe UI / system sans-serif

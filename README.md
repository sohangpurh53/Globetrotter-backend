Design and implement a full-stack web application called 'Globetrotter Challenge' with a Next.js frontend and Django REST Framework backend. The app is a travel guessing game where users guess famous destinations based on cryptic clues, unlocking fun facts and trivia upon answering. Use the provided starter dataset (3 destinations: Paris, Tokyo, New York) and expand it to 100+ destinations using AI tools (e.g., web scraping or GPT-based generation), including clues, fun facts, and trivia for each.

# Globetrotter Challenge Backend

A Django REST Framework backend for the Globetrotter Challenge travel guessing game.

## API Documentation

The API documentation is available through Swagger UI and ReDoc:

- Swagger UI: `/swagger/` - Interactive API documentation
- ReDoc: `/redoc/` - Alternative API documentation view
- Raw Schema: `/swagger.json` - Raw API schema in JSON format

## API Endpoints

### Destinations

- `GET /api/destinations/random/` - Get a random destination with clues and multiple-choice options
- `GET /api/all/` - Get all destinations

### User Management

- `POST /api/users/` - Register a new user
- `GET /api/users/<username>/` - Get user profile and score

### Game Mechanics

- `POST /api/guess/` - Submit a guess and receive feedback

## Setup and Installation

1. Clone the repository
2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```
3. Run migrations:
   ```
   python manage.py migrate
   ```
4. Start the development server:
   ```
   python manage.py runserver
   ```

## Technologies Used

- Django REST Framework
- SQLite database
- drf-yasg for Swagger/OpenAPI documentation

Backend (Django REST Framework):

Create a model for Destination with fields: city, country, clues (list), fun_facts (list), trivia (list).
Store the expanded 100+ destination dataset in a database (e.g., SQLite or PostgreSQL).
Build API endpoints:
GET /api/destinations/random/ to return 1–2 random clues and 4 multiple-choice options (1 correct, 3 random).
POST /api/guess/ to submit a user's guess and return feedback (correct/incorrect, fun fact).
POST /api/users/ to register a username and create a profile.
GET /api/users/<username>/ to fetch user score and profile.
Use Django's ORM to manage data and ensure the dataset is retrieved dynamically from the backend.

# Kira-Blog

A simple Flask-based blog API with JWT authentication and SQLite database.

## Project Status

- The backend (Flask API) is complete and ready for use.
- The frontend (React app in `/frontend`) is currently under development. Some features or pages may be incomplete or subject to change.

## Features
- User registration and login (JWT-based)
- Create, read, and list blog posts
- Input validation with Marshmallow
- Automated tests and Postman collection

## Setup
1. Clone the repository and navigate to the `Kira-Blog` directory.
2. Create a `.env` file based on `.env.example` and fill in your secrets. Example:
   ```
   SECRET_KEY=your-secret-key
   DATABASE_URL=sqlite:///instance/test.db
   JWT_SECRET_KEY=your-jwt-secret
   ```
3. (Recommended) Create and activate a virtual environment:
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```
4. Install dependencies:
   ```sh
   pip install -r requirements.txt
   ```
5. Run the app:
   ```sh
   export FLASK_APP=run.py
   flask run
   ```

## Testing
- Activate the virtual environment:
  ```sh
  source venv/bin/activate
  ```
- Run API tests with pytest:
  ```sh
  pytest
  ```
- Use the Postman collection (`postman_collection.json`) to explore endpoints.

## Environment Variables
See `.env.example` for required variables.

## Project Structure
- `app.py` - App factory and setup
- `config.py` - Configuration
- `extensions.py` - Flask extensions
- `models.py` - Database models
- `schemas.py` - Marshmallow schemas
- `routes/` - API route blueprints
- `test_api.py` - API tests

## Monorepo Structure: Backend & Frontend

This repository contains both the Flask backend API and a React frontend. They are fully decoupled:

- **Backend** (`/`): Flask REST API. Can be used independently by any frontend.
- **Frontend** (`/frontend`): React app that consumes the backend API.

### Using the Backend Only
- You can use the Flask API as a standalone service for your own frontend or mobile app.
- All endpoints are documented below and in the Postman collection.
- Set the API base URL in your frontend to point to your backend (e.g., `http://localhost:5000`).

### Using the Frontend
- The React app in `/frontend` is preconfigured to use the backend API at `http://localhost:5000`.
- You can modify the API base URL in the frontend code if you deploy the backend elsewhere.

## API Endpoints (Summary)
- `POST /register` — Register a new user
- `POST /login` — Login and receive JWT token
- `GET /posts` — List all posts
- `POST /posts` — Create a post (auth required)
- `PUT /posts/<id>` — Edit a post (auth required)
- `DELETE /posts/<id>` — Delete a post (auth required)
- `GET /my-posts` — List posts created by the authenticated user

See the Postman collection for full details and example requests.

## API Usage Example

You can use the backend API with any frontend or tool. Example using `curl`:

```sh
curl -X POST http://localhost:5000/login -H "Content-Type: application/json" -d '{"username":"youruser","password":"yourpass"}'
```

Or using JavaScript (fetch):

```js
fetch('http://localhost:5000/posts', {
  headers: { 'Authorization': 'Bearer <your_token>' }
})
  .then(res => res.json())
  .then(data => console.log(data));
```

## Changing the API Base URL in the Frontend

Set the API URL in `frontend/.env`:
```
REACT_APP_API_URL=http://localhost:5000
```

---

For more details, see code comments and docstrings in each file.

# Kira-Blog

A simple Flask-based blog API with JWT authentication and SQLite database.

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

---

For more details, see code comments and docstrings in each file.

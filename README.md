# Todo API

A secure REST API built with Flask that provides todo list management with user authentication and administrative capabilities.

## Features

- User authentication with JWT tokens
- Todo CRUD operations
- User management with admin privileges
- Local JSON file storage
- CORS support
- Secure password hashing using scrypt

## Prerequisites

- Python 3.7+
- pip (Python package manager)

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd into it
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install flask flask-cors werkzeug PyJWT # or in req.txt in the backend directory
```

4. Set up environment variables (optional):
```bash
export SECRET_KEY=your-secret-key  # On Windows: set SECRET_KEY=your-secret-key # For JWT
```


### Authentication

#### POST /api/signup
Create a new user account.
```json
{
    "username": "string",
    "password": "string",
    "name": "string (optional)"
}
```

#### POST /api/login
Authenticate user and receive JWT token.
```json
{
    "username": "string",
    "password": "string"
}
```

### Todos

All todo endpoints require Authentication header: `Bearer <token>`

#### GET /api/todos
Get all todos for authenticated user.

#### POST /api/todos
Create a new todo.
```json
{
    "content": "string"
}
```

#### PUT /api/todos/<todo_id>
Update a specific todo.
```json
{
    "content": "string (optional)",
    "completed": "boolean (optional)"
}
```

#### DELETE /api/todos/<todo_id>
Delete a specific todo.

### Admin Routes

Requires admin user authentication

#### GET /api/admin/users
Get list of all users with todo counts.

#### DELETE /api/admin/users/<user_id>
Delete a specific user.

## Data Storage

The application uses local JSON files for data storage:

- `users.json`: Stores user information
- `todos.json`: Stores todo items

The files are automatically created if they don't exist.

## Security Features

- Password hashing using scrypt
- JWT token authentication
- Token expiration (24 hours)
- Admin-only routes
- Secure password storage
- CORS protection

## Error Handling

The API returns appropriate HTTP status codes:

- 200: Success
- 201: Created
- 400: Bad Request
- 401: Unauthorized
- 403: Forbidden
- 404: Not Found

## Running the Application

Start the development server:
```bash
python app.py
export NODE_OPTIONS=--openssl-legacy-provider
```

The API will be available at `http://localhost:5000` and the frontend on `http://localhost:3000`

## Development Mode

The application runs in debug mode by default when started directly. For production deployment, make sure to:

1. Disable debug mode
2. Implement proper database storage or locally
3. `export NODE_OPTIONS=--openssl-legacy-provider`

## Contributing
Feel free to contribute!

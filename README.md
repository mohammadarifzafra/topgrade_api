# Django JWT Authentication API

A simple Django REST API with JWT authentication using Django Ninja and Simple JWT.

## Features

- Email/password login with JWT token generation
- Access and refresh token support
- Protected endpoints with JWT authentication
- User information retrieval
- Token refresh functionality

## Setup

1. Install dependencies:
```bash
pip install django ninja djangorestframework-simplejwt pyjwt
```

2. Run migrations:
```bash
python manage.py migrate
```

3. Create a test user:
```bash
python manage.py shell -c "
from django.contrib.auth.models import User
user = User.objects.create_user(
    username='testuser',
    email='test@example.com',
    password='testpassword123'
)
print(f'Created user: {user.email}')
"
```

4. Start the development server:
```bash
python manage.py runserver
```

## API Endpoints

### Authentication

#### POST `/api/auth/login`
Login with email and password to get JWT tokens.

**Request Body:**
```json
{
    "email": "test@example.com",
    "password": "testpassword123"
}
```

**Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "user_id": 1,
    "email": "test@example.com"
}
```

**Error Response (400):**
```json
{
    "error": "Invalid credentials",
    "detail": "User with this email does not exist"
}
```

#### POST `/api/auth/refresh`
Refresh access token using refresh token.

**Request Body:**
```json
{
    "refresh": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Response (200):**
```json
{
    "access": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

### Protected Endpoints

#### GET `/api/auth/me`
Get current authenticated user information.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "user_id": 1,
    "username": "testuser",
    "email": "test@example.com",
    "first_name": "",
    "last_name": "",
    "is_staff": false,
    "is_active": true,
    "date_joined": "2024-01-01T00:00:00Z"
}
```

#### GET `/api/auth/protected`
Example protected endpoint.

**Headers:**
```
Authorization: Bearer <access_token>
```

**Response (200):**
```json
{
    "message": "This is a protected endpoint",
    "user_id": 1,
    "username": "testuser",
    "email": "test@example.com"
}
```

### Public Endpoints

#### GET `/api/hello`
Simple hello world endpoint (no authentication required).

**Response (200):**
```json
{
    "message": "Hello World!"
}
```

## Testing

Run the test script to verify the authentication system:

```bash
python tmp_rovodev_test_login.py
```

This will test:
- Valid login
- Invalid login
- Token refresh
- Protected endpoint access

## JWT Configuration

The JWT tokens are configured with the following settings:

- **Access Token Lifetime**: 60 minutes
- **Refresh Token Lifetime**: 7 days
- **Token Rotation**: Enabled (new refresh token on each refresh)
- **Algorithm**: HS256

## Usage Examples

### Using curl

1. **Login:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "testpassword123"}'
```

2. **Access protected endpoint:**
```bash
curl -X GET http://127.0.0.1:8000/api/auth/me \
  -H "Authorization: Bearer YOUR_ACCESS_TOKEN"
```

3. **Refresh token:**
```bash
curl -X POST http://127.0.0.1:8000/api/auth/refresh \
  -H "Content-Type: application/json" \
  -d '{"refresh": "YOUR_REFRESH_TOKEN"}'
```

### Using Python requests

```python
import requests

# Login
response = requests.post('http://127.0.0.1:8000/api/auth/login', json={
    'email': 'test@example.com',
    'password': 'testpassword123'
})
tokens = response.json()

# Use access token
headers = {'Authorization': f'Bearer {tokens["access"]}'}
user_info = requests.get('http://127.0.0.1:8000/api/auth/me', headers=headers)
print(user_info.json())
```

## Project Structure

```
topgrade/
├── manage.py
├── db.sqlite3
├── topgrade/
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
└── topgrade_api/
    ├── __init__.py
    ├── models.py
    ├── views.py
    ├── urls.py
    ├── schemas.py
    ├── auth.py
    ├── admin.py
    ├── apps.py
    └── tests.py
```

## Security Notes

- The secret key is used for JWT signing - keep it secure in production
- Access tokens have a short lifetime (60 minutes) for security
- Refresh tokens are rotated on each use
- Always use HTTPS in production
- Consider implementing rate limiting for login attempts
# Authentication API Documentation

## Overview
This document provides a complete guide for implementing authentication in your frontend/mobile application using our Django REST API with JWT tokens.

## Base URL
```
http://your-domain.com/auth/
```

## Authentication Flow

### 1. Token-Based Authentication
- **Access Token**: Valid for 1 hour, used for API calls
- **Refresh Token**: Valid for 7 days, used to get new access tokens
- **Header Format**: `Authorization: Bearer <access_token>`

---

## API Endpoints

### 1. Email Signup
**Endpoint**: `POST /auth/signup`

**Request Body**:
```json
{
    "fullname": "John Doe",
    "email": "john@example.com",
    "password": "securepassword123",
    "confirm_password": "securepassword123"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "User created successfully",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "has_area_of_intrest": true
}
```

**Error Responses**:
```json
// Passwords don't match
{
    "message": "Passwords do not match"
}

// Email already exists
{
    "message": "User with this email already exists"
}
```

---

### 2. Email Signin
**Endpoint**: `POST /auth/signin`

**Request Body**:
```json
{
    "email": "john@example.com",
    "password": "securepassword123"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Signin successful",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "has_area_of_intrest": true
}
```

**Error Response** (401):
```json
{
    "message": "User not found"
}
```

---

### 3. Phone OTP Signin (2-Step Process)

#### Step 1: Request OTP
**Endpoint**: `POST /auth/request-phone-otp`

**Request Body**:
```json
{
    "phone_number": "9876543210"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "OTP sent to phone successfully",
    "user_exists": true
}
```

**Error Response** (400):
```json
{
    "message": "Phone number must be exactly 10 digits"
}
```

#### Step 2: Signin with OTP
**Endpoint**: `POST /auth/phone-signin`

**Request Body**:
```json
{
    "phone_number": "9876543210",
    "otp": "654321"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Phone signin successful",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9...",
    "has_area_of_intrest": true
}
```

**Error Responses**:
```json
// No OTP request found
{
    "message": "No OTP request found. Please request OTP first."
}

// OTP expired
{
    "message": "OTP has expired. Please request a new OTP."
}

// Invalid OTP
{
    "message": "Invalid OTP"
}
```

**Note**: If user doesn't exist, they will be automatically created with:
- **fullname**: Masked phone (e.g., "98XXXXXXX0")
- **email**: Auto-generated (e.g., "phone_9876543210_1703123456@tempuser.com")

---

### 4. Password Reset (3-Step Process)

#### Step 1: Request OTP for Reset
**Endpoint**: `POST /auth/request-otp`

**Request Body**:
```json
{
    "email": "john@example.com"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "OTP sent successfully"
}
```

**Error Response** (404):
```json
{
    "message": "User with this email does not exist"
}
```

#### Step 2: Verify OTP
**Endpoint**: `POST /auth/verify-otp`

**Request Body**:
```json
{
    "email": "john@example.com",
    "otp": "654321"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "OTP verified successfully"
}
```

**Error Responses**:
```json
// Invalid OTP
{
    "message": "Invalid OTP"
}

// User not found
{
    "message": "User with this email does not exist"
}
```

#### Step 3: Reset Password
**Endpoint**: `POST /auth/reset-password`

**Request Body**:
```json
{
    "email": "john@example.com",
    "new_password": "newpassword123",
    "confirm_password": "newpassword123"
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Password reset successfully"
}
```

**Error Responses**:
```json
// Passwords don't match
{
    "message": "Passwords do not match"
}

// User not found
{
    "message": "User with this email does not exist"
}
```

---

### 5. Refresh Token
**Endpoint**: `POST /auth/refresh`

**Request Body**:
```json
{
    "refresh_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Success Response** (200):
```json
{
    "success": true,
    "message": "Token refreshed successfully",
    "access_token": "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9..."
}
```

**Error Response** (401):
```json
{
    "message": "Invalid or expired refresh token"
}
```

---
## Important Notes

### 1. OTP Configuration
- **Static OTP**: Currently set to "654321" for all requests
- **OTP Expiration**: 10 minutes for both email and phone OTP
- **Phone Validation**: Must be exactly 10 digits
- **Supported Formats**: "9876543210", "+91 9876543210", "(987) 654-3210"
- **Security**: OTP verification is required before password reset or phone signin

### 2. Security Best Practices
- Store tokens securely (not in plain localStorage for production)
- Implement automatic token refresh
- Handle token expiration gracefully
- Use HTTPS in production
- Validate all user inputs

### 3. Error Handling
- Always check response status codes
- Implement retry logic for network failures
- Show user-friendly error messages
- Log errors for debugging

### 4. Token Lifecycle
- **Access Token**: 1 hour expiry
- **Refresh Token**: 7 days expiry
- **Auto-refresh**: Implement automatic token refresh
- **Logout**: Clear all stored tokens

### 5. OTP Verification Security
- **Email Password Reset**: Must complete 3-step flow (request → verify → reset)
- **Phone Signin**: Must complete 2-step flow (request → signin with OTP)
- **Verification Tracking**: System tracks OTP verification status internally
- **One-time Use**: OTP verification records are cleaned up after successful completion
- **Expiration**: All OTP verifications expire after 10 minutes
- **Sequential Flow**: Cannot skip steps - must request OTP before verification/signin

---

## Testing Endpoints

You can test all endpoints using tools like:
- **Postman**
- **curl**
- **Insomnia**
- **Thunder Client** (VS Code extension)

Example curl command:
```bash
curl -X POST http://your-domain.com/auth/signin \
  -H "Content-Type: application/json" \
  -d '{"email": "test@example.com", "password": "password123"}'
```

---

## Support

For any issues or questions regarding the authentication API, please contact the backend development team or refer to the API documentation at:
- **General API Docs**: `http://your-domain.com/api/docs`
- **Auth API Docs**: `http://your-domain.com/auth/docs`
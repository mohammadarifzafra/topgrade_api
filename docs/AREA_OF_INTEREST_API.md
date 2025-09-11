# Area of Interest API Documentation

## Overview
This document provides comprehensive documentation for the Area of Interest API endpoint. This endpoint allows authenticated users to update their area of interest, which can be used for personalization, content recommendations, and user profiling.

## Base URL
```
http://your-domain.com/
```

## Authentication Required
This endpoint requires JWT authentication. Users must include a valid access token in the Authorization header.

---

## API Endpoint

### Update Area of Interest
**Endpoint**: `POST /add-area-of-interest`

**Authentication**: Required (Bearer Token)

**Description**: Updates the authenticated user's area of interest. This field can be used to personalize user experience, show relevant content, or categorize users based on their interests.

#### Request Headers
```
Content-Type: application/json
Authorization: Bearer <access_token>
```

#### Request Body
```json
{
    "area_of_intrest": "Technology"
}
```

**Schema Definition**:
- `area_of_intrest` (string, required): The user's area of interest

**Example Values**:
- "Technology"
- "Healthcare"
- "Education"
- "Finance"
- "Sports"
- "Entertainment"
- "Travel"
- "Food & Cooking"
- "Art & Design"
- "Business"

#### Success Response (200)
```json
{
    "success": true,
    "message": "Area of interest updated successfully",
    "area_of_intrest": "Technology"
}
```

#### Error Responses

**Unauthorized (401)**:
```json
{
    "detail": "Authentication credentials were not provided."
}
```

**Invalid Token (401)**:
```json
{
    "detail": "Given token not valid for any token type"
}
```

**Server Error (500)**:
```json
{
    "message": "Error updating area of interest: [error details]"
}
```

**Validation Error (422)**:
```json
{
    "detail": [
        {
            "type": "missing",
            "loc": ["body", "area_of_intrest"],
            "msg": "Field required"
        }
    ]
}
```

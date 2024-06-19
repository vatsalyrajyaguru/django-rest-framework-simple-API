# Customer Management API

## Overview
This API provides endpoints for managing customers in the application. It is built using Django Rest Framework (DRF). This document includes details on how to log in to obtain an authentication token, add a customer, retrieve customer details, edit customer information, and change a user's password.

## Prerequisites
- Ensure you have the API running locally on `http://localhost:8000`.
- Python and Django installed on your system.

## Authentication
All API requests, except for the login request, require an authentication token. You need to include the token in the request headers.

## API Endpoints

### 1. Login to Obtain Token
**URL:** `http://localhost:8000/api/login/`

**Method:** `POST`

**Request Body:**
```json
{
    "username": "admin@gmail.com",
    "password": "admin123"
}
```

### 2. Add Customer
**URL:** `http://localhost:8000/api/add_customer/`

**Method:** `POST`
**Authorization::** Token <your_token_here>

**Request Body:**
```json
{
    {
    "full_name": "John Doe",
    "mobile_number": "1234567890",
    "birthdate": "1990-01-01",
    "gender": 1,
    "addresses": [
        {
            "address": "123 Main St",
            "landmark": "Near Park",
            "pincode": "123456"
        }
    ]
}
```

### 3.Get Customer
**URL:** `http://localhost:8000/api/get_customer/1/` (replace 1 with a valid customer ID)

**Method:** `GET`

**Authorization:** Token <your_token_here>

### 4. Edit Customer
**URL:** `http://localhost:8000/api/edit_customer/1/`(replace 1 with a valid customer ID)

**Method:** `PUT or PATCH`

**Authorization::** Token <your_token_here>

**Request Body:**
```json
--> updated data
{ 
    "full_name": "John Doe",
    "mobile_number": "1234567890",
    "birthdate": "1990-01-01",
    "gender": 1,
    "addresses": [
        {
            "address": "456 Elm St",
            "landmark": "Near School",
            "pincode": "654321"
        }
    ]
}
```

### 5. Change Password
**URL:** `http://localhost:8000/api/change_password/`

**Method:** `POST`

**Authorization::** Token <your_token_here>

**Request Body:**
```json
{
    "old_password": "old_password",
    "new_password": "new_password123"
}
```

## Additional Information

**Django Rest Framework (DRF)**

- Django Rest Framework is a powerful and flexible toolkit for building Web APIs in Django. It includes:

- A web browsable API.
- Authentication policies including packages for OAuth1a and OAuth2.
- Serialization that supports both ORM and non-ORM data sources.
- Customizable all the way down - just use regular function-based - views if you don't need the more powerful features.

## API Usage Tips

- Always include the Authorization header with the token received from the login endpoint for authenticated endpoints.
- Ensure your JSON payloads are correctly formatted and include all required fields.
- Use appropriate HTTP methods: POST for creating resources, GET for retrieving data, PUT or PATCH for updating resources, and DELETE for removing resources (if applicable).

## Conclusion
This documentation provides the necessary details to interact with the customer management API using Django Rest Framework. For further details, refer to the DRF official documentation or the source code of the project.


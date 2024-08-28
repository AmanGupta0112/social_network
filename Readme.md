# Social Network API

This project is a social networking application API built with Django Rest Framework.

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/social-network-api.git
   cd social-network-api
   ```

2. Build and run the Docker containers:
   ```
   docker-compose up --build
   ```

3. Apply migrations:
   ```
   docker-compose exec web python manage.py migrate
   ```

4. Create a superuser:
   ```
   docker-compose exec web python manage.py createsuperuser
   ```

## API Endpoints

- User Signup: POST /api/users/signup/
- User Login: POST /api/users/login/
- Search Users: GET /api/users/search/?query=
- Send Friend Request: POST /api/friend-requests/send_request/
- Accept Friend Request: POST /api/friend-requests/{id}/accept/
- Reject Friend Request: POST /api/friend-requests/{id}/reject/
- List Friends: GET /api/friend-requests/list_friends/
- List Pending Friend Requests: GET /api/friend-requests/pending_requests/

For detailed API documentation, please refer to the Postman collection.

## Running Tests

To run the tests, use the following command:

```
docker-compose exec web python manage.py test
```

## Postman Collection

A Postman collection for testing the API endpoints is included in the `postman` directory of this repository.

To use it:
1. Open Postman
2. Click on "Import" and select the JSON file from the `postman` directory
3. Set up an environment variable called `base_url` with the value `http://localhost:8000/api`
4. You can now use the imported collection to test the API endpoints
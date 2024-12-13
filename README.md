# Django E-Commerce Application

This is a Dockerized Django application for managing an e-commerce system with PostgreSQL as the database and PgAdmin for database management.

## Prerequisites

Before starting, ensure you have the following installed on your machine:
- [Docker](https://docs.docker.com/get-docker/)
- [Docker Compose](https://docs.docker.com/compose/install/)

## Setup Instructions

### 1. Clone the Repository
```bash
git clone https://github.com/kalyanakannan/ecommerce.git
cd ecommerce
```

### 2. Create a `.env` File
Create a `.env` file in the root directory with the following environment variables:
```env
# Django settings
DJANGO_DEBUG=False
ALLOWED_HOSTS=localhost,127.0.0.1

# Database settings
DATABASE_NAME=ecommerce_db
DATABASE_USER=ecommerce_user
DATABASE_PASSWORD=secure_password
POSTGRES_HOST=postgres
POSTGRES_PORT=5432

# pgAdmin settings
PGADMIN_DEFAULT_EMAIL=admin@admin.com
PGADMIN_DEFAULT_PASSWORD=admin
```

### 3. Build and Run the Containers
To build and start the application, use:
```bash
docker-compose up --build
```

This will:
- Build the `app` service from the provided `Dockerfile`.
- Start the `PostgreSQL` and `PgAdmin` services.
- Apply migrations and start the Django application using Gunicorn.

The application will be available at `http://localhost:8000`.

### 4. Access PgAdmin
PgAdmin will be available at `http://localhost:5050`. Use the email and password specified in the `.env` file to log in.

## Running Tests

To run tests, enter the `app` container and execute the test suite:
```bash
docker exec -it app_container python manage.py test
```

## Useful Commands

### Stop the Containers
```bash
docker-compose down
```

### View Logs
To view logs for the app container:
```bash
docker logs app_container
```

### Rebuild the Containers
If you make changes to the `Dockerfile` or dependencies:
```bash
docker-compose down --volumes
docker-compose up --build
```

## Troubleshooting

### 400 Bad Request
- Ensure `ALLOWED_HOSTS` in the `.env` file includes `localhost` or `*` for development.

### Database Connection Issues
- Verify the `DATABASE_*` environment variables in the `.env` file match the settings in `docker-compose.yml`.
- Check the `postgres_container` logs for errors:
  ```bash
  docker logs postgres_container
  ```
  

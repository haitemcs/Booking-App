# Booking App

A full-stack room-booking application with a Django REST Framework API and a React/Vite frontend. PostgreSQL stores application data, and Docker Compose can run the database, backend, and frontend together.

## Features

- Room listing and room detail endpoints
- Room-image management
- User registration, token login, and logout
- Authenticated booking (occupancy) creation and management
- Users can access their own bookings; staff users have broader access
- Date validation and protection against invalid or overlapping bookings
- Django password validation and login throttling
- API tests and a GitHub Actions workflow

## Tech stack

- Python and Django 6.1
- Django REST Framework
- PostgreSQL 16
- React and Vite
- Docker Compose
- GitHub Actions

## Project layout

```text
Booking-App/
├── backend/
│   ├── .env.example
│   ├── Dockerfile
│   ├── requirements.txt
│   └── booking_backend/
│       ├── manage.py
│       ├── booking_backend/
│       └── room_booking/
├── frontend/
├── docker-compose.yml
├── .github/workflows/ci.yml
├── LICENSE
└── README.md
```

## Run with Docker Compose

Requirements: Docker Engine and the Docker Compose plugin.

From the repository root:

```bash
cp backend/.env.example backend/.env
```

Edit `backend/.env` and set a suitable development secret and database password. The Compose file provides its own PostgreSQL container configuration; keep the database credentials in the environment consistent with that configuration before running the app.

Then start the services:

```bash
docker compose up --build -d
docker compose exec web python manage.py migrate
```

- Frontend: http://localhost:5173
- API root: http://localhost:8000/api/
- Django admin: http://localhost:8000/admin/

Stop the services with `docker compose down`. Database data is stored in the named `postgres_data` volume; use `docker compose down -v` only if you intentionally want to delete that data.

## Run the frontend separately

```bash
cd frontend
npm install
npm run dev
```

Vite serves the frontend at http://localhost:5173 by default.

## Run the backend separately

The backend expects PostgreSQL. Start a compatible PostgreSQL instance and configure the `POSTGRES_*` values from `backend/.env.example` for that instance.

```bash
cd backend
python -m venv .venv
```

Activate the virtual environment, then install the backend requirements:

```bash
pip install -r requirements.txt
```

Copy `.env.example` to `.env` if you have not already. From `backend/booking_backend`, load the values from `backend/.env` into your shell, then run:

```bash
python manage.py migrate
python manage.py runserver
```

## API routes

The API is mounted at `/api/`. Main routes include:

| Route | Purpose |
|---|---|
| `GET /api/` | API index |
| `/api/rooms/` | List and create rooms; detail routes support individual rooms |
| `/api/room-images/` | List and manage room images |
| `/api/occupancies/` | List and manage bookings |
| `/api/users/` | Authenticated user access, with staff permissions |
| `POST /api/register/` | Register a user |
| `POST /api/login/` | Obtain an authentication token |
| `POST /api/logout/` | Log out and invalidate the current token |

Room and room-image writes are restricted to staff; read operations are available without staff privileges. Booking and user routes require authentication, and ordinary users are limited to their own records. Consult the serializers and views for the exact request and response fields.

## Tests

Run the Django tests from the backend project directory with the virtual environment and database configured:

```bash
python manage.py test room_booking
```

Build-check the frontend with:

```bash
cd frontend
npm run build
```

## License

Distributed under the MIT License. See [LICENSE](LICENSE).

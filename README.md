# Booking-App

Django REST Framework backend with a React/Vite frontend for room reservations.

## Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- React
- Vite
- GitHub Actions

## Architecture

    React / Vite
         ↓
    Django REST API
         ↓
    Django ORM
         ↓
    PostgreSQL

## Features

- User registration and token authentication
- Room management and room images
- Booking creation and management
- Booking ownership and staff permissions
- Booking date validation
- Overlapping-booking prevention
- API tests
- Frontend production build
- GitHub Actions CI

## Run backend

    cd backend
    python -m venv .venv
    pip install -r requirements.txt
    cp .env.example .env
    python booking_backend/manage.py migrate
    python booking_backend/manage.py runserver

API: `http://127.0.0.1:8000/api/`

## Run frontend

    cd frontend
    npm install
    npm run dev

## Tests

    python backend/booking_backend/manage.py test room_booking
    cd frontend
    npm run build

## Technical focus

Full-stack application practice with Django REST Framework, PostgreSQL, authentication, database validation, API testing, and a separate React frontend.

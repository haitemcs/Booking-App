# Booking App Frontend

React + Vite frontend for the Django REST booking API.

## Run locally

From this directory:

```bash
npm install
npm run dev
```

The Vite development server proxies `/api` and `/media` to `http://127.0.0.1:8000`.

Start Django separately from `backend/booking_backend`:

```bash
python manage.py runserver
```

Then open the Vite URL shown in the terminal.

## Backend API used

- `GET /api/rooms/`
- `GET /api/rooms/:id/`
- `POST /api/register/`
- `POST /api/login/`
- `POST /api/logout/`
- `GET /api/occupancies/`
- `POST /api/occupancies/`

Authentication uses the Django REST Framework token returned by login/register.

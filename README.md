# NEXO Super App

A comprehensive super app for Nepal providing services for travel, health, agriculture, education, payments, and more.

## Features

- **Authentication**: JWT-based authentication with secure password hashing
- **User Management**: User profiles, contacts, and role-based access control
- **Travel Services**: Browse travel packages and destinations
- **Health Services**: Access health clinics and book appointments
- **Agricultural Support**: Get farming advice, market prices, and equipment rentals
- **Education**: Browse and enroll in courses
- **Chat Assistant**: AI-powered chat using OpenAI
- **Nexo Paisa**: Integrated payment system
- **Calendar**: Manage events and appointments
- **Admin Dashboard**: Administrative tools and analytics

## Setup

### Prerequisites

- Python 3.8+
- MySQL 5.7+ or MariaDB 10.3+
- pip (Python package manager)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/harshalg-a11y/NEXO.git
cd NEXO
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Create a `.env` file based on `.env.example`:
```bash
cp .env.example .env
```

4. Edit `.env` and configure your settings:
```env
SECRET_KEY=your-secret-key-here
JWT_SECRET_KEY=your-jwt-secret-key-here
DB_HOST=localhost
DB_PORT=3306
DB_USERNAME=your_db_user
DB_PASSWORD=your_db_password
DB_DATABASE=nexo
OPENAI_API_KEY=your-openai-api-key  # Optional, for chat feature
```

### Database Setup

1. Create the database:
```sql
CREATE DATABASE nexo CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. Run migrations:
```bash
alembic upgrade head
```

### Running the Application

Start the development server:
```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at `http://localhost:8000`

API documentation:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the test suite:
```bash
pytest
```

Run tests with coverage:
```bash
pytest --cov=app --cov-report=html
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `SECRET_KEY` | Secret key for sessions | - | Yes |
| `JWT_SECRET_KEY` | JWT token secret | Uses SECRET_KEY | No |
| `JWT_ALGORITHM` | JWT algorithm | HS256 | No |
| `JWT_ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiration time | 30 | No |
| `DB_HOST` | Database host | localhost | Yes |
| `DB_PORT` | Database port | 3306 | Yes |
| `DB_USERNAME` | Database username | root | Yes |
| `DB_PASSWORD` | Database password | - | Yes |
| `DB_DATABASE` | Database name | nexo | Yes |
| `OPENAI_API_KEY` | OpenAI API key for chat | - | No |
| `OPENAI_MODEL` | OpenAI model to use | gpt-3.5-turbo | No |
| `MAIL_FROM` | Sender email address | noreply@example.com | No |
| `MAIL_HOST` | SMTP server host | smtp.example.com | No |
| `MAIL_PORT` | SMTP server port | 587 | No |
| `MAIL_USERNAME` | SMTP username | - | No |
| `MAIL_PASSWORD` | SMTP password | - | No |
| `NEXO_PAISA_API_KEY` | Nexo Paisa API key | - | No |
| `NEXO_PAISA_WEBHOOK_SECRET` | Nexo Paisa webhook secret | - | No |

## API Endpoints

### Authentication
- `POST /auth/register` - Register a new user
- `POST /auth/login` - Login and get JWT token
- `GET /auth/me` - Get current user info

### Users
- `GET /users` - List all users (admin only)
- `GET /users/me` - Get current user profile
- `PUT /users/me` - Update current user profile
- `GET /users/{user_id}` - Get specific user
- `GET /users/{user_id}/contacts` - Get user contacts
- `GET /users/{user_id}/bookings/cars` - Get user car bookings
- `GET /users/{user_id}/bookings/hotels` - Get user hotel bookings
- `GET /users/{user_id}/transactions` - Get user transactions

### Travel
- `GET /travel/packages` - List travel packages
- `GET /travel/packages/{package_id}` - Get package details
- `GET /travel/destinations` - List destinations

### Health
- `GET /health/status` - Get health services info
- `GET /health/appointments` - List appointments
- `GET /health/records` - Get health records

### Agriculture
- `GET /agro/advice` - Get farming advice
- `GET /agro/markets` - Get market prices
- `GET /agro/equipment` - List equipment

### Education
- `GET /education/courses` - List courses
- `GET /education/courses/{course_id}` - Get course details
- `GET /education/enrollments` - List enrollments
- `GET /education/resources` - List resources

### Chat
- `POST /chat/message` - Send message to AI assistant

### Nexo Paisa
- `POST /nexo-paisa/pay` - Initiate payment
- `POST /nexo-paisa/webhook` - Handle payment webhook
- `GET /nexo-paisa/transactions/{transaction_id}` - Get transaction

### Calendar
- `GET /calendar/events` - List events
- `GET /calendar/events/{event_id}` - Get event details
- `GET /calendar/upcoming` - Get upcoming events

### Admin
- `GET /admin/dashboard` - Admin dashboard (admin only)
- `GET /admin/users/stats` - User statistics (admin only)
- `GET /admin/transactions/stats` - Transaction stats (admin only)
- `GET /admin/system/health` - System health (admin only)

## Project Structure

```
NEXO/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application entry point
│   ├── config.py            # Configuration settings
│   ├── db.py                # Database connection
│   ├── security.py          # Authentication utilities
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── contact.py
│   │   ├── car.py
│   │   ├── car_booking.py
│   │   ├── hotel_booking.py
│   │   └── nexo_paisa_transaction.py
│   ├── schemas/             # Pydantic schemas
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── contact.py
│   │   ├── booking.py
│   │   ├── nexo_paisa.py
│   │   └── chat.py
│   ├── routers/             # API route handlers
│   │   ├── auth.py
│   │   ├── user.py
│   │   ├── travel.py
│   │   ├── health.py
│   │   ├── agro.py
│   │   ├── education.py
│   │   ├── chat.py
│   │   ├── nexo_paisa.py
│   │   ├── calendar.py
│   │   └── admin.py
│   └── services/            # Business logic services
│       ├── mailer.py
│       ├── openai_service.py
│       └── nexo_paisa_service.py
├── alembic/                 # Database migrations
│   └── versions/
├── tests/                   # Test suite
│   ├── conftest.py
│   ├── test_auth.py
│   └── test_routers.py
├── static/                  # Static files
├── templates/               # HTML templates
├── requirements.txt         # Python dependencies
├── alembic.ini             # Alembic configuration
├── .env.example            # Environment variables example
└── README.md               # This file
```

## Development

### Creating a Migration

After modifying models:
```bash
alembic revision --autogenerate -m "Description of changes"
alembic upgrade head
```

### Code Style

This project follows PEP 8 style guidelines. Format your code before committing:
```bash
black app/ tests/
```

## License

Copyright © 2024 NEXO. All rights reserved.
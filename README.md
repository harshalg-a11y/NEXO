# NEXO - All-in-One Platform

NEXO is a comprehensive FastAPI-based web application providing travel booking, health consultation, agriculture advice, education resources, AI chat, digital wallet (Nexo Paisa), and more.

## Features

- 🚗 **Travel Booking**: Book cars and hotels
- 🏥 **Health Consultation**: AI-powered health information
- 🌾 **Agriculture Advice**: Plant care and farming guidance
- 📚 **Education**: Access courses and learning materials
- 💬 **AI Chat**: Interactive AI assistant
- 💰 **Nexo Paisa**: Digital wallet for payments and transfers
- 📅 **Calendar**: Event scheduling and management
- 🔐 **Session-based Authentication**: Secure login with CSRF protection
- 🌓 **Light/Dark Theme**: Cozy UI with theme toggle

## Technology Stack

- **Backend**: FastAPI (Python)
- **Database**: SQLAlchemy ORM (supports MySQL/SQLite)
- **Templates**: Jinja2
- **Frontend**: Alpine.js for interactivity
- **Styling**: Custom CSS with light/dark themes
- **Authentication**: Session-based with itsdangerous
- **Security**: CSRF protection, password hashing with bcrypt

## Prerequisites

- Python 3.8+
- MySQL database (or SQLite for development)
- pip (Python package manager)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/harshalg-a11y/NEXO.git
   cd NEXO
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and update the configuration:
   - Set `SECRET_KEY`, `SESSION_SECRET_KEY`, and `CSRF_SECRET_KEY` to secure random values
   - Configure `DATABASE_URL` for your database
   - Optionally set `OPENAI_API_KEY` for AI features
   - Configure SMTP settings for email notifications

4. **Initialize database**
   
   The application will automatically create tables on first run using SQLAlchemy's `Base.metadata.create_all()`.
   
   For production, consider setting up Alembic for database migrations:
   ```bash
   pip install alembic
   alembic init alembic
   # Configure alembic.ini and create migrations
   ```

## Running the Application

### Development Mode

```bash
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Or using the main script:

```bash
python app/main.py
```

The application will be available at `http://localhost:8000`

### Production Mode

For production deployment, use a production-grade ASGI server:

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Or with Gunicorn:

```bash
pip install gunicorn
gunicorn app.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Project Structure

```
NEXO/
├── app/
│   ├── main.py              # FastAPI application entrypoint
│   ├── config.py            # Configuration management
│   ├── database.py          # Database setup and session
│   ├── security.py          # Authentication and CSRF utilities
│   ├── models/              # SQLAlchemy models
│   │   ├── user.py
│   │   ├── contact.py
│   │   ├── car.py
│   │   ├── booking.py
│   │   └── nexo_paisa.py
│   ├── schemas/             # Pydantic schemas
│   │   └── auth.py
│   ├── routers/             # API route handlers
│   │   ├── auth.py
│   │   ├── dashboard.py
│   │   ├── travel.py
│   │   ├── health.py
│   │   ├── agro.py
│   │   ├── education.py
│   │   ├── chat.py
│   │   ├── nexo_paisa.py
│   │   ├── calendar.py
│   │   └── admin.py
│   └── services/            # Service integrations
│       ├── openai_service.py
│       └── mailer_service.py
├── templates/               # Jinja2 templates
│   ├── base.html
│   ├── welcome.html
│   ├── login.html
│   ├── dashboard.html
│   ├── travel.html
│   ├── health.html
│   ├── agro.html
│   ├── education.html
│   ├── chat.html
│   ├── load_nexo_paisa.html
│   ├── calendar.html
│   ├── admin.html
│   └── error.html
├── static/
│   └── css/
│       └── app.css          # Custom CSS with themes
├── requirements.txt
├── .env.example
└── README.md
```

## Configuration

### Database Configuration

**MySQL** (Production):
```env
DATABASE_URL=mysql+pymysql://username:password@localhost:3306/nexo_db
```

**SQLite** (Development):
```env
DATABASE_URL=sqlite:///./nexo.db
```

### Security Configuration

Generate secure keys for production:

```python
import secrets
print(secrets.token_urlsafe(32))  # For SECRET_KEY
print(secrets.token_urlsafe(32))  # For SESSION_SECRET_KEY
print(secrets.token_urlsafe(32))  # For CSRF_SECRET_KEY
```

### OpenAI Integration (Optional)

For AI chat and health consultation features:
```env
OPENAI_API_KEY=sk-your-api-key-here
```

### Email Configuration (Optional)

For email notifications:
```env
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password
SMTP_FROM=noreply@nexo.com
```

## API Endpoints

### Authentication
- `GET /login` - Login page
- `POST /login` - Submit login
- `GET /register` - Registration page
- `POST /register` - Submit registration
- `GET /logout` - Logout

### Main Features
- `GET /` - Welcome page
- `GET /dashboard` - User dashboard
- `GET /travel` - Travel booking
- `GET /health` - Health consultation
- `GET /agro` - Agriculture advice
- `GET /education` - Education resources
- `GET /chat` - AI chat
- `GET /nexo-paisa` - Digital wallet
- `GET /calendar` - Calendar/events
- `GET /admin` - Admin dashboard (admin only)

### Utility
- `GET /health-check` - Health check endpoint

## Default Admin Setup

To create an admin user, you can use Python to add a user directly to the database:

```python
from app.database import SessionLocal
from app.models.user import User
from passlib.context import CryptContext

db = SessionLocal()
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

admin = User(
    email="admin@nexo.com",
    password_hash=pwd_context.hash("your-secure-password"),
    full_name="Admin User",
    is_admin=True
)
db.add(admin)
db.commit()
```

## Development Notes

- **CSRF Protection**: All state-changing routes (POST/PUT/DELETE) require CSRF tokens
- **Session Management**: Uses signed cookies for session management
- **Password Security**: Passwords are hashed using bcrypt
- **Database**: Currently uses `Base.metadata.create_all()` for table creation. For production, implement Alembic migrations
- **Service Stubs**: OpenAI and mailer services are implemented but may need additional configuration
- **Static Files**: Additional assets can be added to the `static/` directory

## Future Enhancements

- [ ] Implement Alembic for database migrations
- [ ] Add comprehensive test suite
- [ ] Implement payment gateway integration
- [ ] Add real-time notifications with WebSockets
- [ ] Implement advanced admin features
- [ ] Add API documentation with Swagger/OpenAPI
- [ ] Implement rate limiting
- [ ] Add logging and monitoring
- [ ] Docker containerization

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is provided as-is for educational and development purposes.

## Support

For issues and questions, please open an issue on the GitHub repository.
# Xero Integration API with Django

## Table of Contents
- [Features](#features)
- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [API Endpoints](#api-endpoints)
- [Usage Examples](#usage-examples)
- [Project Structure](#project-structure)
- [Code Implementation](#code-implementation)
- [Running the Project](#running-the-project)
- [Testing](#testing)
- [Deployment](#deployment)
- [Troubleshooting](#troubleshooting)
- [License](#license)

---

## Features 🚀
- ✅ Complete OAuth 2.0 implementation for Xero
- ✅ JWT authentication for API users
- ✅ Multi-user support with data isolation
- ✅ Chart of Accounts synchronization
- ✅ Token refresh handling
- ✅ Bulk database operations for performance
- ✅ Comprehensive error handling

---

## Requirements 🛠️
- Python 3.10.16
- Django 4.0+
- Django REST Framework 3.14+
- Xero developer account
- PostgreSQL (recommended for production)

---

## Installation 📥

### 1. Clone the repository:
```bash
git clone git@github.com:jabeenshres/xero_integration.git
cd xero_integration
```

### 2. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate    # Windows
```

### 3. Install dependencies:
```bash
pip install -r requirements.txt
```

---

## Configuration ⚙️

### Environment Variables 🌍
Create a `.env` file in the project root:
```ini
SECRET_KEY=your-django-secret-key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database
DB_ENGINE=django.db.backends.postgresql
DB_NAME=xero_integration
DB_USER=postgres
DB_PASSWORD=postgres
DB_HOST=localhost
DB_PORT=5432

# Xero Configuration
XERO_CLIENT_ID=your-client-id
XERO_CLIENT_SECRET=your-client-secret
XERO_REDIRECT_URI=http://localhost:8000/api/v1/xero/callback/
XERO_SCOPES=openid profile email accounting.transactions accounting.settings
XERO_AUTH_URL=https://login.xero.com/identity/connect/authorize
XERO_TOKEN_URL=https://identity.xero.com/connect/token
XERO_CONNECTIONS_URL=https://api.xero.com/connections
XERO_API_BASE_URL=https://api.xero.com/api.xro/2.0
XERO_ACCOUNTS_URL=https://api.xero.com/api.xro/2.0/Accounts
```

### Django Settings 🛠️
Update `settings.py`:
```python
INSTALLED_APPS = [
    ...
    'rest_framework',
    'rest_framework_simplejwt',
    'xero_auth',
    'xero_data',
    'authentication'
]

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    )
}

# Xero Configuration
XERO_CONFIG = {
    'CLIENT_ID': os.getenv('XERO_CLIENT_ID'),
    'CLIENT_SECRET': os.getenv('XERO_CLIENT_SECRET'),
    'REDIRECT_URI': os.getenv('XERO_REDIRECT_URI'),
    'SCOPES': os.getenv('XERO_SCOPES').split(),
}
```

---

## API Endpoints 🌐

### **Authentication**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/auth/register/` | POST | User registration |
| `/api/v1/auth/login/` | POST | User login (JWT tokens) |
| `/api/v1/auth/token/refresh/` | POST | Refresh JWT token |

### **Xero Integration**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/xero/login/` | GET | Initiate Xero OAuth flow |
| `/api/v1/xero/callback/` | GET | Xero OAuth callback |
| `/api/v1/xero/refresh/` | GET | Refresh Xero tokens |

### **Chart of Accounts**
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/xero/accounts/fetch/` | GET | Fetch and sync Chart of Accounts |

---

## Usage Examples 📌

### 1. User Registration
```bash
curl -X POST http://localhost:8000/api/v1/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123", "email": "test@example.com"}'
```

### 2. User Login
```bash
curl -X POST http://localhost:8000/api/v1/auth/login/ \
  -H "Content-Type: application/json" \
  -d '{"username": "testuser", "password": "testpass123"}'
```

### 3. Fetch Chart of Accounts
```bash
curl -X GET http://localhost:8000/api/v1/xero/accounts/fetch/ \
  -H "Authorization: Bearer your_jwt_token"
```

---

## Running the Project 🚀

### Apply migrations:
```bash
python manage.py migrate
```

### Create a superuser:
```bash
python manage.py createsuperuser
```

### Run development server:
```bash
python manage.py runserver
```

Access the API at [http://localhost:8000/](http://localhost:8000/)

---

## Testing 🧪
Run the test suite with:
```bash
python manage.py test
```

---

## Deployment 🚀
For production deployment:
- Set `DEBUG=False` in settings
- Configure a production database (PostgreSQL recommended)
- Set up HTTPS with a valid certificate
- Configure proper CORS settings
- Use a production WSGI server (Gunicorn + Nginx)

---

## Troubleshooting 🛠️

| Issue | Solution |
|--------|-----------|
| Xero authentication fails | Verify redirect URI matches exactly in Xero developer portal |
| Token refresh issues | Check refresh token hasn't expired |
| Database errors | Verify database connection settings |
| CORS errors | Ensure proper CORS headers are set |

---

## License 📜
This project is licensed under the **MIT License**.

---

This `README.md` provides a structured, well-formatted guide covering everything needed for setting up, configuring, and using the **Xero Integration API with Django**. 🚀


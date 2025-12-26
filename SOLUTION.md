# Mini CRM Solution

## Overview

This is a full-stack CRM application built with Django REST Framework backend and Vue.js frontend. The solution demonstrates modern web development practices with a clean separation of concerns, RESTful API design, and responsive Material Design UI.

## Architecture

### Backend (Django)
- **Framework**: Django 4.2.7 with Django REST Framework
- **Database**: SQLite for simplicity
- **Authentication**: Token-based authentication
- **API**: RESTful endpoints for all CRUD operations

### Frontend (Vue.js)
- **Framework**: Vue 3 with Composition API
- **UI Library**: Vuetify 3 (Material Design)
- **Build Tool**: Vite for fast development
- **HTTP Client**: Axios for API communication

## Key Features Implemented

1. **Authentication System**
   - Secure login/logout with token authentication
   - Protected routes and API endpoints

2. **Dashboard**
   - Real-time statistics and analytics
   - Overview of companies, contacts, deals, and tasks

3. **Contact Management**
   - Full CRUD operations for contacts
   - Company association and contact details

4. **Company Management**
   - Company profiles with industry and contact information
   - Relationship tracking with contacts and deals

5. **Deal Pipeline**
   - Deal tracking through different stages
   - Amount and close date management

6. **Task Management**
   - Task creation with priorities and due dates
   - Assignment to contacts and deals

7. **Campaign Management**
   - Marketing campaign creation and tracking
   - Campaign performance monitoring
   - Integration with contacts and deals

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Node.js 16 or higher
- npm or yarn package manager

### Backend Setup

1. **Navigate to backend directory**
   ```bash
   cd backend
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

5. **Start development server**
   ```bash
   python manage.py runserver
   ```

   Backend will be available at `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend directory**
   ```bash
   cd frontend
   ```

2. **Install dependencies**
   ```bash
   npm install
   ```

3. **Start development server**
   ```bash
   npm run dev
   ```

   Frontend will be available at `http://localhost:5173`

### Demo Credentials
- **Username**: demo
- **Password**: demo123

## Technical Decisions

### Backend Choices
- **SQLite**: Chosen for simplicity and portability
- **Token Authentication**: Stateless authentication suitable for API-first architecture
- **Django REST Framework**: Provides robust serialization and viewsets

### Frontend Choices
- **Vue 3**: Modern reactive framework with excellent developer experience
- **Vuetify 3**: Material Design components for consistent UI
- **Vite**: Fast build tool with hot module replacement
- **Axios**: Promise-based HTTP client with interceptors for auth

### Design Patterns
- **Repository Pattern**: Service layer for API calls
- **Component Composition**: Reusable Vue components
- **RESTful API**: Standard HTTP methods and status codes

## Project Structure

```
UnityMiniCRM/
├── backend/
│   ├── config/              # Django settings
│   │   ├── settings.py
│   │   ├── asgi.py
│   │   ├── urls.py
│   │   └── wsgi.py
│   ├── tasks/               # Main CRM app
│   │   ├── models.py        # Database models
│   │   ├── serializers.py   # API serializers
│   │   ├── views.py         # API views
│   │   └── urls.py          # URL routing
│   ├── fixtures/            # Demo data
│   ├── manage.py
│   └── requirements.txt
│
└── frontend/
    ├── src/
    │   ├── components/      # Reusable components
    │   ├── views/           # Page components
    │   ├── services/        # API service layer
    │   ├── router/          # Vue Router config
    │   ├── plugins/         # Vuetify setup
    │   └── assets/          # Static assets
    ├── package.json
    └── vite.config.js
```

## API Documentation

All endpoints are prefixed with `/api/` and require authentication except login.

### Authentication
- `POST /api/auth/register/` - Sign up with username/password/email(optional)
- `POST /api/auth/login/` - Login with username/password
- `POST /api/auth/logout/` - Logout and invalidate token

### Resources
- Companies: `/api/companies/`
- Contacts: `/api/contacts/`
- Deals: `/api/deals/`
- Tasks: `/api/tasks/`
- Campaigns: `/api/campaigns/`
- Dashboard: `/api/dashboard/stats/`

All resource endpoints support standard CRUD operations (GET, POST, PUT, DELETE).

## Development Workflow

1. **Start both servers** (backend on :8000, frontend on :5173)
2. **Login** with demo credentials
3. **Explore features** through the web interface
4. **API testing** available at `http://localhost:8000/api/`

## Production Considerations

For production deployment:
- Use PostgreSQL instead of SQLite
- Configure proper CORS settings
- Set up environment variables for secrets
- Use a proper web server (nginx + gunicorn)
- Implement proper logging and monitoring
- Add input validation and rate limiting

## Testing

The application includes:
- Django unit tests for models and API endpoints
- Vue component tests
- API integration tests

Run backend tests:
```bash
cd backend
python manage.py test
```

## Future Enhancements

- Email integration for notifications
- File upload for contacts/companies
- Advanced filtering and search
- Export functionality (CSV, PDF)
- Real-time updates with WebSockets
- Mobile app with React Native

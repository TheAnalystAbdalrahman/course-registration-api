# Course Registration API

A production-ready RESTful API for managing academic course registrations, built with FastAPI and PostgreSQL. The system provides comprehensive functionality for managing departments, courses, students, and enrollments with role-based access control, prerequisite validation, and seat availability management.

## 🚀 Features

- **Department Management**: Create and manage academic departments
- **Course Management**: Full CRUD operations with pagination, filtering, and search
- **Student Management**: Student registration and profile management
- **Enrollment System**: 
  - Prerequisite validation
  - Seat availability checking
  - Soft delete (drop/re-enroll support)
  - Duplicate prevention
- **Authentication & Authorization**: 
  - JWT-based authentication
  - Role-based access control (Admin, Faculty, Student)
- **Health Monitoring**: Dedicated health check endpoint for deployment validation
- **Interactive API Documentation**: Auto-generated Swagger UI at `/docs`

## 🏗️ Architecture

- **Backend Framework**: FastAPI (Python 3.10+)
- **Database**: PostgreSQL (hosted on Supabase)
- **ORM**: SQLAlchemy 2.0
- **Migrations**: Alembic
- **Authentication**: JWT tokens with python-jose
- **Password Hashing**: bcrypt via passlib
- **Containerization**: Docker
- **Deployment**: Render (Web Service) + Supabase (PostgreSQL)

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL 15+ (or access to Supabase)
- Docker and Docker Compose (for local development)
- Git

## 🛠️ Installation

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd course-registration-api
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   Create a `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql://postgres:postgres@localhost:5432/course_reg_db
   SECRET_KEY=your-secret-key-change-in-production-min-32-characters-long
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=30
   DEBUG=true
   PORT=8000
   ```

5. **Run database migrations**
   ```bash
   alembic upgrade head
   ```

6. **Start the development server**
   ```bash
   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

### Docker Development

1. **Build and start services**
   ```bash
   docker-compose up --build
   ```

   The API will be available at `http://localhost:8000`

2. **Run migrations** (if needed)
   ```bash
   docker-compose exec api alembic upgrade head
   ```

## 📚 API Documentation

Once the server is running, access the interactive API documentation:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 🔐 Authentication

### Register a User (Admin only)

```bash
POST /api/auth/register
Authorization: Bearer <admin-token>
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword",
  "role": "student",
  "student_id": 1  # Optional, for student users
}
```

### Login

```bash
POST /api/auth/login
Content-Type: application/x-www-form-urlencoded

username=user@example.com&password=securepassword
```

Or using JSON:

```bash
POST /api/auth/login-json
Content-Type: application/json

{
  "email": "user@example.com",
  "password": "securepassword"
}
```

Response:
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

### Using the Token

Include the token in the Authorization header:
```
Authorization: Bearer <your-token>
```

## 🎯 User Roles

- **Admin**: Full system access
  - Create departments, courses, students
  - Manage users
  - View all data
  
- **Faculty**: Course and student management
  - Create and update courses
  - View enrolled students
  - View course availability
  
- **Student**: Self-service enrollment
  - View available courses
  - Enroll in courses (subject to prerequisites and availability)
  - View own enrollments
  - Drop enrollments

## 📡 API Endpoints

### Health Check
- `GET /health` - Health check endpoint (no authentication required)

### Authentication
- `POST /api/auth/register` - Register new user (Admin only)
- `POST /api/auth/login` - Login and receive JWT token
- `POST /api/auth/login-json` - Login using JSON body
- `GET /api/auth/me` - Get current user information

### Departments
- `GET /api/departments` - List all departments
- `POST /api/departments` - Create department (Admin only)

### Courses
- `GET /api/courses` - List courses (with pagination, filtering, sorting)
- `GET /api/courses/{course_id}` - Get course by ID
- `POST /api/courses` - Create course (Admin/Faculty)
- `PUT /api/courses/{course_id}` - Update course (Admin/Faculty)
- `DELETE /api/courses/{course_id}` - Delete course (Admin only)
- `GET /api/courses/{course_id}/students` - Get enrolled students (Admin/Faculty)
- `GET /api/courses/{course_id}/availability` - Get seat availability

### Students
- `GET /api/students` - List students (Admin/Faculty)
- `GET /api/students/{student_id}` - Get student by ID
- `POST /api/students` - Create student (Admin only)
- `GET /api/students/{student_id}/enrollments` - Get student enrollments

### Enrollments
- `POST /api/enrollments` - Create enrollment
- `DELETE /api/enrollments/{enrollment_id}` - Drop enrollment

### Prerequisites
- `GET /api/prerequisites` - List all prerequisites
- `POST /api/prerequisites` - Create prerequisite (Admin/Faculty)
- `DELETE /api/prerequisites/{prerequisite_id}` - Delete prerequisite (Admin/Faculty)

## 🗄️ Database Schema

The database consists of the following main tables:

- **departments**: Academic departments
- **courses**: Course offerings with department association
- **students**: Student records
- **enrollments**: Student-course enrollment relationships (with soft delete)
- **course_prerequisites**: Prerequisite relationships between courses
- **users**: Authentication and authorization data

See the [project report](course_registration_api_report.tex) for detailed schema documentation.

## 🔄 Database Migrations

Migrations are managed using Alembic:

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
```

## 🚢 Deployment

### Render Deployment

1. **Connect Repository**: Link your GitHub repository to Render
2. **Create Web Service**: 
   - Build Command: `docker build -t course-registration-api .`
   - Start Command: `python entrypoint.py`
3. **Set Environment Variables**:
   - `DATABASE_URL`: PostgreSQL connection string from Supabase
   - `SECRET_KEY`: Strong secret key (min 32 characters)
   - `ALGORITHM`: `HS256`
   - `ACCESS_TOKEN_EXPIRE_MINUTES`: `30`
   - `PORT`: Provided by Render (defaults to 8000)
4. **Health Check**: Set to `/health`

### Supabase Setup

1. Create a new PostgreSQL project on Supabase
2. Copy the connection string
3. Add it as `DATABASE_URL` in Render environment variables
4. Migrations run automatically via the entrypoint script

## 🧪 Testing

### Manual Testing

Use the interactive Swagger UI at `/docs` or tools like Postman/curl:

```bash
# Health check
curl http://localhost:8000/health

# Login
curl -X POST http://localhost:8000/api/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=admin@example.com&password=password"

# Get courses (with token)
curl http://localhost:8000/api/courses \
  -H "Authorization: Bearer <token>"
```

## 📁 Project Structure

```
course-registration-api/
├── alembic/              # Database migrations
│   └── versions/         # Migration files
├── app/
│   ├── middleware/       # Authentication middleware
│   ├── models/           # SQLAlchemy models
│   ├── routers/          # API route handlers
│   ├── schemas/          # Pydantic schemas
│   ├── services/         # Business logic layer
│   ├── config.py         # Configuration
│   ├── database.py       # Database connection
│   ├── exceptions.py     # Custom exceptions
│   └── main.py           # FastAPI application
├── scripts/              # Utility scripts
├── Dockerfile            # Docker image definition
├── docker-compose.yml    # Local development setup
├── entrypoint.py         # Production entrypoint
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

## 🔒 Security Features

- Password hashing with bcrypt
- JWT token-based authentication
- Role-based access control
- SQL injection prevention via SQLAlchemy ORM
- Environment variable-based configuration
- HTTPS/TLS in production (via Render)

## 🐛 Troubleshooting

### Database Connection Issues

- Verify `DATABASE_URL` is correctly set
- Check database is accessible from your network
- Ensure database credentials are correct

### Migration Errors

- Check database connection before running migrations
- Verify migration files are in correct order
- Review Alembic logs for specific errors

### Port Already in Use

- Change the `PORT` environment variable
- Or stop the process using port 8000

## 📝 License

This project is developed for academic purposes.

## 👤 Author

**ABDALRAHMAN SIDDIG ALI BASHIR**

## 📄 Documentation

For detailed project documentation, see:
- [Project Report (LaTeX)](course_registration_api_report.tex) - Comprehensive technical documentation
- [API Documentation](http://localhost:8000/docs) - Interactive API reference (when server is running)

## 🤝 Contributing

This is an academic project. For questions or issues, please contact the author.

## 🔮 Future Enhancements

- Automated testing suite (unit, integration, e2e)
- CI/CD pipeline
- Email notifications
- Waitlist system for full courses
- Advanced reporting and analytics
- Rate limiting
- API versioning

---

**Version**: 1.0.0  
**Last Updated**: 2025

# DevFest Lecce 2025 - Backend

This is the backend API for the DevFest Lecce 2025 conference application. It's built with Django and Django REST Framework, providing endpoints for managing conferences, speakers, badges, user connections, and leaderboards.

## 🚀 Features

- **User Management**: Firebase-based authentication for secure user access
- **Conference Management**: Manage conference details, rooms, and schedules
- **Speaker Profiles**: CRUD operations for speaker information
- **Badge System**: Gamification with collectible badges and points
- **Connections**: Network with other attendees
- **Leaderboard**: Track user points and rankings
- **RESTful API**: Well-documented API with Swagger/OpenAPI support
- **Admin Interface**: Django admin panel for easy data management

## 📋 Prerequisites

- Python 3.10 or higher
- PostgreSQL (for production) or SQLite (for development)
- [uv](https://github.com/astral-sh/uv) - Fast Python package installer
- Firebase project (for authentication)
- Google Cloud Storage bucket (optional, for media storage)

## 🛠️ Installation

### 1. Clone the repository

```bash
git clone https://github.com/riccardotornesello/devfest-lecce-be.git
cd devfest-lecce-be
```

### 2. Install dependencies

```bash
uv sync
```

### 3. Set up environment variables

Copy the example environment file and configure it:

```bash
cp .env.example .env
```

Edit `.env` with your configuration:

- `SECRET_KEY`: Django secret key (generate one for production)
- `DEBUG`: Set to `false` in production
- `ALLOWED_HOSTS`: Your domain(s)
- `FIREBASE_AUDIENCE`: Your Firebase project ID
- `POSTGRES_*`: Database credentials (if using PostgreSQL)
- `GS_BUCKET_NAME`: Google Cloud Storage bucket (optional)

### 4. Run migrations

```bash
cd devfest_lecce_2025_be
uv run manage.py migrate
```

### 5. Create a superuser (optional)

```bash
uv run manage.py createsuperuser
```

### 6. Start the development server

```bash
uv run manage.py runserver
```

The API will be available at `http://localhost:8000`

## 📚 API Documentation

Once the server is running, you can access the API documentation at:

- **Swagger UI**: `http://localhost:8000/swagger/`
- **ReDoc**: `http://localhost:8000/redoc/`
- **Admin Panel**: `http://localhost:8000/admin/`

## 🧪 Development

### Code Quality

This project uses `ruff` for linting and formatting:

```bash
# Format code
uv run ruff format

# Lint and auto-fix
uv run ruff check --fix
```

### Git Hooks

Install pre-commit hooks to automatically lint and format on commit:

```bash
uv run pre-commit install
```

## 🏗️ Project Structure

```
devfest_lecce_2025_be/
├── app/                 # Core Django settings and configuration
├── badges/              # Badge system app
├── conferences/         # Conference management app
├── connections/         # User connections app
├── leaderboard/         # Points and rankings app
├── rooms/               # Conference rooms app
├── speakers/            # Speaker profiles app
└── users/               # User management app
```

## 🐳 Docker

Build and run with Docker:

```bash
docker build -t devfest-lecce-be .
docker run -p 8000:8000 --env-file .env devfest-lecce-be
```

## ☁️ Deployment

### Google Cloud Platform

This project is configured for deployment on Google Cloud Run. See `cloudbuild.yaml` for the CI/CD pipeline configuration.

```bash
# Build and deploy
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_ARTIFACT_REGISTRY="europe-west1-docker.pkg.dev/devfest-lecce/devfest-lecce",_SERVICE_REGION="europe-west1"
```

### Environment Variables for Production

Ensure the following environment variables are set in your production environment:

- `SECRET_KEY`: A strong, random secret key
- `DEBUG=false`
- `ALLOWED_HOSTS`: Your production domain(s)
- `CORS_ALLOWED_ORIGINS`: Your frontend domain(s)
- `CSRF_TRUSTED_ORIGINS`: Your frontend domain(s)
- Database credentials
- `FIREBASE_AUDIENCE`: Your Firebase project ID
- `GS_BUCKET_NAME`: For media storage (if using Google Cloud Storage)

## 🔐 Security

This application follows security best practices:

- **No hardcoded secrets**: All sensitive data is loaded from environment variables
- **HTTPS enforcement**: In production, all traffic is redirected to HTTPS
- **Security headers**: XSS protection, content type nosniff, and frame options
- **CSRF protection**: Enabled for all state-changing operations
- **CORS configuration**: Properly configured allowed origins
- **Firebase authentication**: Secure token-based authentication
- **SQL injection protection**: Django ORM provides protection by default
- **Password validation**: Strong password requirements enforced

### Security Checklist for Production

- [ ] Set `DEBUG=false`
- [ ] Use a strong, unique `SECRET_KEY`
- [ ] Configure `ALLOWED_HOSTS` with your specific domains
- [ ] Set up HTTPS/SSL certificates
- [ ] Configure `CORS_ALLOWED_ORIGINS` to only allow your frontend
- [ ] Use a production-grade database (PostgreSQL)
- [ ] Set up regular database backups
- [ ] Keep dependencies up to date
- [ ] Monitor application logs
- [ ] Set up rate limiting if needed

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Run tests and linting (`uv run ruff check --fix`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## 📝 License

This project is part of DevFest Lecce 2025.

## 👥 Authors

- **Riccardo Tornesello** - [riccardo.tornesello@gmail.com](mailto:riccardo.tornesello@gmail.com)

## 🙏 Acknowledgments

- DevFest Lecce organizing team
- Google Developers Group Lecce
- All contributors to this project

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the development team.

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

### GitHub Workflows

This repository includes two GitHub Actions workflows for development purposes:

1. **CI Workflow** (`.github/workflows/ci.yml`): Runs on push and pull requests
   - Lints and formats code with ruff
   - Runs security scans
   - Validates Django configuration
   - Tests Docker build

2. **Release Workflow** (`.github/workflows/release.yml`): Runs on release creation
   - Builds Docker image
   - Publishes to GitHub Container Registry
   - Creates build attestation for supply chain security

**Note:** These workflows are for reference and development testing only. They validate code quality and ensure the Docker image builds correctly, but they do not deploy to production.

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

### Using Docker Compose (Recommended for local development)

The easiest way to run the application with all dependencies:

```bash
# Start all services (database and web server)
docker-compose up

# Run migrations (in another terminal)
docker-compose run migrate

# Stop all services
docker-compose down

# Remove all data
docker-compose down -v
```

The API will be available at `http://localhost:8000`

### Using Docker directly

Build and run with Docker:

```bash
docker build -t devfest-lecce-be .
docker run -p 8000:8000 --env-file .env devfest-lecce-be
```

## ☁️ Deployment

### Production Deployment Pipeline

**The production deployment is fully automated using Google Cloud Build.** On every push to the `main` branch, Cloud Build automatically:

1. **Builds the Docker image** and pushes it to Artifact Registry
2. **Updates the Cloud Run Job** with the new image
3. **Runs database migrations** via the Cloud Run Job (`TASK=migrate`)
4. **Collects static files** via the Cloud Run Job (`TASK=collectstatic`)
5. **Deploys the backend service** to Cloud Run with the new image

The pipeline is configured in `cloudbuild.yaml` and is triggered automatically by a Cloud Build trigger set up through Terraform (see Infrastructure section below).

**Manual Trigger (if needed):**

```bash
gcloud builds submit --config cloudbuild.yaml \
  --substitutions=_ARTIFACT_REGISTRY="europe-west1-docker.pkg.dev/devfest-lecce/devfest-lecce",_SERVICE_REGION="europe-west1"
```

### GitHub Container Registry (Optional - For Development)

Docker images can also be published to GitHub Container Registry through the release workflow. This is useful for development and testing purposes:

**Creating a Release:**

```bash
# Create and push a tag
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Then create a release on GitHub from the tag
```

The workflow automatically publishes the image to:
- `ghcr.io/riccardotornesello/devfest-lecce-be:latest`
- `ghcr.io/riccardotornesello/devfest-lecce-be:1.0.0`
- `ghcr.io/riccardotornesello/devfest-lecce-be:1.0`
- `ghcr.io/riccardotornesello/devfest-lecce-be:1`

**Pulling the Image:**

```bash
docker pull ghcr.io/riccardotornesello/devfest-lecce-be:latest
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

## 🏗️ Infrastructure

The entire Google Cloud infrastructure is managed with **Terraform** and is located in the `infrastructure/` directory.

**⚠️ Important: Terraform should only be executed once during initial setup.** It provisions all the necessary infrastructure including:

- Google Cloud Project Services (Artifact Registry, Cloud Build, Cloud Run, SQL Admin)
- Artifact Registry repository for Docker images
- Cloud Storage bucket for media files
- Cloud SQL (PostgreSQL) database instance
- Cloud Run service for the backend API
- Cloud Run job for migrations and static file collection
- Load balancer with SSL certificate
- Cloud Build trigger (automatic deployment on push to `main`)
- Service accounts and IAM permissions

### Initial Infrastructure Setup

1. **Prerequisites:**
   - Google Cloud Project created
   - Terraform installed (`terraform` CLI)
   - Google Cloud SDK installed and authenticated (`gcloud auth application-default login`)
   - GitHub repository connected to Google Cloud Build

2. **Configure variables:**

   Create a `terraform.tfvars` file in the `infrastructure/` directory:

   ```hcl
   project       = "your-gcp-project-id"
   region        = "europe-west1"
   repository_id = "devfest-lecce"
   bucket_name   = "devfest-lecce-media"
   db_password   = "your-secure-database-password"
   domain        = "api.devfest.gdglecce.it"
   repo_owner    = "riccardotornesello"
   repo_name     = "devfest-lecce-be"
   ```

3. **Initialize and apply Terraform:**

   ```bash
   cd infrastructure
   terraform init
   terraform plan  # Review the infrastructure changes
   terraform apply  # Apply the changes (type 'yes' to confirm)
   ```

4. **Post-setup:**
   - Once applied, Terraform will output important values like database connection details
   - The Cloud Build trigger will automatically deploy on every push to `main`
   - Manual intervention should not be needed unless infrastructure changes are required

For detailed information about the infrastructure components, see the [infrastructure README](infrastructure/README.md).

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

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Authors

- **Riccardo Tornesello** - [riccardo.tornesello@gmail.com](mailto:riccardo.tornesello@gmail.com)

## 🙏 Acknowledgments

- DevFest Lecce organizing team
- Google Developers Group Lecce
- All contributors to this project

## 📞 Support

For issues and questions, please open an issue on GitHub or contact the development team.

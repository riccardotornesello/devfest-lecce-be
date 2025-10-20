# Infrastructure Documentation

This directory contains Terraform configurations for provisioning and managing the Google Cloud infrastructure for the DevFest Lecce 2025 Backend application.

## ⚠️ Important Notice

**This Terraform configuration should only be executed once during the initial infrastructure setup.** Once the infrastructure is provisioned, it manages itself through the Cloud Build pipeline that automatically deploys changes on every push to the `main` branch.

## 📋 Overview

The infrastructure is organized into modular components:

```
infrastructure/
├── main.tf           # Main infrastructure configuration and orchestration
├── variables.tf      # Input variables for configuration
├── backend/          # Cloud Run service and job configuration
├── db/               # Cloud SQL PostgreSQL database
└── storage/          # Google Cloud Storage bucket for media files
```

## 🏗️ Infrastructure Components

### 1. Google Cloud Services

Enables the following APIs required for the application:
- **Artifact Registry** - Docker image storage
- **Cloud Build** - CI/CD pipeline
- **Cloud Run** - Serverless container deployment
- **Cloud SQL Admin** - Managed PostgreSQL database
- **Compute Engine** - Load balancer and networking

### 2. Artifact Registry

- **Repository**: Docker container registry
- **Format**: Docker
- **Location**: Configurable region (default: `europe-west1`)
- **Purpose**: Stores the backend Docker images built by Cloud Build

### 3. Cloud Storage (Module: `storage/`)

- **Bucket**: Media file storage
- **Access**: Public read access for media files
- **Uniform bucket-level access**: Enabled for consistent permissions
- **Purpose**: Stores user-uploaded images and static files

**Configuration** (`storage/main.tf`):
- Creates a Google Cloud Storage bucket
- Enables uniform bucket-level access
- Grants public read access (`roles/storage.objectViewer`)

### 4. Cloud SQL Database (Module: `db/`)

- **Database**: PostgreSQL 17
- **Instance Type**: `db-f1-micro` (Enterprise edition)
- **Deletion Protection**: Enabled to prevent accidental deletion
- **Purpose**: Stores application data

**Configuration** (`db/main.tf`):
- Creates a Cloud SQL instance
- Creates a database within the instance
- Creates a user with credentials

### 5. Cloud Run Backend (Module: `backend/`)

#### Cloud Run Service
- **Name**: `devfest-lecce-be`
- **Container**: Django REST API
- **Port**: 8000
- **Ingress**: Public (all traffic allowed)
- **Database Connection**: Cloud SQL Unix socket (`/cloudsql/`)
- **Storage**: Connected to Cloud Storage bucket
- **Public Access**: Enabled for all users

#### Cloud Run Job
- **Name**: `devfest-lecce-be-job`
- **Purpose**: Runs database migrations and static file collection
- **Timeout**: 60 seconds
- **Tasks**: 
  - `TASK=migrate` - Runs Django migrations
  - `TASK=collectstatic` - Collects static files to Cloud Storage

**Environment Variables** (configured in `backend/main.tf`):
- `GS_BUCKET_NAME` - Cloud Storage bucket name
- `POSTGRES_DB` - Database name
- `POSTGRES_USER` - Database user
- `POSTGRES_PASSWORD` - Database password
- `POSTGRES_HOST` - Cloud SQL Unix socket path
- `POSTGRES_PORT` - Database port (5432)
- `ALLOWED_HOSTS` - Django allowed hosts
- `CORS_ALLOWED_ORIGINS` - CORS configuration
- `CSRF_TRUSTED_ORIGINS` - CSRF trusted origins

**Service Account**:
- Custom service account (`gcf-devfest-lecce-be-runner`)
- Permissions:
  - `roles/cloudsql.editor` - Access to Cloud SQL
  - `roles/storage.objectUser` - Access to Cloud Storage

### 6. Load Balancer

- **Type**: HTTPS Load Balancer with SSL
- **SSL Certificate**: Managed SSL certificate for the domain
- **HTTPS Redirect**: Enabled (HTTP traffic redirected to HTTPS)
- **Backend**: Cloud Run service via serverless NEG (Network Endpoint Group)
- **CDN**: Disabled (not needed for API)

### 7. Cloud Build Configuration

#### Service Account
- **Name**: `cloudbuild-sa`
- **Purpose**: Executes Cloud Build pipelines
- **Permissions**:
  - `roles/iam.serviceAccountUser` - Act as service accounts
  - `roles/editor` - Modify resources
  - `roles/logging.logWriter` - Write logs

#### Cloud Build Trigger
- **Name**: `devfest-lecce-backend-build`
- **Trigger**: Automatic on push to `main` branch
- **Configuration**: Uses `cloudbuild.yaml` from repository
- **GitHub Integration**: Connected to the repository
- **Logs**: Included with build status

**Substitutions**:
- `_ARTIFACT_REGISTRY` - Full path to Artifact Registry
- `_SERVICE_REGION` - Deployment region

## 🚀 Initial Setup

### Prerequisites

Before running Terraform, ensure you have:

1. **Google Cloud Project** created and billing enabled
2. **Terraform** installed (v1.0 or higher)
3. **Google Cloud SDK** installed and authenticated:
   ```bash
   gcloud auth application-default login
   ```
4. **GitHub Repository** connected to Google Cloud Build
5. **Required permissions** in the Google Cloud Project:
   - Project Editor or Owner
   - Service Account Admin
   - Cloud Build Editor

### Configuration

1. Create a `terraform.tfvars` file in this directory:

```hcl
# Google Cloud Project Configuration
project       = "your-gcp-project-id"
region        = "europe-west1"

# Artifact Registry
repository_id = "devfest-lecce"

# Cloud Storage
bucket_name   = "devfest-lecce-media"

# Database
db_password   = "your-secure-database-password"  # Use a strong password!

# Domain
domain        = "api.devfest.gdglecce.it"

# GitHub Repository (optional, defaults are set)
repo_owner    = "riccardotornesello"
repo_name     = "devfest-lecce-be"
```

2. **Security Note**: Never commit `terraform.tfvars` to version control. It's already in `.gitignore`.

### Execution

```bash
# Navigate to the infrastructure directory
cd infrastructure

# Initialize Terraform (downloads providers and modules)
terraform init

# Preview the infrastructure changes
terraform plan

# Apply the infrastructure (creates all resources)
terraform apply

# Type 'yes' when prompted to confirm
```

### Outputs

After successful application, Terraform will output:

- Database connection name
- Backend service URL
- Storage bucket name
- Artifact Registry repository path

## 🔄 Post-Setup

After the initial Terraform setup:

1. **Automatic Deployments**: Every push to `main` triggers Cloud Build
2. **Pipeline Execution**: Cloud Build follows the steps in `cloudbuild.yaml`:
   - Builds Docker image
   - Pushes to Artifact Registry
   - Updates Cloud Run Job
   - Runs migrations and collects static files
   - Updates Cloud Run Service

3. **No Manual Intervention Needed**: The infrastructure manages itself

## 🛠️ Maintenance

### When to Run Terraform Again

You should only run Terraform again if you need to:

- Change infrastructure configuration (e.g., instance size, region)
- Add new resources (e.g., additional databases, buckets)
- Update IAM permissions
- Modify environment variables in the Cloud Run service/job
- Update the domain or SSL configuration

### Making Infrastructure Changes

1. Modify the relevant `.tf` files
2. Run `terraform plan` to preview changes
3. Run `terraform apply` to apply changes
4. Review the changes carefully before confirming

### Destroying Infrastructure

**⚠️ Warning**: This will delete all resources and data!

```bash
# Preview what will be destroyed
terraform plan -destroy

# Destroy all infrastructure
terraform destroy
```

Note: The Cloud SQL instance has deletion protection enabled. You'll need to disable it first or use the `-target` flag to exclude it.

## 📝 Variables Reference

| Variable | Type | Description | Default |
|----------|------|-------------|---------|
| `project` | string | Google Cloud Project ID | *Required* |
| `region` | string | Deployment region | `europe-west1` |
| `repository_id` | string | Artifact Registry repository ID | *Required* |
| `bucket_name` | string | Cloud Storage bucket name | *Required* |
| `db_password` | string | Database password | *Required* |
| `domain` | string | Domain for SSL certificate | *Required* |
| `repo_owner` | string | GitHub repository owner | `riccardotornesello` |
| `repo_name` | string | GitHub repository name | `devfest-lecce-be` |

## 🔐 Security Considerations

1. **Database Password**: Use a strong, unique password and store it securely
2. **Service Accounts**: Follow principle of least privilege
3. **IAM Permissions**: Regularly audit and review permissions
4. **SSL/TLS**: Managed certificates are automatically renewed
5. **Secrets**: Never commit `terraform.tfvars` or state files to version control
6. **State Management**: Consider using a remote backend (e.g., Google Cloud Storage) for team collaboration

## 🤔 Troubleshooting

### Common Issues

**Issue**: "API not enabled" errors
- **Solution**: Wait a few minutes after applying, then re-run `terraform apply`

**Issue**: Cloud Build trigger not working
- **Solution**: Ensure GitHub repository is connected to Google Cloud Build in the console

**Issue**: Database connection failures
- **Solution**: Verify the Cloud SQL Unix socket path is correctly mounted in Cloud Run

**Issue**: Permission denied errors
- **Solution**: Check that service accounts have the correct IAM roles

### Getting Help

1. Check Terraform logs for detailed error messages
2. Review Google Cloud Console for resource status
3. Check Cloud Build logs for deployment issues
4. Verify environment variables in Cloud Run console

## 📚 Additional Resources

- [Terraform Google Provider Documentation](https://registry.terraform.io/providers/hashicorp/google/latest/docs)
- [Google Cloud Run Documentation](https://cloud.google.com/run/docs)
- [Google Cloud Build Documentation](https://cloud.google.com/build/docs)
- [Google Cloud SQL Documentation](https://cloud.google.com/sql/docs)

## Useful commands

- Install packages: uv sync
- Format project: uv run ruff format
- Lint and fix project: uv run ruff check --fix
- Start Django dev server: cd devfest_lecce_2025_be && uv run manage.py runserver

## Build

```bash
gcloud builds submit --config cloudbuild.yaml --substitutions=_ARTIFACT_REGISTRY="europe-west1-docker.pkg.dev/devfest-lecce/devfest-lecce",_SERVICE_REGION="europe-west1",_SERVICE_NAME="devfest-lecce-backend",COMMIT_SHA=dev
```

## TODO

- Log levels
- Postgres configuration
- Docker compose
- Pipeline and git hooks

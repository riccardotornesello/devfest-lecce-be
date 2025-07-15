## Useful commands

- Install packages: uv sync
- Format project: uv run ruff format
- Lint and fix project: uv run ruff check --fix
- Start Django dev server: cd devfest_lecce_2025_be && uv run manage.py runserver
- Install git hooks: uv run pre-commit install

## Build

```bash
gcloud builds submit --config cloudbuild.yaml --substitutions=_ARTIFACT_REGISTRY="europe-west1-docker.pkg.dev/devfest-lecce/devfest-lecce",_SERVICE_REGION="europe-west1"
```

## Pipeline

Note: to save on the registry price, all the images are tagged with the "latest" tag.

## TODO

- Postgres configuration
- Docker compose
- Automatic pipeline

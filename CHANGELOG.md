# Changelog

## v1.0.2

- Added `profile = "black"` to isort configuration
- Added `SENTRY_ENVIRONMENT` which gives the possibility to set a specific sentry environment for issues

## v1.0.1

- Renamed `queue.yml` chart to `rabbitmq.yml`
- Updated to Python 3.9
- Updated `README.md`
- Used `entrypoint.sh` in `Dockerfile` so that kubernetes environments could also use it

## v1.0.0

- Initial release
- Uses Python 3.9
- Uses FastAPI 0.54
- Uses `Poetry` as package manager
- Added linting & autoformatting via `black`, `isort`, `flake8`, `mypy`
- Added code metrics analysis via `radon` (Maintainability index, Cyclomatic complexity)
- Uses `Pytest` for testing
- Uses `alembic` for migrations management
- Uses `SQLAlchemy` as database toolkit
- Uses `Pydantic` for data structures schema

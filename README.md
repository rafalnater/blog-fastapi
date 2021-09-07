# FastAPI Project Template

## Services

This template consists of the following services:

* `fastapi` - the FastAPI-based application
* `postgres` - PostgreSQL database
* `worker` - Celery worker
* `beat` - Celery-beat scheduler
* `rabbitmq` - RabbitMQ message broker
* `bootstrap` - a container that runs only at the startup and exits when finishes executing all commands (e.g. applies adatabase migrations)

## Main tools used

* [FastAPI][1] - the framework used
* [SQLAlchemy][2] - a database toolkit
* [Pydantic][3] - data structure schemas
* [Alembic][4] - migrations tool
* [Pytest][5] - testing framework
* [Poetry][6] - dependency management tool

## Usage

### Project set up

1. Clone this repository.
2. Update dependencies if needed.
3. Remove `.git/` directory.
4. Attach remote to a repository of your new project.
5. Set up the `.env` file basing on `.env.example` contents.
6. Write the code.

### Workflow

You can take advantage of the `make` commands that were especially prepared to make your workflow even smoother.

#### Database migrations

- `make migrations-generate` - generates new database migrations
- `make migrations-apply` - applies all migrations that weren't already applied
- `make migrations-rollback` - rollbacks all migrations to the initial state

#### Code quality

- `make format` - runs code auto-formatters ([`black`][9], [`isort`][10])
- `make lint` - runs code linting ([`black`][9], [`isort`][10], [`flake8`][11], [`mypy`][12])
- `make test` - runs all available tests and produces tests coverage report
- `make metrics` - produces code quality metrics using [`radon`][13] ([Maintainability index][7], [Cyclomatic complexity][8])

[1]: https://fastapi.tiangolo.com/
[2]: https://www.sqlalchemy.org/
[3]: https://pydantic-docs.helpmanual.io/
[4]: https://alembic.sqlalchemy.org/en/latest/
[5]: https://pytest.org/
[6]: https://python-poetry.org/
[7]: https://en.wikipedia.org/wiki/Maintainability#Software_engineering
[8]: https://en.wikipedia.org/wiki/Cyclomatic_complexity
[9]: https://github.com/psf/black
[10]: https://github.com/PyCQA/isort
[11]: https://flake8.pycqa.org/en/latest/
[12]: https://mypy.readthedocs.io/en/stable/
[13]: https://radon.readthedocs.io/
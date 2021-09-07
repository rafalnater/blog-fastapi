#!/bin/sh
set -e

if [ "$1" = 'runserver' ]; then
    shift
    exec python -m uvicorn main:app --reload --host 0.0.0.0 --port 8000 $@
elif [ "$1" = 'worker' ]; then
    shift
    exec celery --app worker worker --loglevel info --queues main-queue --concurrency 1 $@
elif [ "$1" = 'beat' ]; then
    shift
    exec celery --app worker beat --loglevel info $@
elif [ "$1" = 'test' ]; then
    shift
    exec pytest $@
elif [ "$1" = 'lint' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black --check --diff $OPTS || EXIT=$?
    echo "-- isort --" && isort -c --diff $OPTS || EXIT=$?
    echo "-- flake8 --" && flake8 $OPTS || EXIT=$?
    MYPY_OPTS=${@:-'src/'}
    echo "-- mypy --" && mypy $MYPY_OPTS || EXIT=$?
    exit ${EXIT:-0}
elif [ "$1" = 'metrics' ]; then
    shift
    SOURCE_PATH=${@:-'src/'}
    echo "-- cyclomatic complexity --" && radon cc $SOURCE_PATH || EXIT=$?
    echo "-- maintainability index --" && radon mi $SOURCE_PATH || EXIT=$?
    exit ${EXIT:-0}
elif [ "$1" = 'fmt' ]; then
    shift
    OPTS=${@:-'.'}
    echo "-- black --" && black $OPTS
    echo "-- isort --" && isort --atomic $OPTS
    exit 0
elif [ "$1" = 'bootstrap' ]; then
    shift
    exec alembic upgrade head
elif [ "$1" = 'gunicorn' ]; then
    shift
    exec gunicorn --bind 0.0.0.0:8000 --worker-class uvicorn.workers.UvicornWorker main:app
fi

exec "$@"

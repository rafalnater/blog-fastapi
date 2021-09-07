PROJECT_NAME=fastapi
BACKEND_CONTAINER_NAME=backend
COMPOSE_RUN=docker-compose run --rm $(BACKEND_CONTAINER_NAME)

migrations-generate:
	$(COMPOSE_RUN) alembic revision --autogenerate -m "$(filter-out $@,$(MAKECMDGOALS))"

migrations-apply:
	$(COMPOSE_RUN) alembic upgrade head

migrations-rollback:
	$(COMPOSE_RUN) alembic downgrade base

lint:
	$(COMPOSE_RUN) lint

format:
	$(COMPOSE_RUN) fmt

test:
	$(COMPOSE_RUN) test

metrics:
	$(COMPOSE_RUN) metrics

%: # Ignore unknown commands and extra params
	@:

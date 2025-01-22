DOCKER_COMPOSE = docker compose

migrate:
	@$(DOCKER_COMPOSE) exec fastapi alembic upgrade head

run:
	@$(DOCKER_COMPOSE) up

down:
	@$(DOCKER_COMPOSE) down

build:
	@$(DOCKER_COMPOSE) up --build

install: run migrate

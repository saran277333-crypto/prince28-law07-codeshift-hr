.PHONY: install lint test cov run up down

install:
	uv sync --locked

lint:
	uv run poe lint

test:
	uv run pytest

cov:
	uv run poe cov

run:
	uv run uvicorn codeshift_hr.api.main:app --reload

up:
	docker compose up --build -d

down:
	docker compose down

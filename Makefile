.PHONY: run deps-up deps-down lint exec logs locale-gen locale-compile env

run:
	docker compose -f docker-compose.yaml up -d --build
	python main.py

deps-up:
	docker compose -f docker-compose.yaml up -d --build

deps-down:
	docker compose -f docker-compose.yaml down

lint:
	isort --profile black .
	black .

exec:
	docker compose -f docker-compose.yaml exec -it $(name) bash

logs:
	docker compose -f docker-compose.yaml logs -f $(name)
env:
	export $(cat .env | xargs)


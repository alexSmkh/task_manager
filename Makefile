build:
	docker build -t task-manager .

run:
	docker compose up

dc-build:
	docker compose build

dc-api-bash:
	docker compose run --rm --service-ports api /bin/bash

dc-api-migrate:
	docker compose run --rm api bash -c 'python manage.py migrate'

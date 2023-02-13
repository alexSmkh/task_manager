build:
	docker build -t task-manager .

dc-build:
	docker compose build

dc-api-bash:
	docker compose run --rm --service-ports api /bin/bash
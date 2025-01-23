build:
	docker compose up --build -d --remove-orphans

up:
	docker compose up -d

down:
	docker compose down

down-v:
	docker compose down -v

migrate:
	docker compose exec api python3 manage.py migrate

makemigrations:
	docker compose exec api python3 manage.py makemigrations

superuser:
	docker compose exec api python3 manage.py createsuperuser

collectstatic:
	docker compose exec api python3 manage.py collectstatic --no-input --clear
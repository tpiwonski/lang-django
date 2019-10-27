build:
	docker-compose build
up:
	docker-compose up -d
down:
	docker-compose down
stop:
	docker-compose stop
start-db:
	docker-compose start database
stop-db:
	docker-compose stop database
dump-db:
	docker-compose exec database pg_dump -U lang -F p lang
drop-db:
	docker-compose exec database dropdb -U lang lang
create-db:
	docker-compose exec database createdb -U lang lang
migrate:
	docker-compose run --rm backend python manage.py migrate

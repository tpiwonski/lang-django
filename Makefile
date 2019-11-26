build:
	docker-compose build
up:
	docker-compose up
down:
	docker-compose down
stop:
	docker-compose stop
start-db:
	docker-compose start database
stop-db:
	docker-compose stop database
dump-db:
	docker-compose exec database pg_dump -U lang -F p $(LANG_DB_NAME)
drop-db:
	docker-compose exec database dropdb -U lang $(LANG_DB_NAME)
drop-db-name:
	docker-compose exec database dropdb -U lang $(name)
create-db:
	docker-compose exec database createdb -U lang $(LANG_DB_NAME)
list-db:
	docker-compose exec database psql -U lang -c "\l"
migrations:
	docker-compose run --rm backend /usr/bin/env python manage.py makemigrations --name $(name)
migrate:
	docker-compose run --rm backend /usr/bin/env python manage.py migrate
dev:
	docker-compose.exe -f docker-compose.dev.yaml up -d

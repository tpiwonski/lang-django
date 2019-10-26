FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /lang-django

WORKDIR /lang-django

COPY Pipfile* /lang-django/

RUN pip install pipenv
RUN pipenv install --system --deploy

COPY . /lang-django

# ENV DJANGO_SETTINGS_MODULE langsite.settings.docker

EXPOSE 8000

CMD /usr/bin/env python manage.py migrate && \
	/usr/bin/env python manage.py runserver 0.0.0.0:8000 --nothreading --noreload
#	/usr/bin/env gunicorn langsite.wsgi:application --bind 0.0.0.0:8000 --workers=1 --reload
#    pipenv run python manage.py runserver 0.0.0.0:8000 --nothreading --noreload

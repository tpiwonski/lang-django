FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /lang-django

WORKDIR /lang-django

COPY Pipfile* /lang-django/

RUN pip install pipenv && \
    pipenv install

COPY . /lang-django

ENV DJANGO_SETTINGS_MODULE langsite.settings.docker

EXPOSE 8000

CMD pipenv run python manage.py migrate && \
    pipenv run python manage.py runserver 0.0.0.0:8000 --nothreading --noreload

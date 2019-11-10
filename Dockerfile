FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /lang-django

WORKDIR /lang-django

COPY Pipfile /lang-django
COPY Pipfile.lock /lang-django

RUN pip install pipenv==2018.11.26
RUN pipenv install --system --deploy

COPY . /lang-django

# ENV DJANGO_SETTINGS_MODULE langsite.settings.docker

EXPOSE 8000

# ENTRYPOINT /usr/bin/env python manage.py migrate && \
#		   /usr/bin/env gunicorn langsite.wsgi:application --bind 0.0.0.0:8000 --log-file - --access-logfile -

CMD ["/usr/bin/env", "gunicorn", "langsite.wsgi:application", "--bind", "0.0.0.0:8000", "--log-file", "-", "--access-logfile", "-"]

#	/usr/bin/env python manage.py runserver 0.0.0.0:8000 --nothreading --noreload
#	/usr/bin/env gunicorn langsite.wsgi:application --bind 0.0.0.0:8000 --workers=1 --reload

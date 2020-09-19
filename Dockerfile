FROM python:3.8-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # install pipenv
  && pip install pipenv \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*

WORKDIR /opt/dictionary

ARG DEVEL=no

RUN pip --no-cache-dir --disable-pip-version-check install --upgrade pip setuptools wheel

COPY Pipfile Pipfile.lock ./

RUN if [ "$DEVEL" = "yes" ] ; then pipenv install --dev --system ; else pipenv install --deploy --system ; fi
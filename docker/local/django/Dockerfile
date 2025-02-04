FROM python:3.12.7-slim-bookworm as python

# Stage 1: Build dependency wheels
FROM python AS python-build-stage

ARG BUILD_ENVIRONMENT=local

RUN apt-get update && apt-get install --no-install-recommends -y \
    build-essential \
    libpq-dev

COPY ./requirements .

RUN pip wheel --wheel-dir /usr/src/app/wheels \
    -r ${BUILD_ENVIRONMENT}.txt

# Stage 2: Run Stage
FROM python AS python-run-stage

ARG BUILD_ENVIRONMENT=local

ARG APP_HOME=/app

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    BUILD_ENV=${BUILD_ENVIRONMENT}

WORKDIR ${APP_HOME}

RUN apt-get update && apt-get install --no-install-recommends -y \
    libpq-dev gettext \
    && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
    && rm -rf /var/lib/apt/lists/*

COPY --from=python-build-stage /usr/src/app/wheels /wheels/

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels/

COPY ./docker/local/django/entrypoint.sh /entrypoint
COPY ./docker/local/django/start.sh /start
COPY ./docker/local/django/celery/worker/start.sh /start-celeryworker
COPY ./docker/local/django/celery/flower/start.sh /start-flower

RUN sed -i 's/\r$//g' /entrypoint /start /start-celeryworker /start-flower && \
    chmod +x /entrypoint /start /start-celeryworker /start-flower

ENTRYPOINT [ "/entrypoint"]
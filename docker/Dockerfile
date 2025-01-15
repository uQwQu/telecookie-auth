FROM python:3.10-slim

WORKDIR /app

COPY . /app/

RUN pip install --no-cache-dir -r requirements.txt

COPY ./docker/start.sh /start

RUN sed -i 's/\r$//g' /start && chmod +x /start
FROM python:3.9.5-slim-buster

EXPOSE 5000
EXPOSE 5432

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV FLASK_ENV="development"

RUN apt-get update \ 
    && apt-get -y install libpq-dev gcc \
    && pip install psycopg2

COPY requirements.txt .
RUN python -m pip install -r requirements.txt

WORKDIR /app
COPY . /app

RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

CMD ["flask", "run", "--host", "0.0.0.0"]
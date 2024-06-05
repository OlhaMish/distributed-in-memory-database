FROM python:3.10-slim

LABEL authors="olya"

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root

COPY . /app
EXPOSE 5000

CMD ["poetry", "run", "python", "server.py"]

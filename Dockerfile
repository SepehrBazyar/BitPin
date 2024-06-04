FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /src

COPY pyproject.toml poetry.lock /src/

RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y python3-pip && \
    pip install poetry

RUN poetry install --no-root

COPY . /src/

EXPOSE 8000

CMD ["poetry", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]

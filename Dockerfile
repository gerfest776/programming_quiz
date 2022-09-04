FROM python:3.10-slim-buster

ENV PYTHONUNBUFFERED 1

WORKDIR /application
COPY poetry.lock pyproject.toml /application/

ENV PYTHONPATH=/application

RUN apt-get update \
    && apt-get -y install gcc g++ apt-transport-https \
                          ca-certificates curl gnupg \
                           --no-install-recommends
    \

RUN pip install --upgrade pip poetry \
    && poetry config virtualenvs.create false \
    && poetry install --no-dev \
    && rm -rf /root/.cache/pip
    \

COPY . /application
WORKDIR /application

RUN chmod +x ./entrypoint.sh


ENTRYPOINT ["./entrypoint.sh"]

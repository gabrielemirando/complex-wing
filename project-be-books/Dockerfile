FROM python:3.12-slim

# Configure and install Poetry

ENV POETRY_VERSION=1.8.3
ENV POETRY_HOME=/opt/poetry
ENV POETRY_VENV=/opt/poetry-venv
ENV POETRY_CACHE_DIR=/opt/.cache

ENV PATH="${PATH}:${POETRY_VENV}/bin"

RUN python3 -m venv $POETRY_VENV \
	&& $POETRY_VENV/bin/pip install -U pip setuptools \
	&& $POETRY_VENV/bin/pip install poetry==${POETRY_VERSION}

# Install dependencies

WORKDIR /usr/src

COPY . .

RUN poetry install --sync

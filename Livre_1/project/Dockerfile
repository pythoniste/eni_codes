FROM python:3.11-rc-bullseye

SHELL ["/bin/bash", "-c"]

ENV DEBIAN_FRONTEND noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV LANG en_US.utf8
ENV TERM xterm
ARG POETRY_VERSION=1.3.2


RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y libsasl2-dev libldap2-dev libssl-dev python3-dev libxml2-dev libxslt1-dev libgflags-dev \
    libsnappy-dev zlib1g-dev libbz2-dev liblz4-dev libzstd-dev librdkafka-dev libpq-dev libgirepository1.0-dev \
    libsqlite3-dev default-libmysqlclient-dev default-libmysqld-dev libmysql++-dev libmysqlcppconn-dev \
    make g++ build-essential devscripts debhelper fakeroot locales locales-all vim net-tools \
    --no-install-recommends

ENV LC_ALL en_US.UTF-8
ENV LANG en_US.UTF-8
ENV LANGUAGE en_US.UTF-8

RUN useradd pythoniste --create-home --user-group --groups sudo --shell /bin/bash

WORKDIR /home/pythoniste

# Mise à jour de PIP
RUN pip install --no-cache-dir --upgrade pip

# Installation de Poetry
RUN pip install poetry==${POETRY_VERSION}
RUN poetry config virtualenvs.create false

# Installation des dépendances
COPY * .
RUN poetry install --no-interaction --no-ansi

RUN cd project
RUN pip install -e .

# Nettoyage des paquets debian qui ne sont plus utiles
RUN apt-get clean

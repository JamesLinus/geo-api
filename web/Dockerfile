# https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose
# https://dzone.com/articles/how-ansible-and-docker-fit

FROM python:2.7.13-onbuild

MAINTAINER Dheeraj Chand <dheeraj@mautinoa.com>

# Create an environment variable for the name of the project root

ENV INSTALL_PATH /geo_api

# Make a directory for the installation

RUN mkdir -p $INSTALL_PATH

WORKDIR $INSTALL_PATH

RUN apt-get update && apt-get install -y \
    vim \
    nano




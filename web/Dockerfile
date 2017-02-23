# https://nickjanetakis.com/blog/dockerize-a-flask-celery-and-redis-application-with-docker-compose  
# https://dzone.com/articles/how-ansible-and-docker-fit  
  
FROM python:2.7.13-onbuild  
  
MAINTAINER Dheeraj Chand <dheeraj@mautinoa.com>

ENV PYTHONPATH=/usr/local/lib/python2.7/site-packages
ENV FLASK_APP=MautinoaGeo

ENV GUNICORN_WORKERS=2
ENV GUNICORN_BACKLOG=4096
ENV GUNICORN_BIND=0.0.0.0:8000
ENV GUNICORN_ACCESSLOG=-

RUN apt-get update && apt-get install -y \
    apt-file \
    gdal-bin \
    git \
    libpq-dev \
    nano \
    python-apt \
    python-pip \
    python-psycopg2 \
    python-pycurl \
    python-setuptools \
    supervisor \
    vim \
    virtualenvwrapper 

RUN pip install gunicorn json-logging-py
RUN cd MautinoaGeo && pip install .

#RUN mkdir -p /var/log/supervisor
#COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

COPY gunicorn.conf /gunicorn.conf
COPY logging.conf /logging.conf

EXPOSE 8000

ENTRYPOINT ["gunicorn", "--config", "/gunicorn.conf", "--log-config", "/logging.conf", "-b", ":8000", "MautinoaGeo:app"]

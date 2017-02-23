FROM ubuntu:latest
MAINTAINER meredith@mautinoa.com

RUN apt-get update
RUN apt-get install -y build-essential lighttpd python-dev python-pip

ADD lighttpd.conf /etc/lighttpd/lighttpd.conf
EXPOSE 80
EXPOSE 443
VOLUME /var/www

COPY docker-entrypoint.sh /
RUN chmod +x ./docker-entrypoint.sh

ENTRYPOINT ["./docker-entrypoint.sh"]
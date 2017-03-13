# Mautinoa Geo API

This is a multi-container Docker application that provides the Python version of
Mautinoa's geolocation API, using lighttpd as frontend and Flask under gunicorn on
the backend.

## Installation

You will need:

- [docker](https://www.docker.com)
- [docker-compose](https://docs.docker.com/compose/)

To build the containers: `docker-compose build`
To launch the application: `docker-compose up -d`

That's it! Docker will fetch all the component parts. (This will take a while the first time.) The application serves the API at http://localhost:80.

You can view the logs for any component process with `docker logs <name>`, e.g., `docker logs geoapi_web_1`.

## What's inside

`docker-compose.yml` lists the four containers that make up this application.

- The `db` container is a [PostGIS](http://www.postgis.net/) database.
- The `data` container is a data volume for `db`.
- The `web` container serves the [Flask](http://flask.pocoo.org/) API on port 8000 using [gunicorn](http://gunicorn.org/). There are 2 workers by default. (For more information on settings, see below.)
- The `lighttpd` container proxies API requests on port 80 to the `web` container, using [lighttpd](https://www.lighttpd.net/).

Docker will attach these containers to a virtual network. Use `docker network inspect geoapi_default` to display the details of the network (e.g., the containers' IP addresses).

## Settings and Internals

### web

The Dockerfile for the `web` container has several environment variables that translate
into `gunicorn` settings. For example, `GUNICORN_WORKERS` sets the number of workers to use,
and `GUNICORN_BIND` sets the interface and port on which to serve the API. If you need to
add a new `gunicorn` setting, add it to the Dockerfile as another environment variable
(using the ENV instruction), uppercased and prefixed with `GUNICORN_`.

### lighttpd

The Dockerfile for the `lighttpd` container exposes ports 80 and 443. If you want to turn
off one or the other of these, you can do so in the Dockerfile, but remember that the
`ports` setting in `docker-compose.yml` will override it.

All settings for lighttpd are in `lighttpd.conf`. The `host` value in the `proxy.server` seting [must](https://redmine.lighttpd.net/projects/1/wiki/Docs_ModProxy) point to the IP address of the `web` endpoint, as assigned by Docker.

The `ENTRYPOINT` script, `docker-entrypoint.sh`, contains some minor pipe redirection
wizardry that was necessary to get [mod_accesslog](https://redmine.lighttpd.net/projects/1/wiki/Docs_ModAccesslog) working properly with `docker logs`. Do not modify this
script unless you know what you're doing or don't care about logging. Don't give the `lighttpd` container a `command` in `docker-compose.yml`, either.


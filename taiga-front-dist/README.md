moss/taiga-front-dist
====================

## Introduction

[Taiga](https://taiga.io/) is a project management platform for startups and
agile developers & designers who want a simple, beautiful tool that makes work
truly enjoyable.

This Docker image can be used for running the Taiga frontend. It works together
with the [moss/taiga-back](https://hub.docker.com/r/moss/taiga-front-dist/)
image.

[![GitHub stars](https://img.shields.io/github/stars/moss-it/taiga-docker.svg?style=flat-square)](https://github.com/moss-it/taiga-docker)
[![GitHub forks](https://img.shields.io/github/forks/moss-it/taiga-docker.svg?style=flat-square)](https://github.com/moss-it/taiga-docker)
[![GitHub issues](https://img.shields.io/github/issues/moss-it/taiga-docker.svg?style=flat-square)](https://github.com/moss-it/taiga-docker/issues)

## Quick start

A [moss/taiga-back](https://hub.docker.com/r/moss/taiga-front-dist/) container
should be linked to the taiga-front-dist container. Also connect the volumes of
this the taiga-back container if you want to serve the static files for the
admin panel.

```bash
docker run --name taiga_front_dist_container_name --link \
    taiga_back_container_name:taigaback --volumes-from \
    taiga_back_container_name moss-it/taiga-front-dist
```

## Docker-compose

For a complete taiga installation (``moss/taiga-back`` and
``moss/taiga-front-dist``) you can use this docker-compose configuration:

```bash
data:
  image: tianon/true
  volumes:
    - /var/lib/postgresql/data
    - /usr/local/taiga/media
    - /usr/local/taiga/static
    - /usr/local/taiga/logs
postgres:
  image: postgres
  environment:
    POSTGRES_USER: taiga
    POSTGRES_PASSWORD: password
  volumes_from:
    - data
taigaback:
  image: moss/taiga-back
  hostname: dev.example.com
  environment:
    SECRET_KEY: examplesecretkey
    EMAIL_USE_TLS: 'True'
    EMAIL_HOST: smtp.gmail.com
    EMAIL_PORT: 587
    EMAIL_HOST_USER: youremail@gmail.com
    EMAIL_HOST_PASSWORD: yourpassword
    LDAP_ENABLED: 'True'
    LDAP_SERVER: "ldap://openldap"
    LDAP_PORT: 389
    LDAP_BIND_DN: "cn=admin,dc=example,dc=com"
    LDAP_BIND_PASSWORD: 'securepassword'
    LDAP_SEARCH_BASE: "ou=people,cn=admin,dc=example,dc=com"
    LDAP_FULL_NAME_PROPERTY: 'cn'
  links:
    - postgres:postgres
  volumes_from:
    - data
taigafront:
  image: moss/taiga-front-dist
  hostname: dev.example.com
  links:
    - taigaback
  environment:
    LDAP_ENABLED: 'True'
  volumes_from:
    - data
  ports:
    - 0.0.0.0:80:80
```

## SSL Support

HTTPS can be enabled by setting ``SCHEME`` to ``https`` and filling ``SSL_CRT``
and ``SSL_KEY`` env variables (see Environment section below). *http* (port 80) 
requests will be redirected to *https* (port 443).

Example:

```
data:
  ...
db:
  ...
taigaback:
  image: moss-it/taiga-back:stable
  hostname: dev.example.com
  environment:
    ...
    API_SCHEME: https
    FRONT_SCHEME: https
  links:
    - db:postgres
  volumes_from:
    - data
taigafront:
  image: moss-it/taiga-front-dist:stable
  hostname: dev.example.com
  environment:
    SCHEME: https
    SSL_CRT: |
        -----BEGIN CERTIFICATE-----
        ...
        -----END CERTIFICATE-----
    SSL_KEY: |
        -----BEGIN RSA PRIVATE KEY-----
        ...
        -----END RSA PRIVATE KEY-----
  links:
    - taigaback
  volumes_from:
    - data
  ports:
    - 0.0.0.0:80:80
    - 0.0.0.0:443:443
```

## Environment variables

* ``PUBLIC_REGISTER_ENABLED`` defaults to ``true``
* ``API`` defaults to ``"/api/v1"``
* ``SCHEME`` defaults to ``http``. If ``https`` is used either
* ``SSL_CRT`` and ``SSL_KEY`` needs to be set **or** 
* ``/etc/nginx/ssl/`` volume attached with ``ssl.crt`` and ``ssl.key`` files
* ``SSL_CRT`` SSL certificate value. Valid only when ``SCHEME`` set to https.
* ``SSL_KEY`` SSL certificate key. Valid only when ``SCHEME`` set to https.
* ``LDAP_ENABLED`` defaults to ``False``, needs to be ``True`` to use ldap
  login.

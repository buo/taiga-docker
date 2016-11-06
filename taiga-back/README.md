moss-it/taiga-back
==================

## Introduction
[Taiga](https://taiga.io/) is a project management platform for startups and
agile developers & designers who want a simple, beautiful tool that makes work
truly enjoyable.

This Docker image can be used for running the Taiga backend. It works together
with the
[moss-it/taiga-front-dist](https://hub.docker.com/u/moss-it/taiga-front-dist/)
image.

[![GitHub stars](https://img.shields.io/github/stars/moss-it/taiga-docker.svg?style=flat-square)](https://github.com/moss-it/taiga-docker)
[![GitHub forks](https://img.shields.io/github/forks/moss-it/taiga-docker.svg?style=flat-square)](https://github.com/moss-it/taiga-docker)
[![GitHub issues](https://img.shields.io/github/issues/moss-it/taiga-docker.svg?style=flat-square)](https://github.com/moss-it/taiga-docker/issues)

## Quickstart

A [postgres](https://hub.docker.com/_/postgres/) container should be linked to
the taiga-back container. The taiga-back container will use the
``POSTGRES_USER`` and ``POSTGRES_PASSWORD`` environment variables that are
supplied to the postgres container.

```
docker run --name taiga_back_container_name --link postgres_container_name:postgres moss-it/taiga-back
```

## Docker-compose

For a complete taiga installation (``moss-it/taiga-back`` and
``moss-it/taiga-front-dist``) you can use this docker-compose configuration:

```
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

## Database Initialization

To initialize the database, use ``docker exec -it taiga-back bash`` and execute the following commands:

```bash
cd /usr/local/taiga/taiga-back/
python manage.py loaddata initial_user
python manage.py loaddata initial_project_templates
python manage.py loaddata initial_role
```

## Environment variables

### Basic variables
* ``SECRET_KEY`` defaults to ``"insecurekey"``, but you might want to change this.
* ``DEBUG`` defaults to ``False``
* ``TEMPLATE_DEBUG`` defaults to ``False``
* ``PUBLIC_REGISTER_ENABLED`` defaults to ``True``

### URLs for static files and media files from taiga-back:

* ``MEDIA_URL`` defaults to ``"http://$HOSTNAME/media/"``
* ``STATIC_URL`` defaults to ``"http://$HOSTNAME/static/"``

### Domain configuration:

* ``API_SCHEME`` defaults to ``"http"``. Use ``https`` if ``moss-it/taiga-front-dist`` is used and SSL enabled.
* ``API_DOMAIN`` defaults to ``"$HOSTNAME"``
* ``FRONT_SCHEME`` defaults to ``"http"``. Use ``https`` if ``moss-it/taiga-front-dist`` is used and SSL enabled.
* ``FRONT_DOMAIN`` defaults to ``"$HOSTNAME"``

### Email configuration:

* ``EMAIL_USE_TLS`` defaults to ``False``
* ``EMAIL_HOST`` defaults to ``"localhost"``
* ``EMAIL_PORT`` defaults to ``"25"``
* ``EMAIL_HOST_USER`` defaults to ``""``
* ``EMAIL_HOST_PASSWORD`` defaults to ``""``
* ``DEFAULT_FROM_EMAIL`` defaults to ``"no-reply@example.com"``

### Database configuration:

* ``POSTGRES_HOST``. Use to override database host.
* ``POSTGRES_PORT``. Use to override database port.
* ``POSTGRES_DB_NAME``. Use to override database name.
* ``POSTGRES_USER``. Use to override user specified in linked postgres container.
* ``POSTGRES_PASSWORD``. Use to override password specified in linked postgres container.

### Openldap configuration:

Full DN of the service account use to connect to LDAP server and search for login user's account entry.

If LDAP_BIND_DN is not specified, or is blank, then an anonymous bind is attempted.

* ``LDAP_ENABLED`` defaults to ``False``, needs to be ``True`` to enable ldap.
* ``LDAP_SERVER`` defaults to ``""``, ie. ``ldap://ldap.domain`` or ``ldaps://ldap.domain``
* ``LDAP_PORT`` defaults to ``389``
* ``LDAP_BIND_DN=`` defaults to ``""``, ie. ``'CN=SVC Account,OU=Service Accounts,OU=Servers,DC=example,DC=com'``
* ``LDAP_BIND_PASSWORD`` defaults to ``""``
* ``LDAP_SEARCH_BASE`` defaults to ``""``, ie. ``'OU=DevTeam,DC=example,DC=net'``
* ``LDAP_SEARCH_PROPERTY`` defaults to ``"uid"``; LDAP property used for searching, ie. login username needs to match value in uid property in LDAP.
* ``LDAP_SEARCH_SUFFIX`` defaults to ``""``, ie ``'@example.com'``
* ``LDAP_EMAIL_PROPERTY`` defaults to ``mail``
* ``LDAP_FULL_NAME_PROPERTY`` defaults to ``'cn'``

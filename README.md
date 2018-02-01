[![Build Status](https://travis-ci.org/antoinehng/pixelwalker.svg?branch=django_2.0)](https://travis-ci.org/antoinehng/pixelwalker 'Travis CI') [![Coverage Status](https://coveralls.io/repos/github/antoinehng/pixelwalker/badge.svg?branch=django_2.0)](https://coveralls.io/github/antoinehng/pixelwalker?branch=django_2.0 'Coveralls') [![](https://img.shields.io/docker/stars/antoinehng/pixelwalker.svg)](https://hub.docker.com/r/antoinehng/pixelwalker 'DockerHub') [![](https://img.shields.io/docker/pulls/antoinehng/pixelwalker.svg)](https://hub.docker.com/r/antoinehng/pixelwalker 'DockerHub')

__Warning:__ This project is not yet ready for prodcution purposes.

## How to launch and try?

_Note: the standalone Dockerfile is currently not working, please use docker-compose_ 

Using [docker-compose](https://docs.docker.com/compose/install/)

```
# GETTING THE SOURCE
# Clone the repo and make it your active directory
git clone https://github.com/antoinehng/pixelwalker ./pixelwalker
cd ./pixelwalker

# CREATE A MEDIA LIBRARY FOLDER ON YOUR HOST
# Default location is {{ repo-root }}/media_library/
# If you need to change this, go to docker-compose/docker-compose.yml 
# and change the volumes parameters for the engine and worker services
mkdir media_library

# USE DOCKER-COMPOSE
# Move to the docker-compose directory
cd docker-compose

# Build all needed docker images
docker-compose build

# Start all services
docker-compose up
```

The plateform should be accessible at http://localhost:8000


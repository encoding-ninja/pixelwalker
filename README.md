__Warning:__ _This project is not yet ready for production purposes._

## How to try?

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


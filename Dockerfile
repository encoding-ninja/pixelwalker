FROM ubuntu:latest
LABEL maintainer="github.com/antoinehng"

# Various dependencies
RUN apt-get update -yqq && apt-get install -yqq \
	build-essential software-properties-common \
	git \
	python3 python3-setuptools python3-dev python3-tk python3-pip npm
RUN npm install -g bower && ln -s /usr/bin/nodejs /usr/bin/node

# Install FFmpeg dependencies
RUN add-apt-repository ppa:mc3man/xerus-media && apt-get update
RUN apt-get install -yqq ffmpeg

# Install rabbitMQ
RUN apt-get install -yqq rabbitmq-server

# Copy pixelwalker sources
COPY ./ /pixelwalker
WORKDIR /pixelwalker

# Python dependencies
RUN pip3 install -r requirements.txt

# Bower JS+CSS dependencies
RUN bower --allow-root install

WORKDIR /pixelwalker/pixelwalker

# Install pixelwalker
RUN python3 manage.py migrate

# Load fixtures
RUN python3 manage.py loaddata AppSettings
RUN python3 manage.py loaddata TaskTypes

# Execute django test suite
RUN python3 manage.py test

# Expose web server port
EXPOSE 8000

# Start django dev server
CMD rabbitmq-server -detached && \
	celery worker -A pixelwalker -l info -Q engine,worker --detach && \
	python3 manage.py runserver 0.0.0.0:8000

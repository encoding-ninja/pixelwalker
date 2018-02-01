FROM ubuntu:latest
LABEL maintainer="github.com/antoinehng"

# Various dependencies
RUN apt-get update -yqq && apt-get install -yqq \
	build-essential software-properties-common \
	git \
	python3 python3-setuptools python3-dev python3-tk python3-pip npm

# Clone pixelwalker repo
COPY . /pixelwalker
WORKDIR /pixelwalker

# Python dependencies
RUN pip3 install -r requirements.txt

# Install FFmpeg dependencies
RUN add-apt-repository ppa:mc3man/xerus-media && \
	apt-get update
RUN apt-get install -yqq ffmpeg

# Get settings
WORKDIR /pixelwalker/pixelwalker/pixelwalker
COPY ./docker-compose/Worker/settings.py ./
COPY ./docker-compose/Worker/urls.py ./

# Launch service
WORKDIR /pixelwalker/pixelwalker
CMD celery worker -A pixelwalker -l info -Q worker -n worker@%h

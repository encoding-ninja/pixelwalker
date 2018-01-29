FROM ubuntu:latest
LABEL maintainer="github.com/antoinehng"

# Various dependencies
RUN apt-get update -yqq && apt-get install -yqq \
	build-essential \
	git \
	python3 python3-setuptools python3-dev python3-tk python3-pip npm

# Clone pixelwalker repo
RUN git clone https://github.com/antoinehng/pixelwalker.git /pixelwalker
WORKDIR /pixelwalker
RUN git checkout django_2.0 && git pull

# Python dependencies
RUN pip3 install -r requirements.txt

# Install FFmpeg dependencies
RUN apt-get install -yqq ffmpeg

# Get settings
WORKDIR /pixelwalker/pixelwalker/pixelwalker
COPY settings.py ./
COPY urls.py ./

WORKDIR /pixelwalker/pixelwalker

# Launch service
CMD sleep 10 && \
    celery -A pixelwalker worker -l info -Q worker -n worker@%h

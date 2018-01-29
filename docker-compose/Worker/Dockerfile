FROM ubuntu:latest
LABEL maintainer="github.com/antoinehng"

# Various dependencies
RUN apt-get update -yqq && apt-get install -yqq \
	build-essential \
	git \
	python3 python3-setuptools python3-dev python3-tk python3-pip npm
RUN npm install -g bower && ln -s /usr/bin/nodejs /usr/bin/node

# Install FFmpeg dependencies
RUN apt-get install -yqq ffmpeg

# Clone pixelwalker repo
RUN git clone https://github.com/antoinehng/pixelwalker.git /pixelwalker
WORKDIR /pixelwalker
RUN git checkout django_2.0 && git pull

# Python dependencies
RUN pip3 install -r requirements.txt

# Get settings
WORKDIR /pixelwalker/pixelwalker
COPY settings.py .

# Execute tests
RUN python3 manage.py test worker

# Launch service
CMD celery worker -A pixelwalker

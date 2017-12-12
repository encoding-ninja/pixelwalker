FROM ubuntu:latest
MAINTAINER Antoine Henning <henning.antoine@gmail.com>

# Essentials
RUN apt-get update -yqq && apt-get install -yqq \
	build-essential \
	git \
	python3 python3-setuptools python3-dev python3-tk python3-pip npm
RUN npm install -g bower && ln -s /usr/bin/nodejs /usr/bin/node


# PIXELWALKER

# Install FFmpeg dependencies
RUN apt-get install -yqq ffmpeg

# Clone pixelwalker repo
RUN git clone https://github.com/antoinehng/pixelwalker.git /pixelwalker
RUN cd /pixelwalker && git checkout django_2.0 && git pull

# Python dependencies
RUN cd /pixelwalker && pip3 install -r requirements.txt

# Bower JS+CSS dependencies
RUN cd /pixelwalker && bower --allow-root install


WORKDIR /pixelwalker/pixelwalker
CMD bash

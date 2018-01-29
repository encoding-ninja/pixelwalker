FROM ubuntu:latest
LABEL maintainer="github.com/antoinehng"

# Various dependencies
RUN apt-get update -yqq && apt-get install -yqq \
	build-essential \
	git \
	python3 python3-setuptools python3-dev python3-tk python3-pip npm
RUN npm install -g bower && ln -s /usr/bin/nodejs /usr/bin/node

# Clone pixelwalker repo
RUN git clone https://github.com/antoinehng/pixelwalker.git /pixelwalker
WORKDIR /pixelwalker
RUN git checkout django_2.0 && git pull

# Python dependencies
RUN pip3 install -r requirements.txt

# Bower JS+CSS dependencies
RUN bower --allow-root install

# Get settings
WORKDIR /pixelwalker/pixelwalker
COPY settings.py .

# Execute tests
RUN python3 manage.py test engine

# Launch service
CMD python3 manage.py makemigrations \
    python3 manage.py migrate \
    python3 manage.py loaddata AppSettings \
	python3 manage.py loaddata TaskTypes \
    celery worker -A pixelwalker & \
    python3 manage.py runserver 0.0.0.0:8000

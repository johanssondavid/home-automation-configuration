FROM python:3.6

MAINTAINER johanssondavid <david.a.joh@gmail.com>

RUN mkdir -p /usr/src/app
WORKDIR /usr/src/app
VOLUME /conf

RUN pip3 install 'appdaemon<3.0'

CMD [ "appdaemon", "-c", "/conf" ]


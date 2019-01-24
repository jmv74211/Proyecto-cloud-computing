
# https://hub.docker.com/r/digitalgenius/alpine-python3-pg

FROM frolvlad/alpine-python3

MAINTAINER Jonathan Martín Valera

WORKDIR /home/jmv74211

COPY src/app/user_service /home/jmv74211
COPY requirements_user-service.txt /home/jmv74211

RUN pip3 install -r requirements_user-service.txt

EXPOSE 80/tcp

ARG mongoVar
ARG passVar

ENV MONGODB_USERS_KEY=$mongoVar
ENV ENCODING_PHRASE=$passVar

CMD python3 /home/jmv74211/user_service.py

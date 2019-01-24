
# https://hub.docker.com/r/digitalgenius/alpine-python3-pg

FROM frolvlad/alpine-python3

MAINTAINER Jonathan Martín Valera

WORKDIR /home/jmv74211

COPY src/app/task_service /home/jmv74211
COPY requirements_task-service.txt /home/jmv74211

RUN pip3 install -r requirements_task-service.txt

EXPOSE 80/tcp

ARG passVar

ENV ENCODING_PHRASE=$passVar

CMD python3 /home/jmv74211/task_service.py

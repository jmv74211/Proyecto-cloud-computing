
# URL imagen de base dockerhub: https://hub.docker.com/r/frolvlad/alpine-python3

# Especifica la imagen de base que se va a utilizar
FROM frolvlad/alpine-python3

# Especifica el espacio de trabajo sobre el que va a actuar docker
WORKDIR /home/jmv74211

COPY src/app/user_service /home/jmv74211
COPY requirements_user-service.txt /home/jmv74211

RUN pip3 install -r requirements_user-service.txt

EXPOSE 80/tcp

ARG mongoVar
ARG passVar

ENV MONGODB_USERS_KEY=$mongoVar
ENV ENCODING_PHRASE=$passVar

CMD gunicorn -b :80 user_service:app

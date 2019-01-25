
# URL imagen de base dockerhub: https://hub.docker.com/r/frolvlad/alpine-python3

# Especifica la imagen de base que se va a utilizar
FROM frolvlad/alpine-python3

# Especifica el espacio de trabajo sobre el que va a actuar docker
WORKDIR /home/jmv74211

# Añade microservicio de usuarios y archivo de instalación de dependencias
COPY src/app/user_service /home/jmv74211
COPY requirements_user-service.txt /home/jmv74211

# Instala las dependencias del microservicio
RUN pip3 install -r requirements_user-service.txt

# Especifica a docker el puerto que va escuchar el contenedor.
EXPOSE 80/tcp

# Declara argumentos que se pasan al ejecutar el contenedor
ARG mongoVar
ARG passVar

# Declara variables de entorno
ENV MONGODB_USERS_KEY=$mongoVar
ENV ENCODING_PHRASE=$passVar

# Ejecuta el microservicio en el puerto 80
CMD gunicorn -b :80 user_service:app

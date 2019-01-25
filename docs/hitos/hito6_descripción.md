
# Documentación del hito 6: Contenedores para despliegue en la nube.

---

# Tabla de contenidos

---

# Introducción

Docker es hoy en día una de las mejores opciones para desplegar en contenedores separados cada uno de los microservicios de una forma más o menos independiente de la máquina subyacente, aunque no de la arquitectura.

El objetivo de este hito es familiarizarse con este tipo de infraestructura virtual que se usa generalmente para dar un acceso limitado a una aplicación o un servicio tal como un servidor web o a un usuario.

El objetivo secundario es el que el alumno tenga instaladas las herramientas necesarias para trabajar con Docker y sepa usarlas adecuadamente; también en qué casos conviene usarlas por motivos de seguridad o de conveniencia.

En primer lugar, he estado consultando varias fuentes acerca de esta tecnología. Como opinión personal, considero que la documentación de docker es bastante completa y representativa, ya que consta de una serie de ejemplos que clarifica demasiado los conceptos.

A continuación voy a referenciar la información más útil que he encontrado.

- [Tutorial](https://www.adictosaltrabajo.com/2015/07/29/docker-for-dummies/) de introducción a docker.

- [Vídeo de youtube](https://www.youtube.com/watch?v=HSyaF9KOzdk) de introducción a docker.

- [Referencia](https://docs.docker.com/v17.09/engine/reference/builder/) oficial de dockerfile.

- [Referencia](https://docs.docker.com/v17.09/engine/userguide/eng-image/dockerfile_best-practices/) de buenas prácticas a la hora de elaborar un dockerfile

---

# Tecnología empleada

## [Docker](https://www.docker.com/)

Docker es una plataforma de software que le permite crear, probar e implementar aplicaciones rápidamente. Docker empaqueta software en unidades estandarizadas llamadas contenedores que incluyen todo lo necesario para que el software se ejecute, incluidas bibliotecas, herramientas de sistema, código y tiempo de ejecución. Con Docker, se puede implementar y ajustar la escala de aplicaciones rápidamente en cualquier entorno con la certeza de saber que el código se ejecutará.

---

# Primeros pasos con Docker

Para empezar a trabajar con docker, he utilizado la siguiente [referencia](https://www.digitalocean.com/community/tutorials/como-instalar-y-usar-docker-en-ubuntu-16-04-es). En esta sección se va a describir una guía inicial de docker, empleando la referencia que se ha comentado anteriormente.

## Instalación

En primer lugar, se va a agregar la clave GPG para el repositorio oficial de Docker al sistema:

    sudo apt-key adv --keyserver hkp://p80.pool.sks-keyservers.net:80 --recv-keys 58118E89F3A912897C070ADBF76221572C52609D

A continuación se agrega el repositorio Docker a las fuentes APT:

    sudo apt-add-repository 'deb https://apt.dockerproject.org/repo ubuntu-xenial main'

Después se actualiza la base de datos de paquetes, con los paquetes Docker desde el repositorio recién agregado:

    sudo apt-get update

Comprobamos que vamos a realizar la instalación desde el repositorio de docker y no del predeterminado de ubuntu.

    apt-cache policy docker-engine

La salida que he obtenido es la siguiente:

![img](1)

Se observa como docker-engine no está instalado.

A continuación se procede a instalarlo mediante:

    sudo apt-get install -y docker-engine

Docker ahora debe estar instalado, el daemon iniciado, y el proceso habilitado para iniciar en el arranque.

Comprobamos el estado del servicio:

![img](2)

## Configuración

De forma predeterminada, ejecutar el comando docker requiere privilegios de root, es decir, tiene que prefijar el comando con sudo. También puede ser ejecutado por un usuario en el grupo docker, que se crea automáticamente durante la instalación de Docker. Si intenta ejecutar el comando docker sin prefijarlo con sudo o sin estar en el grupo docker, obtendrá una salida como esta:

    docker: Cannot connect to the Docker daemon. Is the docker daemon running on this host?.
    See 'docker run --help'.

Si se desea evitar escribir sudo cada vez que ejecute el comando docker, se puede añadir el nombre de usuario actual al grupo docker:

    sudo usermod -aG docker $(whoami)

## Uso del comando docker

Con Docker instalado y funcionando, ahora es el momento de familiarizarse con la utilidad de la línea de comandos. El uso de docker consiste en pasarle una cadena de opciones y comandos seguidos de argumentos. La sintaxis toma esta forma:

    docker [option] [command] [arguments]

Se puede ver toda la lista de comandos disponibles de docker utilizando la orden:

    docker

Para ver información sobre Docker en todo el sistema, se utiliza la orden:

    docker info

---

# Órdenes utilizadas

En esta sección voy a realizar una recopilación de todas las órdenes que he utilizado con docker, a modo de glosario. Estas son:

- Listar imágenes: `docker images`

- Listar contenedores ejecutándose: `docker ps`

- Listar todos los contenedores: `docker ps -a`

- Iniciar contenedor: `docker start <container-id>`

- Detener contenedor: `docker stop <container-id>`

- Eliminar contenedor: `docker rm <container-id>`

- Eliminar imagen: `docker rmi <image-id>`

- Entrar en modo interactivo: `docker run -it <imagen-id>`

Se puede consultar el catálogo oficial de docker en este [enlace](https://docs.docker.com/engine/reference/commandline/docker/)

---

# Dockerfile

Un fichero Dockerfile es simplemente un fichero de texto que nos permite definir las instrucciones a seguir por Docker para construir una imagen, en otras palabras es como una receta para crear nuestras imágenes, que servirán de forma posterior para correr nuestros contenedores.

Para este hito, se realizará dos **[dockerfiles]()** con los que definiremos la imagen donde se desplegará las aplicaciones, y un **[script]()** con el que se automatizará el proceso de creación de la imagen y ejecución del contenedor.

A continuación se va a proceder a describir los parámetros utilizados en el [dockerfile]()

    FROM frolvlad/alpine-python3

Mediante esta línea se procede a seleccionar la imagen base que se va a utilizar. [URL de la imagen](https://hub.docker.com/r/frolvlad/alpine-python3).

En primer lugar, la imagen de base que utiliza es **[Alpine](https://alpinelinux.org/)**. Se ha elegido utilizar esta distribución de linux ya que es una imagen super ligera, segura y eficiente a la hora de utilizar los recursos. Una de las principales características que tiene es que la imagen base de Alpine utilizada en docker **solo ocupa 5MB!**.

Sobre esta imagen se ha construido una capa en la que se ha instalado python3, en concreto la versión 3.6.6 y pip3 como sistema de gestor de paquetes. Esto es justamente lo que necesita los microservicios desarrollados, por lo que esta imagen me venía como anillo al dedo.

La imagen que cumple estos requisitos ha sido encontrada en el repositorio de imágenes de docker: [dockerhub](https://hub.docker.com/). En dicho repositorio había varias imágenes que cumplían con los requerimientos de los microservicios, y es por ello que se han instalado y testeado.

Como aspecto interesante a destacar, existe una gran diferencia en el tamaño de la imagen. Por ejemplo, la imagen `digitalgenius/alphine-python3-pg` tiene un tamaño de 397MB

![img](3)

y la imagen escogida `frolvlad/alpine-python3` ocupa 90.4MB.

![img](4)

La principal diferencia radica en que la imagen escogida es mucho más ligera porque solo tiene de base instalado los paquetes esenciales de python3 que se van a utilizar en el proyecto. En la siguiente imagen se puede observar las versiones de python y pip:

![img](5)

    WORKDIR /home/jmv74211

Especifica el espacio de trabajo donde va a actuar docker.

    COPY src/app/user_service /home/jmv74211
    COPY requirements_user-service.txt /home/jmv74211

Copia el microservicio y requerimentos al contenedor

    RUN pip3 install -r requirements_user-service.txt

Instala las dependencias del microservicio de usuarios.

    EXPOSE 80/tcp

Especifica a docker el puerto que va escuchar el contenedor.

    ARG mongoVar
    ARG passVar

    ENV MONGODB_USERS_KEY=$mongoVar
    ENV ENCODING_PHRASE=$passVar

Mediante *ARG* definimos dos variables que se van a utilizar como argumentos introducidos a la hora de ejecutar el contenedor, y dichos argumentos se utilizarán para definir las variables de entorno en el contenedor.

Mediante *ENV* se definen las variables de entorno del contenedor.

    CMD python3 /home/jmv74211/user_service.py

Con CMD lanzamos la acción para ejecutar el microservicio.

En primer lugar, se va a realizar el [dockerfile]() con el que se va a crear la imagen para el microservicio de usuarios.

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

En segundo lugar se ha realizado el [dockerfile]() con el que se va a crear la imagen del microservicio de tareas. Prácticamente es igual que el anterior porque ambos utilizan python y casi las mismas bibliotecas.

    # URL imagen de base dockerhub: https://hub.docker.com/r/frolvlad/alpine-python3

    # Especifica la imagen de base que se va a utilizar
    FROM frolvlad/alpine-python3

    # Especifica el espacio de trabajo sobre el que va a actuar docker
    WORKDIR /home/jmv74211

    # Añade microservicio de usuarios y archivo de instalación de dependencias
    COPY src/app/task_service /home/jmv74211
    COPY requirements_task-service.txt /home/jmv74211

    # Instala las dependencias del microservicio
    RUN pip3 install -r requirements_task-service.txt

    # Especifica a docker el puerto que va escuchar el contenedor.
    EXPOSE 80/tcp

    # Declara argumentos que se pasan al ejecutar el contenedor
    ARG passVar

    # Declara variables de entorno
    ENV ENCODING_PHRASE=$passVar

    # Ejecuta el microservicio en el puerto 80
    CMD gunicorn -b :80 task_service:app

---

# Creación de las imágenes y ejecución de los contenedores.

Una vez que se han definido los dockerfiles, toca crear las imágenes a partir de la definición que se ha realizado en éstos.

Para ello he ejecutado las siguientes órdenes:

    docker build -t jmv74211/user_service --build-arg mongoVar=${MONGODB_USERS_KEY} --build-arg passVar=${ENCODING_PHRASE} -f contenedores/user_service/Dockerfile .

    docker build -t jmv74211/task_service --build-arg passVar=${ENCODING_PHRASE} -f contenedores/task_service/Dockerfile .

Con el parámetro -t especificamos la imagen que va a tomar el contenedor.
Con --build-arg vamos especificar un argumento, que en este caso son dos, los correspondientes a las variables de entorno que queremos pasar al contenedor. Para ello se utiliza los valores de las variables de entorno locales, por lo que dichos valores quedan protegidos en todo momento.

Comprobamos que efectivamente se han creado dichas imágenes, y vemos el tamaño que ocupan:

![img](6)

Una vez que se han creado las imágenes, vamos a ejecutar los contenedores.

    docker run -d -p 80:80 --name user_service jmv74211/user_service

    docker run -d -p 5000:80 --name task_service jmv74211/task_service

Como se puede observar en los comandos anteriores, se ha ejecutado el microservicio de usuarios en el puerto 80 del contenedor, accesible a través del puerto 80 de la máquina localhost, y el microservicio de tarea en el puerto 80 del contenedor, accesible a través del puerto 5000 de la máquina localhost.

---

# Script de automatización

Para crear las imágenes y ejecutar los contenedores de forma rápida y sencilla se ha elaborado un simple **[script]()** que automatiza el proceso.

El script es el siguiente:


    ############# LOCATION VARS #############

    USER_SERVICE_PORT="80:80" # 80 en máquina, 80 en contenedor
    TASK_SERVICE_PORT="5000:80" #100 en máquina, 80 en contenedor
    ENVIRONMENT_VARS_LIST="./env.list"
    TASK_SERVICE_IMAGE="jmv74211/task_service"
    USER_SERVICE_IMAGE="jmv74211/user_service"

    PATH_USER_SERVICE_DOCKERFILE="contenedores/user_service/Dockerfile"
    PATH_TASK_SERVICE_DOCKERFILE="contenedores/task_service/Dockerfile"

    ########################################

    echo "======================================================== \n"
    echo "Creando la imagen del user_service \n"
    echo "======================================================== \n"

    docker build -t $USER_SERVICE_IMAGE  --build-arg mongoVar=${MONGODB_USERS_KEY} --build-arg passVar=${ENCODING_PHRASE} -f $PATH_USER_SERVICE_DOCKERFILE .

    echo "======================================================== \n"
    echo "Creando la imagen del task_service \n"
    echo "======================================================== \n"

    docker build -t $TASK_SERVICE_IMAGE --build-arg passVar=${ENCODING_PHRASE} -f $PATH_TASK_SERVICE_DOCKERFILE .

    echo "======================================================== \n"
    echo "Ejecuta el contenedor de user_service \n"
    echo "======================================================== \n"

    docker run -d -p $USER_SERVICE_PORT --name user_service $USER_SERVICE_IMAGE

    echo "======================================================== \n"
    echo "Ejecuta el contenedor de task_service \n"
    echo "======================================================== \n"

    docker run -d -p $TASK_SERVICE_PORT --name task_service $TASK_SERVICE_IMAGE

---

# Despliegue de los contenedores en local

En primer lugar, hay que ejecutar el **[script]()** llamado *despliegue.sh* ubicado en el raíz del repositorio.

Una vez que se ha lanzado el script, podemos comprobar haciendo uso de la orden `docker ps` que efectivamente se están ejecutando los dos contenedores:

![img](7)

A continuación, podemos comprobar como efectivamente se han desplegado los dos microservicios:

![img](8)

---


# Documentación del hito 2:

### Creación de un microservicio y despliegue en PaaS

---

### Descripción de la arquitectura

En este hito se ha desarrollado el microservicio llamado **login-register**.

Este microservicio se encarga de recibir peticiones usando una **[API REST](https://www.mulesoft.com/resources/api/restful-api)**, procesar dicha petición y devolver una respuesta en un mensaje HTTP con un tipo de contenido en JSON.

Dicho microservicio está conectado a una base de datos noSQL llamada MongoDB. La siguiente figura ilustra con mayor claridad el flujo de información:  

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/diagrama_estado_hito2.jpg)

---

### Descripción del microservicio

La funcionalidad del microservicio login-register es la siguiente:

 - **Identificación de usuarios:** Permite identificar a un usuario por medio de username y password.

 - **Creación de usuarios:** Permite registrar nuevos usuarios.

 - **Listado de usuarios:** Permite realizar un listado de usuarios.

---

### Guía de uso del microservicio

 El microservicio web recibe peticiones GET para poder listar, crear e identificar usuarios. Dichas peticiones GET se deben de realizar usando las siguientes rutas y parámetros:

  - `/usuarios` :Devuelve la información de los usuarios registrados en el sistema de forma JSON. La salida con los usuarios registrados por defecto es la siguiente:

         {
            "result": [
               {
                "email": "jmv74211@gmail.com",
                "password": "pwdcc",
                "usuario": "jmv74211"
               },
               {
                "email": "nerea.perez.cobos@hotmail.com",
                "password": "pwdnerea",
                "usuario": "npc93"
               },
               {
                "email": "fagomez@gmail.com",
                "password": "pwdfagomez",
                "usuario": "fagomez"
               }
            ]
         }


  - `/identify/<username>/<password>:` Devuelve la información asociada del proceso de identificar al usuario con los parámetros recibidos:

   - **Caso de éxito**.

            {
               "Details": "LOGGED"
            }

   - **"Password incorrecto"** en caso de haber escrito mal la contraseña.

            {
               "Details": "Password incorrecto"
            }

   - **"El usuario no existe"** en caso de haber introducido un nombre de usuario no registrado.

            {
               "Details": "El usuario no existe"
            }


- `/register/<username>/<password>/<email>` : Devuelve información sobre la creación del usuario en el sistema:

            {
               "Details": "El usuario ha sido creado correctamente"
            }

   No podemos crear dos usuarios con el mismo username o nos devolverá el siguiente mensaje:

            {
               "Details": "Error al crear usuario: El usuario ya existe"
            }

---

### Pruebas del software

Para testear el correcto funcionamiento del microservicio de **login-register**, se han desarrollado
los siguientes test:
 - **Test unitarios**: Se prueban todas las funciones desarrolladas en el microservicio de login-register de forma independiente.Click **[aquí](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/src/test/test_funciones_login_registro.py)** para acceder al archivo relacionado.

 - **Test de integración**: Se realizan pruebas sobre las respuestas que genera el microservicio ante las posibles peticiones que puede recibir. También se comprueba las cabeceras del archivo generado por el microservicio comprobando que:
  - El tipo de contenido sea ``'aplication/json'``
  - El código de estado de una petición a una ruta válida sea `200`.
  - El código de estado de una petición cuando una ruta *no* es válida es `404`.

 Click **[aquí](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/src/test/test_servicio_login_registro.py)** para acceder al archivo relacionado

---

### Tecnologías utilizadas
Para el desarrollo de este microservicio, se han empleado las siguientes tecnologías:
- [![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/) Lenguaje de programación principal.

- [![Microframework](https://img.shields.io/badge/Microframework-Flask-brown.svg)](http://flask.pocoo.org/) Microframework web.

-  [![Database](https://img.shields.io/badge/Database-MongoDB-green.svg)](https://www.mongodb.com/es) Sistema de almacenamiento persistente.

- [![Library](https://img.shields.io/badge/Library-MongoAlchemy-yellow.svg)](https://pythonhosted.org/Flask-MongoAlchemy/) Proxy de conexión de python con la BD.

-  [![Library](https://img.shields.io/badge/Library-Requests-yellow.svg)](http://docs.python-requests.org/en/master/) Facilita el uso de peticiones HTTP 1.1.

-  [![Framework](https://img.shields.io/badge/Framework-Unittest-purple.svg)](https://docs.python.org/3/library/unittest.html) Módulo empleado para realizar las pruebas del software.

---

### Servicio de integración continua

Como servicio de integración se ha utilizado Travis CI. Travis CI es un servicio de integración continua alojado y distribuido utilizado para crear y probar proyectos de software alojados en GitHub.

Es muy sencillo de utilizar. Basta con sincronizarlo con la cuenta de github, activar el repositorio en el panel de control y crear un archivo de configuración .travis.yml en el raíz del repositorio.

El archivo de configuración que he usado para este proyecto se puede ver a través de este **[enlace](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/.travis.yml)**

A continuación se muestra una imagen donde se comprueba que se han ejecutado los test correctamente tras hacer el push al repositorio:

![testTravis](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/test_travis_hito2.jpg)

![ejemploTravis](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/ejemplo_test_travis.jpg)

Si la comprobación de test e integración es correcta, se procederá a desplegarlo en heroku.

---

### Despliegue en un PaaS

#### Elección del PaaS

Como PaaS se ha escogido la plataforma de aplicaciones cloud llamada **[HEROKU](https://www.heroku.com/)**:

![Heroku](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/heroku.jpg)

El motivo principal de elegir esta plataforma cloud como servicio ha sido porque tiene la ventaja de que se puede desplegar de forma rápida y sencilla una aplicación de tamaño pequeño o medio. No hay que invertir tiempo en configurar servidores, firewalls, ni bases de datos.

Sin embargo, en el caso de que la aplicación tuviera decenas de millones de visitas diarias, podríamos optar por otro PaaS como [Google App](https://cloud.google.com/appengine/docs/) [Engine](https://cloud.google.com/appengine/docs/), [Openshift](https://www.openshift.com/), [AppFog](https://www.appfog.com) y [DotCloud](https://www.dotcloud.com).

Para más información acerca de este tema, se puede visitar este **[enlace](https://bbvaopen4u.com/es/actualidad/cual-es-el-mejor-servicio-en-la-nube-para-desarrolladores-amazon-web-services-heroku-y)**

####  Configuración del servicio de base de datos MongoDB.

Para utilizar el servicio de base de datos MongoDB, he añadido un add-on llamado mLab MongoDB que es gratuito para heroku.

Tras haber creado la base de datos y colección necesaria para el funcionamiento del microservicio login-register, se ha configurado la URI de conexión mediante una **variable de entorno** de heroku.

![VarEnvironment](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/heroku_variables_entorno.jpg)

#### Conexión con sistema software de control de versiones

Heroku te facilita conectar el repositorio de github a través de la interfaz web de forma sencilla y cómoda.

![herokuGithub](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/heroku_gitHub.jpg)

#### Instalación de gunicorn

Los marcos web de Django y Flask cuentan con servidores web incorporados convenientes, pero estos servidores de bloqueo **solo procesan una sola solicitud a la vez**. Si implementa con uno de estos servidores en Heroku, sus recursos dinámicos serán subutilizados y su aplicación no se responderá.

Por esta razón, se ha instalado gunicorn, ya que permite ejecutar varios procesos de python dentro de un único dyno.

Para más información, se puede consultar el siguiente **[enlace](https://devcenter.heroku.com/articles/python-gunicorn)**

#### Despliegue de la aplicación

Gracias a la sincronización con github, se puede configurar los despliegues automáticamente desde el repositorio de github, incluso se puede seleccionar una opción para que antes del despliegue, se espere a que se realice un control de integración. Se seleccionará esta opción, ya que se utilizará **[TRAVIS](https://travis-ci.org/)**.

![IMAGEN](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/heroku_automatic_deploy.jpg)

Tras esto, hay que añadir el archivo **[Procfile](https://devcenter.heroku.com/articles/procfile)** en el raíz del repositorio, que especifica los comandos que ejecutarán las apps de heroku. En nuestro caso, dicho archivo contiene lo siguiente:

      web: cd src/app/servicio_login_registro;  gunicorn servicio_login_registro:app

Se utiliza el tipo de proceso web: ya que nuestra aplicación incluye un servidor web. En primer lugar nos dirigimos a la ruta donde se encuentra el servicio web, y posteriormente iniciamos dicho servicio con gunicorn.

#### Despliegue: **(https://proyecto-smartage.herokuapp.com/)**

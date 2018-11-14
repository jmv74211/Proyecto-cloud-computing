

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/logoPrincipal.png)

---

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
![Status](https://img.shields.io/badge/Status-building-red.svg)
![Status](https://img.shields.io/badge/Status-documenting-orange.svg)

## Novedades
 - **Versión 2.0** (09/11/2018): Desarrollo del hito número 2 de la asignatura de cloud computing. **[Documentación generada]()**.

### Descripción de la aplicación

**Smartage** va a ser un servicio web que permitirá a los usuarios realizar un seguimiento de su trabajo, a la vez que puedan planificar y repartir nuevas tareas de forma equitativa en un plazo determinado. Dicho servicio constará de las siguientes funcionalidades:

- **Agenda de trabajo:** Permite añadir tareas realizadas con un esfuerzo y coste estimado. Por ejemplo (ejemplo real).

 "Un hombre encargado de gestionar los regadíos de unos campos necesita saber: qué campos ha regado, qué días y cuántas horas ha dedicado en cada uno ellos para llevar un seguimiento de su trabajo y saber cuánto tiene que cobrar a cada uno de ellos mes a mes."

 Esta funcionalidad estaría enfocada a este tipo de contexto, el usuario podrá crear una o varias secciones de trabajo e introducir registros cada vez que realice una tarea, indicando la fecha, concepto y número de horas realizadas. Finalmente, el servicio mostrará dicha información clasificada por mes y aportará distintos datos de interés.


- **Programación de tareas:** Permite añadir nuevas tareas a realizar con una fecha límite y esfuerzo estimado, y el servicio propondrá una distribución de dicha tarea de forma parcial a lo largo del calendario.

- **Calendario**: Permite visualizar la distribución de las tareas a lo largo del calendario.

- **Trabajo diario**: Muestra las tareas del usuario que se proponen a realizar en el día actual.

### Arquitectura

La arquitectura de la aplicación se basa en un arquitectura de **[microservicios](https://openwebinars.net/blog/microservicios-que-son/)**. Cada funcionalidad anteriormente descrita, se desarrollará como un microservicio independiente. Los microservicios previstos a desarrollar son los siguientes:
- Microservicio de gestión de usuarios: Registro y acceso.
- Microservicio de programación de agenda de trabajo.
- Microservicio de programación de tareas.
- Microservicio de calendario.
- Microservicio de trabajo diario.

La estructura del servicio se basará en una aplicación que hará de gestor y se encargará de llamar a los diferentes microservicios cada vez que se necesiten.


### Desarrollo
El conjunto de microservicios se van a desarrollar utilizando las siguientes teconologías:

- [![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/) Lenguaje de programación principal.

- [![Microframework](https://img.shields.io/badge/Microframework-Flask-brown.svg)](http://flask.pocoo.org/) Microframework web.

-  [![Database](https://img.shields.io/badge/Database-MongoDB-green.svg)](https://www.mongodb.com/es) Sistema de almacenamiento persistente.

- [![Library](https://img.shields.io/badge/Library-MongoAlchemy-yellow.svg)](https://pythonhosted.org/Flask-MongoAlchemy/) Proxy de conexión de python con la BD.

-  [![Library](https://img.shields.io/badge/Library-Requests-yellow.svg)](http://docs.python-requests.org/en/master/) Facilita el uso de peticiones HTTP 1.1.

-  [![Framework](https://img.shields.io/badge/Framework-Unittest-purple.svg)](https://docs.python.org/3/library/unittest.html) Módulo empleado para realizar las pruebas del software.

---

### Versión 2.0 : Desarrollo del microservicio login-register

#### Descripción del microservicio

La funcionalidad del microservicio login-register es la siguiente:

 - **Identificación de usuarios:** Permite identificar a un usuario por medio de username y password.

 - **Creación de usuarios:** Permite registrar nuevos usuarios.

 - **Listado de usuarios:** Permite realizar un listado de usuarios

#### Descripción de la arquitectura del microservicio

En este hito se ha desarrollado el microservicio llamado **login-register**.

Este microservicio se encarga de recibir peticiones usando una **[API REST](https://www.mulesoft.com/resources/api/restful-api)**, procesar dicha petición y devolver una respuesta en un mensaje HTTP con un tipo de contenido en JSON.

Dicho microservicio está conectado a una base de datos noSQL llamada MongoDB. La siguiente figura ilustra con mayor claridad el flujo de información:  

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/diagrama_estado_hito2.jpg)

#### Guía de uso del microservicio

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

#### Ejemplos de uso

[Poner ejemplos de uso cuando esté desplegado en heroku]



![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/logoPrincipal.png)

---

[![License](https://img.shields.io/aur/license/yaourt.svg?style=plastic)](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/LICENSE)
[![Status](https://img.shields.io/badge/Status-Documenting-yellow.svg)](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/README.md)
[![Language](https://img.shields.io/badge/language-Python-green.svg)](https://www.python.org/)
[![Language](https://img.shields.io/badge/Microframework-Flask-brown.svg)](http://flask.pocoo.org/)
[![Language](https://img.shields.io/badge/library-MongoAlchemy-purple.svg)](https://www.sqlalchemy.org/)

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

- Lenguaje de programación principal:  [![Language](https://img.shields.io/badge/ -Python-blue.svg)](https://www.python.org/)

- Microframework web:
[![Language](https://img.shields.io/badge/ -Flask-brown.svg)](http://flask.pocoo.org/)

- API RESTFULL de conexión con la BD:  [![Language](https://img.shields.io/badge/ -MongoAlchemy-yellow.svg)](https://pythonhosted.org/Flask-MongoAlchemy/) [![BD](https://img.shields.io/badge/ -Pymongo-yellow.svg)](http://flask.pocoo.org/)

- Sistema de almacenamiento persistente: [![Language](https://img.shields.io/badge/ -MongoDB-green.svg)](http://flask.pocoo.org/)


---
A lo largo del desarrollo de la aplicación, se irán añadiendo los cambios oportunos en esta documentación, y aclarando todo acerca de su desarrollo y despliegue en la nube.

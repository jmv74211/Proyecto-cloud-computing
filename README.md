

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/logoPrincipal.png)

---

[![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/)
![Status](https://img.shields.io/badge/Status-building-red.svg)
![Status](https://img.shields.io/badge/Status-documenting-orange.svg)


# Tabla de contenidos

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
<!-- END doctoc -->

- [Novedades](#novedades)
- [Descripción de la aplicación](#descripci%C3%B3n-de-la-aplicaci%C3%B3n)
- [Arquitectura](#arquitectura)
- [Desarrollo](#desarrollo)
- [Descripción del microservicio](#descripci%C3%B3n-del-microservicio)
- [Descripción de la arquitectura del microservicio](#descripci%C3%B3n-de-la-arquitectura-del-microservicio)
- [Guía de uso del microservicio de login-registro](#gu%C3%ADa-de-uso-del-microservicio-de-login-registro)
- [Guía de uso del microservicio de taras (NUEVO versión 3.0)](#gu%C3%ADa-de-uso-del-microservicio-de-taras-nuevo-versi%C3%B3n-30)
  - [Añadir tareas](#a%C3%B1adir-tareas)
  - [Mostrar tareas](#mostrar-tareas)
  - [Modificar tareas](#modificar-tareas)
  - [Eliminar tareas](#eliminar-tareas)
- [Despliegue de la aplicación en PaaS](#despliegue-de-la-aplicaci%C3%B3n-en-paas)
- [Despliegue de la infraestructura en máquina local](#despliegue-de-la-infraestructura-en-m%C3%A1quina-local)
  - [Instrucciones para el despliegue en localhost](#instrucciones-para-el-despliegue-en-localhost)
    - [Vagrant](#vagrant)
    - [Ansible](#ansible)
  - [Despliegue de la infraestructura](#despliegue-de-la-infraestructura)
- [Despliegue de la infraestructura y aprovisionamiento en azure](#despliegue-de-la-infraestructura-y-aprovisionamiento-en-azure)
- [Comprobaciones de aprovisionamiento del hito3](#comprobaciones-de-aprovisionamiento-del-hito3)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

# Novedades
 - **Versión 2.0** (15/11/2018): Desarrollo del hito número 2 de la asignatura de cloud computing. **[Documentación generada](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/hito2_descripci%C3%B3n.md)**.

- **Versión 3.0** (04/12/2018): Incluye desarrollo del microservicio de tareas y el desarrollo del hito número 3 de la asignatura de cloud computing. **[Documentación generada](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/hito3_descripci%C3%B3n.md)**.

La dirección IP del servidor web es la siguiente MV: 137.116.210.191
---

# Descripción de la aplicación

**Smartage** va a ser un servicio web que permitirá a los usuarios realizar un seguimiento de su trabajo, a la vez que puedan planificar y repartir nuevas tareas de forma equitativa en un plazo determinado. Dicho servicio constará de las siguientes funcionalidades:

- **Agenda de trabajo:** Permite añadir tareas realizadas con un esfuerzo y coste estimado. Por ejemplo (ejemplo real).

 "Un hombre encargado de gestionar los regadíos de unos campos necesita saber: qué campos ha regado, qué días y cuántas horas ha dedicado en cada uno ellos para llevar un seguimiento de su trabajo y saber cuánto tiene que cobrar a cada uno de ellos mes a mes."

 Esta funcionalidad estaría enfocada a este tipo de contexto, el usuario podrá crear una o varias secciones de trabajo e introducir registros cada vez que realice una tarea, indicando la fecha, concepto y número de horas realizadas. Finalmente, el servicio mostrará dicha información clasificada por mes y aportará distintos datos de interés.


- **Programación de tareas:** Permite añadir nuevas tareas a realizar con una fecha límite y esfuerzo estimado, y el servicio propondrá una distribución de dicha tarea de forma parcial a lo largo del calendario.

- **Calendario**: Permite visualizar la distribución de las tareas a lo largo del calendario.

- **Trabajo diario**: Muestra las tareas del usuario que se proponen a realizar en el día actual.

---

# Arquitectura

La arquitectura de la aplicación se basa en un arquitectura de **[microservicios](https://openwebinars.net/blog/microservicios-que-son/)**. Cada funcionalidad anteriormente descrita, se desarrollará como un microservicio independiente. Los microservicios previstos a desarrollar son los siguientes:
- Microservicio de gestión de usuarios: Registro y acceso.
- Microservicio de programación de agenda de trabajo.
- Microservicio de programación de tareas.
- Microservicio de calendario.
- Microservicio de trabajo diario.

La estructura del servicio se basará en una aplicación que hará de gestor y se encargará de llamar a los diferentes microservicios cada vez que se necesiten.

---

# Desarrollo
El conjunto de microservicios se van a desarrollar utilizando las siguientes teconologías:

- [![Language](https://img.shields.io/badge/Language-Python-blue.svg)](https://www.python.org/) Lenguaje de programación principal.

- [![Microframework](https://img.shields.io/badge/Microframework-Flask-brown.svg)](http://flask.pocoo.org/) Microframework web.

-  [![Database](https://img.shields.io/badge/Database-MongoDB-green.svg)](https://www.mongodb.com/es) Sistema de almacenamiento persistente.

- [![Library](https://img.shields.io/badge/Library-MongoAlchemy-yellow.svg)](https://pythonhosted.org/Flask-MongoAlchemy/) Proxy de conexión de python con la BD.

-  [![Library](https://img.shields.io/badge/Library-Requests-yellow.svg)](http://docs.python-requests.org/en/master/) Facilita el uso de peticiones HTTP 1.1.

-  [![Framework](https://img.shields.io/badge/Framework-Unittest-purple.svg)](https://docs.python.org/3/library/unittest.html) Módulo empleado para realizar las pruebas del software.

---

# Descripción del microservicio

La funcionalidad del microservicio login-register es la siguiente:

 - **Identificación de usuarios:** Permite identificar a un usuario por medio de username y password.

 - **Creación de usuarios:** Permite registrar nuevos usuarios.

 - **Listado de usuarios:** Permite realizar un listado de usuarios

La funcionalidad del microservicio de tareas es la siguiente:

 - **Añadir tareas:** Permite que los usuarios añadan nuevas tareas a través de una petición **PUT**.

 - **Modificar tareas:** Permite que los usuarios modifiquen tareas a través de una petición **POST**.

 - **Eliminar tareas:** Permite que los usuarios eliminen tareas a través de una petición **DELETE**.

 - **Mostrar tareas:** Permite que mostrar a los usuarios el conjunto de tareas que existen. En el siguiente hito se desarrollará este apartado más en profundidad, permitiendo enlazar a los usuarios registrados e identificados en el sistema utilizando el microservicio de login y registro, y posteriormente accediendo al microservicio de tareas donde puedan consultar y gestionar sus propias tareas.
 ---

# Descripción de la arquitectura del microservicio

En este hito se ha desarrollado el microservicio llamado **login-register**.

Este microservicio se encarga de recibir peticiones usando una **[API REST](https://www.mulesoft.com/resources/api/restful-api)**, procesar dicha petición y devolver una respuesta en un mensaje HTTP con un tipo de contenido en JSON.

Dicho microservicio está conectado a una base de datos noSQL llamada MongoDB. La siguiente figura ilustra con mayor claridad el flujo de información:  

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/diagrama_estado_hito2.jpg)

---

# Guía de uso del microservicio de login-registro

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


# Guía de uso del microservicio de taras (NUEVO versión 3.0)

Para ejecutar esta aplicación basta con lanzarla mediante la orden `python3 task_service.py` o  `gunicorn -b :3000 task_service:app` dentro del directorio /src/app/task_service.

Si accedemos al raíz de la aplicación nos mostrará el siguiente contenido:

    status	"OK"

Para realizar las distintas peticiones **PUT, POST, DELETE, GET** se va a utilizar la herramienta **[postman](https://www.getpostman.com/)**

## Añadir tareas

Para añadir una tarea vamos a realizar una petición **PUT**, añadiendo la información en formato JSON. Como se puede observar en la siguient imagen, no es necesario añadir el *task_id*, ya que el servicio lo inserta automáticamente.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/demo_1.png)

Como resultado nos devuelve que se ha insertado con id = 0 y un código de estado de 201.

## Mostrar tareas

Para mostar una tarea, vamos a utilizar la petición **GET**.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/demo_2.png)

Como se puede observar, nos muestra la tarea que añadimos en el apartado anterior con un código de estado = 200.


## Modificar tareas

En primer lugar vamos a añadir otra tarea utilizando la orden PUT descrita anteriormente. La tarea la vamos a relacionar con una supuesta práctica de IC.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/demo_3.png)

Ahora vamos a proceder a modificar dicha tarea mediante la petición **POST**. Por ejemplo vamos a modificar la estimación temporal y la fecha máxima de entrega.

**Atención**: En este caso si es necesario introducir el *task_id*, para poder identificar la tarea que deseamos modificar.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/demo_4.png)

## Eliminar tareas

Para proceder a eliminar una tarea vamos a utilizar la petición **DELETE**. Simplemente basta con emplear el identificador de la tarea que se desea eliminar, como se puede observar en la siguiente imagen:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/demo_5.png)

Como se puede observar, nos devuelve el código de estados 204, correspondiente a que no hay contenido.

Volvemos a comprobar la lista de tareas mediante la petición GET para verificar que la tarea se ha eliminado correctamente.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/demo_6.png)

---

# Despliegue de la aplicación en PaaS

La aplicación se ha desplegado en el PaaS heroku. En el siguiente **[enlace](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/hito2_descripci%C3%B3n.md)** se puede ver el por qué se ha tomado esta decisión, y cómo se ha realizado.

**Despliegue:** https://proyecto-smartage.herokuapp.com/

---

# Despliegue de la infraestructura en máquina local

## Instrucciones para el despliegue en localhost

En el caso de que se quiera realizar un despliegue de forma local, se proporciona una serie de código que define la infraestructura necesaria para su correcto despliegue en cuestión de segundos o pocos minutos.

### Vagrant

En primer lugar, se ha utilizado **[Vagrant](http://www.conasa.es/blog/vagrant-la-herramienta-para-crear-entornos-de-desarrollo-reproducibles/)** para generar entornos de desarrollo reproducibles y compartibles de forma muy sencilla.

La versión de vagrant que se ha usado en este proyecto es: `Vagrant 2.0.2`

En este caso se ha utilizado para crear una máquina virtual en **[virtualbox](https://www.virtualbox.org/)**, y configurado para que se ejecute un script de aprovisionamiento que instale el software necesario para que se ejecute nuestra aplicación.

El archivo donde se describe esta infraestructura se llama **[Vagrantfile](https://www.vagrantup.com/docs/vagrantfile/)** y el utilizado en este proceso de despliegue es el **[siguiente](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/vagrant/Vagrantfile)**.

### Ansible

Como software para automatizar el proceso de aprovisionamiento se ha utilizado **[Ansible](https://openwebinars.net/blog/que-es-ansible/)**.

La versión de ansible que se ha utilizado en este proyecto es: `ansible 2.7.2`

Los archivos necesarios para ejecutar correctamente ansible son los siguientes:

- **[ansible.cfg](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/provision/azure/ansible.cfg)**: Archivo para configurar ansible.

- **[ansible_hosts](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/provision/azure/ansible_hosts)**: Archivo para definir el conjunto de host.

- **[playbook_principal.yml](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/provision/azure/playbook_principal.yml)**: Archivo donde se define el conjunto de instrucciones que se van a ejecutar en los hosts. En este caso se han utilizado **[roles](https://docs.ansible.com/ansible/2.7/user_guide/playbooks_reuse_roles.html)** para instalar una configuración base y la versión 3.6 de python.

Se puede consultar el contenido de dichos archivos haciendo click en el nombre del archivo de la lista anterior.


## Despliegue de la infraestructura

Una vez descargado el repositorio e instalado vagrant y ansible, montar la infraestructura necesaria para ejecutar el proyecto es muy sencillo.

Basta con situarse en el directorio de vagrant dentro del directorio del proyecto y ejecutar `vagrant up`.

Automáticamente se creará la máquina virtual (en este caso utilizando VirtualBox) y se ejecutará el playbook principal que contiene el conjunto de instrucciones para instalar el software necesario para el despliegue.

En el caso de no utilizar vagrant, también podemos realizar el aprovisionamiento utilizando órdenes de ansible. En este caso podemos ejecutar el aprovisionamiento situándose dentro del directorio provision y ejecutando la orden `ansible-playbook playbook_principal.yml`

---

# Despliegue de la infraestructura y aprovisionamiento en azure

Se ha creado una máquina virtual en **[Azure](https://azure.microsoft.com/es-es/)** con ubuntu 16.04 LTS.

Para poder ejecutar el aprovisionamiento, se ha creado un playbook específico que se puede ejecutar con la orden `ansible-playbook playbook_principal.yml` y que instala todo el software y dependencias necesarias para lanzar la aplicación.

Tras ejecutar dicho playbook con ansible, lanzamos la aplicación y probamos que funciona correctamente haciendo peticiones a la siguiente dirección:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/azure_app_test.png)

Se puede consultar la **[documentación correspondiente al hito número 3](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/hito3_descripci%C3%B3n.md)** que describe con más detalle el apartado del despliegue de la infraestructura virtual y del aprovisionamiento.

---

# Comprobaciones de aprovisionamiento del hito3

- Comprobación de [@jmv74211](https://github.com/jmv74211) al aprovisionamiento de [@gecofer](https://github.com/Gecofer) disponible en este [enlace](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/correcci%C3%B3n_a_%40Gecofer.md).

- Comprobación de [@gecofer](https://github.com/jmv74211) al aprovisionamiento de [@jmv74211](https://github.com/Gecofer) disponible en este [enlace](https://github.com/Gecofer/proyecto-CC/blob/master/docs/corrección_a_%40jmv74211.md).

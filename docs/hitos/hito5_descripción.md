
# Documentación del hito 5: Orquestación de máquinas virtuales

# Introducción

El objetivo de este hito trata de usar Vagrant para provisionar una o preferiblemente varias máquinas virtuales usando un proveedor de servicios cloud.

---

# Tecnología empleada

## [Vagrant](https://www.vagrantup.com/)

Vagrant es una herramienta gratuita de línea de comandos, disponible para Windows, MacOS X y GNU/Linux, que permite generar entornos de desarrollo reproducibles y compartibles de forma muy sencilla. Para ello, Vagrant crea y configura máquinas virtuales a partir de simples ficheros de configuración.

Basta con compartir el fichero de configuración de Vagrant (llamado *Vagrantfile*) con otro desarrollador para que, con un simple comando, pueda reproducir el mismo entorno de desarrollo.

En este **[enlace](https://www.conasa.es/blog/vagrant-la-herramienta-para-crear-entornos-de-desarrollo-reproducibles/)** hay un artículo que explica claramente qué es vagrant y los primeros pasos para trabajar con esta herramienta.

## [Ansible](https://www.ansible.com/)

En este caso, se ha vuelto a elegir ansible como software para aprovisionar nuestra máquina virtual. Basta con añadir unas cuantas líneas a nuestro *Vagrantfile* para que automáticamente se ejecute el proceso de aprovisionamiento de las máquinas virtuales que hemos creado con vagrant.

Para saber más información acerca de los archivos generados para ansible, se puede consultar la [documentación del hito 3](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/hito3_descripci%C3%B3n.md) donde se explica cada línea configurada.

---

# Primeros pasos con Vagrant

El primer paso, como es habitual, es descargar e instalar Vagrant y además instalar el proveedor de máquinas virtuales que queramos utilizar, que por defecto será VirtualBox, ya que es gratuito y viene integrado en Vagrant. Una vez instalados, podremos ejecutar el comando ‘vagrant’ para obtener un listado de las opciones disponibles.

Vagrant dispone de una serie de plantillas que nos proporcionarán imágenes preparadas para utilizar, estás plantillas son llamadas **boxes**. Existen muchos repositorios de vagrant en los cuales nos podemos descargar estas plantillas. Algunos son:

- [https://www.vagrantbox.es/](https://www.vagrantbox.es/)
- [https://cloud-images.ubuntu.com/](https://cloud-images.ubuntu.com/)
- [https://vagrantcloud.com/](https://vagrantcloud.com/)

Podemos añadir un box de la siguiente forma:

    vagrant box add {title} {url}

Tras esto, crear una máquina virtual con Vagrant es tan sencillo como ejecutar los siguientes comandos:

    vagrant init {title}
    vagrant up


El primer comando, `vagrant init`, genera el fichero de configuración “**Vagrantfile**”. Éste es un fichero de configuración en el que se especifica qué parámetros vamos a utilizar para crear nuestras máquinas virtuales. A lo largo de este documento del hito 5 se verá más en profundidad el contenido de éste.

Por defecto, Vagrant inicia la máquina virtual sin interfaz gráfica. Sin embargo, podemos acceder a ella mediante SSH con el comando:

    vagrant ssh

Una vez que hayamos terminado de trabajar con la máquina podemos ejecutar los siguientes comandos:


- `vagrant suspend`: Pausa la máquina virtual, guardando el estado actual en el disco duro. Permite arrancar de nuevo la máquina muy rápidamente con `vagrant up` con el estado exacto en el que se quedó.

- `vagrant halt`: Realiza un apagado controlado de la máquina virtual (igual a apagar una máquina física). Como en el caso anterior, podemos volver a arrancar la máquina virtual con `vagrant up`, aunque en este caso el arranque es más lento que al hacer un “suspend” (ya que tiene que volver a iniciar el sistema operativo).

- `vagrant destroy`: Destruye la máquina virtual y todo su contenido.

---

# Vagrantfile

Tal y como se ha comentado en el apartado anterior, el en el fichero *Vagrantfile* se va a especificar la configuración necesaria para crear nuestras máquinas.

En este proyecto, voy a crear dos máquinas virtuales. La primera máquina va a contener el microservicio de login y registro de usuarios, y la segunda máquina va a contener el microservicio de tareas, de forma que la segunda máquina utilice el microservicio de la primera para funcionar correctamente.

![img](Imagen arquitectura p5)

---

# Desarrollo del servicio smartage (versión 5.0)

## Descripción de cambios.

Hasta ahora se había desarrollado un microservicio de tareas y otro referente a los usuarios e identificación.

En esta nueva versión se ha comunicado dichos microservicios entre sí, de forma que el microservicio de tareas va a utilizar el microservicio de login y usuarios para poder funcionar correctamente.

En la siguiente figura se muestra la arquitectura de la aplicación hasta la versión 4.

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/estructura_hito4.png)

En esta nueva versión, la arquitectura es la siguiente:

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/diagrama_arquitectura.png)

El objetivo de esto es que los microservicios no sean independientes entre sí, sino que la aplicación vaya utilizando dichos microservicios para componer el conjunto de funcionalidades que posee.

En esta nueva versión, el usuario tiene que identificarse o registrarse para poder acceder al microservicio de tareas.

El microservicio de tareas, delega dicha funcionalidad al microservicio de usuarios, derivando dichas peticiones y gestionándolas internamente.

El acceso a la aplicación se realizará mediante un token de acceso que se proporciona tras haber realizado el proceso de login satisfactoriamente. Dicho token de acceso será necesario enviarlo en la cabecera de cada petición que se realice al microservicio de tareas (menos en la creación e identificación de usuarios, como es obvio).

También se han añadido los correspondientes [test](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/src/test/test_task_service.py) al [microservicio de tareas](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/src/app/task_service/task_service.py), comprobando que efectivamente, todas las funcionalidades del microservicio funcionan correctamente.

## Guía de uso del microservicio de tareas (Versión 5.0).

En primer lugar, para poder acceder a las funcionalidades, es necesario registrarse o identificarse.

### Creación de un usuario

        [PUT] --> {
            'username':'nombreUsuario', 'password':'contraseña', 'email':'direccionEmail'
          } --> http://DirecciónIP/user

Si el usuario se ha creado correctamente nos devolverá el siguiente json:

        [RESPONSE] --> {
            message' : 'New user created!
        }


### Identificación de un usuario

Para poder identificarnos en la aplicación, será necesario introducir nuestro usuario y contraseña en el login.

Tras dicha identificación, se devolverá un mensaje de bienvenida al usuario y el token de sesión que se necesita enviar en la cabecera de cada petición para acceder a las diferentes funcionalidades.

        [POST] --> {
            'usuario':'nombreUsuario',
            'password':'contraseña'
        } --> http://DirecciónIP/login

En el caso de realizar un login correcto se nos devolverá un mensaje como el siguiente:

        [RESPONSE] -->   {
            message' : 'Bienvenid@ usuario',
            token : 'tokenHash'
        }

En el caso de introducir erróneamente los datos, se distinguen los siguientes casos:

- Enviar una petición POST con el contenido de los datos de forma incorrecta (falta algún campo, las claves no se llaman username, pasword...). En tal caso se nos mostrará un mensaje de error como el siguiente:

      Could not verify, invalid arguments!

- Introducir un usuario inexistente. En tal caso se nos mostrará un mensaje de error como el siguiente:

        User does not exist!

- Introducir una contraseña errónea. En tal caso se nos mostrará el siguiente mensaje:

      Password incorrect!

### Obtener los datos del usuarios

Para listar la información de un usuario, basta con realizar la siguiente petición GET:

    [GET] --> {
                headers={ 'content-type': 'application/json',
                          'access-token': 'tokenHash'
                        }
              } --> http://DirecciónIP/user/<username>

En el caso de ser usuario administrador o buscar su propio perfil, la información que nos devuelve es la siguiente:

    [RESPONSE] --> {
                      users' :
                             {
                                "admin": "False",
                                "email": "email@correo.ugr.es",
                                "password": "sha256$8gyJWifM$78e76359473b9fefdbc888ec47eaa98571458b368ff74c19a7be68d7e6160c45",
                                "public_id": "b0c8b763-0bad-41bc-ad16-032cb8e3f10f",
                                "username": "usuarioPrueba"
                              }
                    }

Si se intenta mirar el perfil de otro usuario sin ser administrador nos mostrará el siguiente mensaje:

    [RESPONSE] --> {
                      'message' : 'You cannot perform that action!'
                   }

O si el usuario buscado no existe:


    [RESPONSE] --> {
                      'message' : 'User not found!'
                   }

### Eliminar a un usuario

Esta funcionalidad nos permite eliminar permanentemente un usuario del sistema. Para eliminar a un usuario basta con realizar la siguiente petición **DELETE**:

    [DELETE] --> {
        headers={ 'content-type': 'application/json',
                  'access-token': 'tokenHash'
        }
    } --> http://DirecciónIP/user/<username>

Tras eliminar al usuario, se nos devolverá un mensaje con código de error 204.

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

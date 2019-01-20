
# Documentación del hito 5: Orquestación de máquinas virtuales

---

# Tabla de contenidos

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
<!-- END doctoc -->

- [Tecnología empleada](#tecnolog%C3%ADa-empleada)
  - [Vagrant](#vagrant)
  - [Ansible](#ansible)
- [Primeros pasos con Vagrant](#primeros-pasos-con-vagrant)
- [Orquestación de máquinas virtuales y Vagrantfile](#orquestaci%C3%B3n-de-m%C3%A1quinas-virtuales-y-vagrantfile)
- [Ansible Vault](#ansible-vault)
- [Desarrollo del servicio smartage (versión 5.0)](#desarrollo-del-servicio-smartage-versi%C3%B3n-50)
  - [Descripción de cambios.](#descripci%C3%B3n-de-cambios)
  - [Guía de uso del microservicio de tareas (Versión 5.0).](#gu%C3%ADa-de-uso-del-microservicio-de-tareas-versi%C3%B3n-50)
    - [Creación de un usuario](#creaci%C3%B3n-de-un-usuario)
    - [Identificación de un usuario](#identificaci%C3%B3n-de-un-usuario)
    - [Obtener los datos del usuarios](#obtener-los-datos-del-usuarios)
    - [Eliminar a un usuario](#eliminar-a-un-usuario)
  - [Añadir tareas](#a%C3%B1adir-tareas)
  - [Mostrar tareas](#mostrar-tareas)
  - [Modificar tareas](#modificar-tareas)
  - [Eliminar tareas](#eliminar-tareas)
  - [Comprobaciones del hito 5](#comprobaciones-del-hito-5)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

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

# Orquestación de máquinas virtuales y Vagrantfile

Utilizando vagrant se va a proceder a orquestar dos máquinas virtuales en las que se instalarán los microservicios de usuarios y tareas.

Tal y como se ha comentado en el apartado anterior, el en el fichero *Vagrantfile* se va a especificar la configuración necesaria para crear nuestras máquinas.

En este proyecto, voy a crear dos máquinas virtuales. La primera máquina va a contener el microservicio de login y registro de usuarios, y la segunda máquina va a contener el microservicio de tareas, de forma que la segunda máquina utilice el microservicio de la primera para funcionar correctamente.

Para iniciar con el proceso de orquestación, dado que voy a utilizar el proveedor de azure, he consultado la [documentación de vagrant-azure](https://github.com/Azure/vagrant-azure), y he instalado el plugin de vagrant-azure para poder utilizar `vagrant ssh` con:

    vagrant plugin install vagrant-azure

A continuación se procede a describir los parámetros utilizados en el **[Vagrantfile](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/orquestacion/Vagrantfile)**.

En primer lugar se han definido una serie de variables locales, que serán los parámetros de configuración que vamos a utilizar para orquestar dichas máquinas. Estos parámetros son los siguientes:

    ############# LOCATION VARS #############

    VAGRANTFILE_API_VERSION = "2"
    SSH_PRIVATE_KEY_PATH = '~/.ssh/id_rsa'
    VM_BOX_URL = "https://github.com/azure/vagrant-azure/raw/v2.0/dummy.box"


    ## ------------ AZURE ACTIVE DIRECTORY ------------------
    AZURE_SUBSCRIPTION_ID = ENV['AZURE_SUBSCRIPTION_ID']
    AZURE_TENTANT_ID = ENV['AZURE_TENANT_ID']
    AZURE_CLIENT_ID = ENV['AZURE_CLIENT_ID']
    AZURE_CLIENT_SECRET = ENV['AZURE_CLIENT_SECRET']

    ## ------------ USER SERVICE MACHINE ------------------
    VM_BOX_NAME_M1 = "user-service"
    VM_SSH_USERNAME_M1 = "vagrant"
    AZURE_VM_LOCATION_M1 = "francecentral"
    AZURE_VM_RESOURCE_GROUP_NAME_M1 = "cc-resource-group-francecentral"
    AZURE_VM_IMAGE_URN_M1 ="Canonical:UbuntuServer:18.04-LTS:18.04.201812060"
    AZURE_VM_SIZE_M1 = "Standard_B1s" # https://docs.microsoft.com/en-us/azure/virtual-machines/linux/sizes-general
    AZURE_VM_ADMIN_USERNAME_M1 = "jmv74211"
    AZURE_VM_ADMIN_PASSWORD_M1 = "Pwdcc2019"
    PLAYBOOK_URL_M1 = "../provision/azure/user_service/playbook_principal.yml"
    DNS_M1 = "user-service"

    ## ------------ TASK SERVICE MACHINE ------------------
    VM_BOX_NAME_M2 = "task-service"
    VM_SSH_USERNAME_M2 = "vagrant"
    AZURE_VM_LOCATION_M2 = "westeurope"
    AZURE_VM_RESOURCE_GROUP_NAME_M2 = "myResourceGroup"
    AZURE_VM_IMAGE_URN_M2 ="Canonical:UbuntuServer:18.04-LTS:18.04.201812060"
    AZURE_VM_SIZE_M2 = "Standard_B1s" # https://docs.microsoft.com/en-us/azure/virtual-machines/linux/sizes-general
    AZURE_VM_ADMIN_USERNAME_M2 = "jmv74211"
    AZURE_VM_ADMIN_PASSWORD_M2 = "Pwdcc2019"
    PLAYBOOK_URL_M2 = "../provision/azure/task_service/playbook_principal.yml"
    DNS_M2 = "task-service"
    #############################################

Ahora comenzamos el proceso de orquestación con vagrant, utilizando su versión de API 2, que es la más actual.

    Vagrant.configure(VAGRANTFILE_API_VERSION) do |config|

Ahora establecemos una serie de parámetros globales para todas las máquinas, como la ruta de nuestra clave privada y el dummy box de azure con su URL.

*Nota:* Se ha probado a no poner ese dummy box y vagrant falla, porque primeramente necesita un box para poder funcionar. Como en este caso no se va a trabajar con virtualbox o VMware, es necesario crear dicho dummy al que posteriormente le asignaremos una imagen de azure [referencia](https://blog.scottlowe.org/2017/12/11/using-vagrant-with-azure/).

    config.ssh.private_key_path = SSH_PRIVATE_KEY_PATH
    config.vm.box = 'azure'
    config.vm.box_url = 'https://github.com/msopentech/vagrant-azure/raw/master/dummy.box'

Ahora vamos a comenzar a definir nuestra primera máquina virtual:

    config.vm.define "user-service" do |m1|

Establecemos que el proveedor va a ser AZURE:

    m1.vm.provider :azure do |azure, override|

A continuación vamos a establecer los parámetros de conexión con nuestros datos de azure. Para ello se ha creado un "Azure Active Directory (AAD) Application", y con la orden `az ad sp create-for-rbac` nos ha mostrado la siguiente información:

    {
      "appId": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX",
      "displayName": "some-display-name",
      "name": "http://azure-cli-2017-04-03-15-30-52",
      "password": "XXXXXXXXXXXXXXXXXXXX",
      "tenant": "XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX"
    }

Estos valores se han almacenado en variables de entorno y se han proporcionado al Vagrantfile de la siguiente forma:

    # Mandatory settings
    azure.tenant_id = AZURE_TENTANT_ID
    azure.client_id = AZURE_CLIENT_ID
    azure.client_secret = AZURE_CLIENT_SECRET
    azure.subscription_id = AZURE_SUBSCRIPTION_ID

A continuación se ha establecido el parámetro de la URN de la imagen que vamos a utilizar (en este caso UbuntuServer 18.04), y el nombre de la máquina:

    azure.vm_image_urn = AZURE_VM_IMAGE_URN_M1
    azure.vm_name = VM_BOX_NAME_M1

Finalmente, se han proporcionado una serie de parámetros opcionales de configuración que son los siguientes:

    # Optional settings
    azure.location = AZURE_VM_LOCATION_M1
    azure.resource_group_name = AZURE_VM_RESOURCE_GROUP_NAME_M1
    azure.vm_size = AZURE_VM_SIZE_M1
    azure.tcp_endpoints = 80
    azure.dns_name = DNS_M1

Con estos parámetros establecemos la localización de la máquina virtual, el nombre del grupo de recurso (IMPORTANTE: dicho nombre de grupo de recurso debe de ser distinto a la otra máquina, porque si no vagrant da error), el tamaño de la máquina (en este caso es un tamaño básico y estándard debido a que los microservicios no requieren de mucha CPU ni memoria), y mediante `azure.tcp_endpoints` abrimos el puerto 80 para poder recibir y enviar tráfico HTTP y finalmente con `azure.dns_name` voy a establecer un DNS a mi máquina para que los microservicios puedan conectarse entre sí y funcionar conjuntamente.

Tras terminar dicha configuración de la primera máquina, a continuación se va a proceder a aprovisionarla con ansible:

    config.vm.provision "ansible" do |provision|
      provision.ask_vault_pass=true
      provision.playbook = PLAYBOOK_URL_M1
    end

Como se puede observar, configuramos dos parámetros:

- El primer parámetro es `provision.ask_vault_pass=true` con el que le decimos a vagrant que se va a utilizar ansible-vault y que nos pregunte la contraseña para descrifrar el contenido antes de que realice el aprovisionamiento.

- El segundo parámetro es la URL de nuestro playbook, que contiene el conjunto de instrucciones y roles para aprovisionar dicha máquina

Todo este proceso que se ha realizado para definir la primera máquina virtual, se ha realizado con una segunda máquina, modificando los parámetros (ver en variables locales) y el playbook de aprovisionamiento (En este caso cada máquina virtual utiliza un playbook propio).

Se puede consultar dicho Vagrantfile en este **[enlace](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/orquestacion/Vagrantfile)**.

---

# Ansible Vault

En este nuevo hito, se ha procedido a enviar la información de carácter sensible (como por ejemplo la API-Key para acceder a la base de datos, o variables de entorno locales de cifrado...) a las máquinas virtuales mediante un cifrado con [ansible-vault](https://docs.ansible.com/ansible/2.4/vault.html) en los playbooks de aprovisionamiento.

En primer lugar se ha procedido a cifrar la cadena mediante:

    ansible-vault encrypt_string password --ask-vault-pass

[Referencia](https://stackoverflow.com/questions/30209062/ansible-how-to-encrypt-some-variables-in-an-inventory-file-in-a-separate-vault). (Posdata: He dado like a dicho comentario de stackoverflow)

Esto nos producirá una codificación como la siguiente:

    !vault |
    $ANSIBLE_VAULT;1.1;AES256
    66386439653236336462626566653063336164663966303231363934653561363964363833
    3136626431626536303530376336343832656537303632313433360a626438346336353331

Dicha codificación se ha insertado en el correspondiente valor de la variable cifrada en el ansible-playbook.

- **[Ver en mi playbook del user-service](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/provision/azure/user_service/playbook_principal.yml).**

- **[Ver en mi playbook del task-service](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/provision/azure/task_service/playbook_principal.yml)**

Finalmente, se ha añadido a vagrant el parámetro `provision.ask_vault_pass=true` para que cuando se vaya a realizar el aprovisionamiento, se la añada la contraseña para descifrar dicha información.

---

# Desarrollo del servicio smartage (versión 5.0)

## Descripción de cambios.

Hasta ahora se había desarrollado un microservicio de tareas y otro referente a los usuarios e identificación.

En esta nueva versión se ha comunicado dichos microservicios entre sí, de forma que el microservicio de tareas va a utilizar el microservicio de login y usuarios para poder funcionar correctamente.

En la siguiente figura se muestra la arquitectura de la aplicación hasta la versión 4.

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/estructura_hito4.png)

En esta nueva versión, la arquitectura es la siguiente:

![Diagrama](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/diagrama_arquitectura.jpg)

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


---

## Comprobaciones del hito 5

- Comprobación de [@jmv74211](https://github.com/jmv74211) al aprovisionamiento de [@gecofer](https://github.com/Gecofer) disponible en este [enlace](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/correcci%C3%B3n_a_%40Gecofer_hito5.md).

- Comprobación de [@gecofer ](https://github.com/Gecofer) al aprovisionamiento de [@jmv74211](https://github.com/jmv74211) disponible en este [enlace](https://github.com/Gecofer/Proyecto-cloud-computing/blob/master/docs/hitos/comprobacion_hito5_de_%40Gecofer.md).

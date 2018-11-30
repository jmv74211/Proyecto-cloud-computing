
# Documentación del hito 3: Provisionamiento de máquinas virtuales

---

# Introducción

El objetivo de este hito es realizar un aprovisionamiento de una máquina virtual que
instale todo lo necesario para que se pueda desplegar correctamente la aplicación.

---

# Tecnología empleada

## VirtualBox

Como software de virtualización se ha utilizado **[VirtualBox](https://www.virtualbox.org/)**.

Se ha elegido virtualbox porque es un software de código abierto, gratuito y muy sencillo de usar. Además, parto con cierta experiencia en el uso de este software y es totalmente compatible con el resto de tecnologías que se van a utilizar en este hito.

## Vagrant

Aunque en este hito no era necesario utilizar esta herramienta, consideré muy útil poder crear, eliminar... un conjunto de máquinas virtuales ejecutando una simple orden, además de poder ejecutar directamente el aprovisionamiento de ansible a la vez que se cree la máquina virtual.

Además, el objetivo de la asignatura es poder desplegar de forma automática un servicio en la nube, y en este caso, vagrant sería el primer botón rojo que se pulsaría para crear el conjunto de infraestructuras necesarias para poder desplegar nuestra aplicación.

En primer lugar se ha instalado Vagrant y creado un directorio dentro del proyecto donde se ha realizado `vagrant init`.

Posteriormente se ha definido el archivo **[Vagrantfile]()** donde se ha especificado que la imagen del sistema operativo sea **Ubuntu 16.04LTS**.

Los motivos de elegir esta versión de sistema operativo como base para ejecutar la aplicación son los siguientes:
- Encontrar soluciones a los problemas de Ubuntu es mucho más fácil que otras versiones debido a que existe una gran comunidad de usuarios de ubuntu y a una extensa documentación.

- El servidor Ubuntu tiene una gran cantidad de soporte para implementaciones en contenedores y en la nube.

- Por lo general, los paquetes de software de Ubuntu están más actualizados que en Debian.

- Las nuevas tecnologías llegan antes a Ubuntu debido a las colaboraciones de Canonical y otras compañías.

- Estabilidad a largo plazo. Ubuntu ofrece soporte prolongado en sus versiones LTS para que se puedan seguir manteniendo y actualizando durante un largo periodo de tiempo.

El motivo de elegir la versión 16.04LTS ha sido porque he utilizado esta versión en otras prácticas de asignaturas y no he tenido ningún problema, y consultando foros hablan positivamente acerca de esta versión.

Los siguientes enlaces argumentan parcialmente la decisión que he tomado

- **[enlace 1](https://www.hostinger.es/tutoriales/centos-vs-ubuntu-elegir-servidor-web/#gref)**
- **[enlace 2](https://www.linuxadictos.com/debian-vs-ubuntu.html)**

Dicha especificación del SO la he realizado mediante la siguiente línea:

      config.vm.box = "ubuntu/xenial64"

A continuación se ha definido el nombre del host de la máquina, en este caso lo he llamado *smartage* debido al nombre de la aplicación que propuse.

      config.vm.hostname = "smartage"

Por último, en el Vagrantfile se ha especificado que se aprovisione la máquina con ansible y que ejecute nuestro playbook.

    config.vm.provision "ansible" do |ansible|
      ansible.playbook = "../provision/playbook_principal.yml"
    end

## Ansible

En este caso, se ha elegido ansible como software para aprovisionar nuestra máquina virtual. El principal motivo de esta elección, es que es muy sencillo de usar, basta con instarlo y configurar una serie de archivos que se describirán a continuación. Otro de los principales motivos de esta elección, es porque se realizó un seminario con esta herramienta, e incluso se mostraba como podía integrarse utilizando vagrant, por lo tanto, esta decisión ha sido la acertada.

Bien es cierto que también se ha podido utilizar otro software como por ejemplo Chef o Puppet, que ya veremos más adelante en un seminario, aunque para este hito lo más adecuado (en mi opinión) ha sido utilizar ansible.

Tras instalar ansible con `pip install ansible` (*anécdota: Inicialmente lo instalé con apt y me instaló una versión más antigua que no me funcionaba correctamente, tras instalarlo con pip me instaló la última versión y se arregló*), creé un directorio llamado provision (tal y como se indica en el hito) y dentro guardé los siguientes archivos:

### ansible.cfg

En este archivo nos permite modificar la configuración básica de ansible. En este caso este archivo tiene el siguiente contenido:

    [defaults]
    host_key_checking = False      
    inventory = ./ansible_hosts

`host_key_checking = False`: está a false para evitar la comprobación de de clave de ssh de forma que se puedan usar diferentes máquinas con la misma MAC sin que haya problema

`inventory = ./ansible_hosts`: Especifica la ubicación y nombre del fichero de host con el que se va a trabajar.

### ansible_hosts

Fichero con formato parecido a los init file de configuración que vamos a utilizar para definir lo siguiente:

      [vagrantboxes]
      smartage ansible_ssh_port=2222 ansible_ssh_host=127.0.0.1 ansible_ssh_private_key_file=./.vagrant/machines/default/virtualbox/private_key

      [vagrantboxes:vars]
      ansible_ssh_user=vagrant

En la sección de `[vagrantboxes]` vamos a definir el conjunto host que tenemos (en este caso solo uno) y a especificar la siguiente información para cada uno de ellos:

- `ansible_ssh_port`: Puerto ssh mediante el cuál vamos a acceder a la máquina. En este caso es 2222 porque vagrant por defecto utiliza este puerto.

- `ansible_ssh_host`: Se especifica la dirección de acceso para comunicarnos con la máquina. En este caso es la dirección 127.0.0.1 ya que estamos utilizando la dirección localhost.

- `ansible_ssh_private_key_file`: Para acceder a la máquina mediante ssh es necesaria tener la clave privada, y en este parámetro se especifica la dirección donde se encuentra dicha clave.

En la sección de `[vagrantboxes:vars]` vamos a definir la información global que se van a utilizar para todas las máquinas. En este caso tenemos la siguiente línea:

- `ansible_ssh_user`: Aquí se especifica el usuario que vamos a utilizar para acceder por ssh. En este caso se utiliza el usuario vagrant para todas las máquinas.

### ansible_playbook

En este archivo vamos a definir un archivo en formato .yaml para realizar las instrucciones de aprovisionamiento. En este caso se ha definido una serie de roles (que a su vez contienen otros playbook) que van a ejecutar una labor en concreta.

En este caso el playbook principal es el siguiente:

    - hosts: all
      gather_facts: False
      become: yes

      roles:
      - base
      - python3

Como breve resumen de este playbook, lo que vamos a hacer es que para todos los hosts (en este caso uno solo) vamos a ejecutar como superusuario los siguientes roles. Sinceramente, no sé exactamente (tras haber investigado sobre ello)el valor de gather facts. Tiene el valor de false porque inicialmente me daba error al ejecutar y estableciéndolo a false me funcionó. Según he visto (pero no entiendo muy bien) estableciéndolo a true sirve para llamar al módulo setup como primera tarea del playbook ([enlace](https://stackoverflow.com/questions/34485286/ansible-gathering-facts-with-filter-inside-a-playbook)).

Se puede consultar los archivos relacionados:

- [playbook_principal](): Describe el conjunto de roles que se van a usar para el aprovisionamiento.
- [Playbook_base](): Instala python mínimo, git y repositorio; además de configurar unas variables de entorno.
- [Playbook_python](): Instala python 3.6, pip3 y las dependencias necesarias para ejecutar correctamente la aplicación.

---

# Prueba de despliegue de la infraestructura y aprovisionamiento en local

Utilizando la configuración de vagrant y ansible del apartado anterior es super sencillo la creación de la máquina virtual y aprovisonamiento para que se pueda ejecutar nuestra aplicación.

Simplemente hay que lanzar `vagrant up` desde el directorio de vagrant (dentro del proyecto).

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/vagrant_up.png)

A continuación se creará la máquina virtual y se instalará todo lo necesario sin tener que hacer nada.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/provision.png)


Comprobamos que se ha creado la máquina virtual.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/mv_virtualbox.png)


Accedemos a dicha máquina virtual por `vagrant ssh`.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/vagrant_ssh.png)

Probamos lanzar la aplicación directamente, y comprobamos que se ejecuta correctamente.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/ejecutar_app.png)

A continuación abrimos otra terminal y volvemos a hacer `vagrant ssh`, y probamos que el servicio web esté funcionando.

Prueba 1

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/app_test1.png)

Prueba 2

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/app_test2.png)

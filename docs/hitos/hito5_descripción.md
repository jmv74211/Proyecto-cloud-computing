
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

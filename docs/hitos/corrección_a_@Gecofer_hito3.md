# Comprobación a **[@Gecofer](https://github.com/Gecofer/proyecto-CC)** del aprovisionamiento

---

# Tabla de contenidos

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->
<!-- END doctoc -->

- [Proceso de comprobación en máquina local con vagrant](#proceso-de-comprobaci%C3%B3n-en-m%C3%A1quina-local-con-vagrant)
- [Comprobación de la aplicación en azure.](#comprobaci%C3%B3n-de-la-aplicaci%C3%B3n-en-azure)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

---

# Introducción

Voy a comprobar el aprovisionamiento realizado por **[@Gecofer](https://github.com/Gecofer/)** en el hito número de 3 de la asignatura de cloud computing.

---

# Proceso de comprobación en máquina local con vagrant

En primer lugar he realizado un `fork` del repositorio y he clonado dicho fork a mi disco local.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test1_gecofer.png)

Comprobamos el contenido de dicho repositorio

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test2_gecofer.png)

A continuación, nos situamos en el directorio de vagrant y lanzamos `vagrant up` para crear la máquina virtual.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test3_gecofer.png)

Como podemos comprobar en la imagen anterior, se nos descarga una máquina con ubuntu trusty64.

En el proceso de instalación de la máquina virtual tiene programado que se ejecute el script de ansible para aprovisionar la máquina. En la siguiente imagen podemos comprobar que el aprovisionamiento se realiza correctamente.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test4_gecofer.png)

Al finalizar el proceso de instalación y aprovisionamiento, podemos comprobar que la máquina creado se está ejecutando.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test5_gecofer.png)

En la imagen anterior vemos que la máquina que se ha creado llamada **vagrant_ubuntu_default_154370** se iniciado automáticamente (debido a `vagrant up`)

A continuación iniciamos sesión con ssh a través de la orden `vagrant ssh`

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test6_gecofer.png)

Una vez iniciado sesión, procedemos a ejecutar la aplicación. En este momento vamos a comprobar si realmente se ha realizado correctamente el aprovisionamiento, ya que para ejecutar este proyecto se necesita instalar unas dependencias que supuestamente se han instalado en la fase del aprovisionamiento con ansible.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test7_gecofer.png)

Podemos comprobar que la aplicación se ha lanzado correctamente sin ningún problema. Podemos concluir que **EL APROVISIONAMIENTO SE HA REALIZADO CON ÉXITO**.

Finalmente probamos la respuesta dada por la aplicación al realizar las siguientes peticiones.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test8_gecofer.png)

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test9_gecofer.png)

---

# Comprobación de la aplicación en azure.

[@Gecofer](https://github.com/Gecofer/) ha desplegado dicha aplicación en el sistema cloud Azure. Dicha usuaria ha ejecutado el mismo playbook de ansible que el que he comprobado en la máquina virtual de vagrant, por lo que podemos afirmar que se ha realizado el mismo proceso de aprovisionamiento y se puede decir que **EL APROVISIONAMIENTO SE HA REALIZADO CON ÉXITO**.

Vamos a comprobar que el servicio realmente está disponible y devuelve la respuesta a las peticiones enviadas.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito3/test10_gecofer.png)

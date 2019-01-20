# Comprobación a **[@Gecofer](https://github.com/Gecofer/proyecto-CC)** del aprovisionamiento
---

# Introducción

Voy a comprobar el aprovisionamiento realizado por **[@Gecofer](https://github.com/Gecofer/)** en el hito número de 5 de la asignatura de cloud computing.

---

# Proceso de comprobación del hito 5

En primer lugar he realizado un `fork` del repositorio y he clonado dicho fork a mi disco local.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/clone.png)

A continuación me he situado en el directorio de orquestación (dentro de dicho repositorio) y he ejecutado lo siguiente: `vagrant up --no-parallel --provider=azure`

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/up.png)

Tras crearse la primera máquina, ha comenzado la fase de aprovisionamiento con ansible:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/provision1.png)

Como se puede observar, el proceso de aprovisionamiento se ha realizado con éxito. Ahora observamos como se crea la segunda máquina y se aprovisiona correctamente

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/provision2.png)

Tras terminar el proceso, comprobamos en Azure que efectivamente se han creado las dos máquinas virtuales

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/mvs.png)

Nos conectamos por ssh a la máquina principal y ejecutamos el servicio

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/exec.png)

Vemos como la aplicación se ejecuta correctamente.

A continuación vamos a acceder al servicio a través del navegador `40.89.156.93`

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/status1.png)

Vemos como efectivamente, el servicio funciona y se ha desplegado correctamente

Ahora accedemos a la parte de la base de datos, a través de la siguiente URL:
`40.89.156.93/BD`

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito5/status2.png)

La conclusión final de la comprobación es: **SE HA REALIZADO CON ÉXITO**

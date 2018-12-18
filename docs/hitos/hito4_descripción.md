
# Documentación del hito 4: Automatización de la creación de máquinas virtuales desde línea de órdenes

---

# Tabla de contenidos

---

# Introducción

El objetivo de este hito trata de usar los clientes de línea de órdenes de los servicios en la nube para crear instancias de máquinas virtuales en la nube y otros recursos necesarios para las mismas. Estas instancias, posteriormente, se provisionarán y se instalará en ella la aplicación que se ha venido usando hasta ahora.

---

# Tecnología empleada

## [Azure CLI](https://docs.microsoft.com/es-es/cli/azure/?view=azure-cli-latest)

La CLI de Azure es la experiencia de línea de comandos multiplataforma de Microsoft para administrar los recursos de Azure.

Azure CLI dispone de una gran serie de comandos para poder crear, eliminar.. y configurar todo tipo de parámetros de la máquina virtual. Los comandos básicos están disponibles en este [enlace](https://docs.microsoft.com/es-es/azure/virtual-machines/linux/cli-manage).

Se ha elegido virtualbox porque es un software de código abierto, gratuito y muy sencillo de usar. Además, parto con cierta experiencia en el uso de este software y es totalmente compatible con el resto de tecnologías que se van a utilizar en este hito.

## [Ansible](https://www.ansible.com/)

En este caso, se ha vuelto a elegir ansible como software para aprovisionar nuestra máquina virtual. Basta con añadir una línea adicional a nuestro script *acopio.sh* para que automáticamente se ejecuten nuestro playbooks que contienen las instrucciones necesarias para aprovisionar nuestra máquina.

Para saber más información acerca de los archivos generados para ansible, se puede consultar la [documentación del hito 3](https://github.com/jmv74211/Proyecto-cloud-computing/blob/master/docs/hitos/hito3_descripci%C3%B3n.md) donde se explica cada línea configurada.

---

# Instalación y configuración de Azure CLI

Si está ejecutando una distribución que viene con *apt*, como Ubuntu o Debian, hay un paquete de 64 bits disponible para la CLI de Azure. Este paquete se ha probado con:

- Ubuntu trusty, xenial, artful y bionic
- Debian wheezy, jessie y stretch

En primer lugar añadimos el repositorio a nuestra lista:

    sudo apt-get install apt-transport-https lsb-release software-properties-common -y
    AZ_REPO=$(lsb_release -cs)
    echo "deb [arch=amd64] https://packages.microsoft.com/repos/azure-cli/ $AZ_REPO main" | \
    sudo tee /etc/apt/sources.list.d/azure-cli.list

A continuación se obtiene la clave de firma de Microsoft:

    sudo apt-key --keyring /etc/apt/trusted.gpg.d/Microsoft.gpg adv \
     --keyserver packages.microsoft.com \
     --recv-keys BC528686B50D79E339D3721CEB3E94ADBE1229CF

Finalmente instalamos el CLI de Azure

    sudo apt-get update
    sudo apt-get install azure-cli


Después, ejecute la CLI de Azure con el comando `az`. Para iniciar sesión, hay que usar el comando:

    az login

Tras ejecutar dicho comando nos saldrá una ventana para introducir nuestras credenciales de acceso. Una vez introducidas correctamente, nos mostrará lo siguiente:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/1_azure login.png)

A continuación se nos mostrará la lista de suscripciones que tenemos:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/2_suscripciones.png)

Después elegimos la suscripción que queremos usar para poder trabajar con el resto de órdenes.

    az account set --subscription <name or id>

---

# Script de creación y aprovisionamiento en Azure

Para poder crear automáticamente una máquina virtual y aprovisionarla se ha creado un script llamado **[acopio.sh]()**. Dicho script contiene una serie de órdenes de Azure CLI para poder crear una máquina virtual con unos parámetros específicos. También se ejecuta ansible para aprovisionar dicha máquina creada.

A continuación se va a mostrar y explicar en qué consiste dicho script.

En primer lugar se declara un conjunto de variables que vamos a utilizar en las órdenes siguientes. Por ejemplo, el nombre del grupo de recurso, la localización del grupo de recurso, el nombre de la máquina virtual, un nombre para asociar a la IP pública, el nombre de la imagen del SO que vamos a utilizar y la ruta del playbook de ansible que vamos a ejecutar para aprovisionar la máquina virtual que se construya.

    ############# LOCATION VARS #############

    RESOURCE_GROUP_NAME="cc-resource-group-francecentral"
    LOCATION_RESOURCE_GROUP="francecentral"
    VIRTUAL_MACHINE_NAME="user-service"
    IP_NAME="user-service-public-ip-address"
    SO_IMAGE="Canonical:UbuntuServer:18.04-LTS:18.04.201812060"
    #SO_IMAGE="OpenLogic:CentOS:7.5:latest"
    PLAYBOOK_PATH="./provision/azure/playbook_principal.yml"

    #########################################

Como se puede observar, hay una línea comentada que se corresponde con la SO_IMAGE que se ha usado para especificar un [URN](https://docs.microsoft.com/es-es/azure/virtual-machines/linux/cli-ps-findimage) de dicha imagen. En el caso de que se desee utilizar una versión específica de una imagen, basta con añadir el URN a esta línea y todo se modificará correctamente.Por ejemplo, yo he obtenido dicho URN tras ejecutar la orden `az vm image list --offer Debian --all --output table`

Posteriormente se ha creado el grupo de recursos con los parámetros especificados.

    echo "======================================================== \n"
    echo "Creando el grupo de trabajo con los siguientes parámetros \n"
    echo "======================================================== \n"

    echo "resource-group = $RESOURCE_GROUP_NAME \n"
    echo "location = $LOCATION_RESOURCE_GROUP \n"

    #Creamos el grupo de trabajo
    az group create \
      --name $RESOURCE_GROUP_NAME \
      --location $LOCATION_RESOURCE_GROUP

    #########################################

Después se ha creado la máquina virtual especificando el grupo de recurso al que vamos a añadir dicha máquina, el nombre de la máquina, la imagen que vamos a utilizar para instalar nuestro sistema operativo, especificamos que se cree un par de clave pública y privada para poder autentificarnos y finalmente le damos un nombre a nuestra IP pública especificando que sea estática.

    #Creamos la máquina virtual
    az vm create \
      --resource-group $RESOURCE_GROUP_NAME \
      --name $VIRTUAL_MACHINE_NAME \
      --image $SO_IMAGE \
      --generate-ssh-keys \
      --public-ip-address-allocation static \
      --public-ip-address $IP_NAME

Tras crear dicha máquina, vamos a realizar una petición para consultar la dirección de la IP pública que se le ha asignado con el motivo de guardarla para despúes indicar dicha dirección en la orden de ansible para realizar el aprovisionamiento.

Para ello se ha filtrado la salida de la orden az ip show utilizando json query, ya que la salida por defecto de dicha orden te muestra un json con toda la información de la dirección IP de la máquina y con jq nos quedamos solo con el campo que especifica la dirección IP pública.

    # Obtiene la dirección IP pública de la máquina que acabamos de crear
    PUBLIC_IP=$(az network public-ip show --resource-group $RESOURCE_GROUP_NAME --name $IP_NAME | jq -r '.ipAddress')


A continuación se abren los puertos 80 y 22 para permitir el tráfico HTTP y SSH. Es importante especificar la prioridad de cada uno con un valor diferente, ya que en caso contrario no funcionará.

    #########################################

    echo "======================================================== \n"
    echo "         Configurando puertos HTTP Y SSH (80,22)         \n"
    echo "======================================================== \n"

    #Abrimos los puertos para HTTP Y SSH
    az vm open-port \
      --port 80 \
      --resource-group $RESOURCE_GROUP_NAME \
      --name $VIRTUAL_MACHINE_NAME \
      --priority 300

    az vm open-port \
      --port 22 \
      --resource-group $RESOURCE_GROUP_NAME \
      --name $VIRTUAL_MACHINE_NAME \
      --priority 320

Finalmente se ejecuta la orden de ansible para ejecutar el playbook de aprovisionamiento utilizando la dirección de la IP pública de la máquina virtual.

      echo "======================================================== \n"
      echo "              Provisionando la máquina                   \n"
      echo "======================================================== \n"

      #Ejecutamos el playbook principal de ansible para provisionar la máquina
      ansible-playbook -i $PUBLIC_IP, $PLAYBOOK_PATH


Tras ejecutar dicho script, observamos que el proceso se ha realizado correctamente:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/acopio-execute.png)

Comprobamos en el panel de control que se ha creado correctamente la máquina virtuales

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/panel-vm.png)

Y que tiene la dirección IP indicada de forma estática.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/ip-vm.png)

A continuación entramos por SSH y ejecutamos el servicio web en el puerto 80.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/ssh-mv.png)

Comprobamos que nos responde el servicio web en la dirección IP del servidor a través de una petición HTTP.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/mv-response-http.png)

---

# Elección de la ubicación del centro de datos

Azure tiene más regiones globales que cualquier otro proveedor de servicios en la nube, lo que le permite ofrecer la escala necesaria para acercar las aplicaciones a usuarios de todo el mundo. De este modo, mantiene la residencia de los datos y ofrece a los clientes opciones muy completas de cumplimiento normativo y resistencia. Podemos consultar la lista de regiones en este [enlace](https://azure.microsoft.com/es-es/global-infrastructure/regions/) y también en este otro [enlace](https://azure.microsoft.com/es-es/global-infrastructure/geographies/).

También te muestra las posibles regiones si te equivocas al elegir una.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/locations.png)

A la hora de crear la máquina virtual he tenido en cuenta que existen bastantes regiones y que lo más común es elegir la región más cercana a la ubicación actual para tener menos latencia y que la información ubicada en el centro de datos cumpla con la normativa y leyes del área geográfica donde está situado. Por ese motivo, he realizado diferentes pruebas eligiendo las regiones más cercanas a España y una alejada como es USA para observar con mayor detalle las posibles diferencias en rendimiento que puede haber teniendo en cuenta la distancia.

En este caso he realizado una prueba de rendimiento utilizando **[apache benchmak](https://httpd.apache.org/docs/2.4/programs/ab.html)** y ejecutando la aplicación en cinco máquinas virtuales ubicadas en las siguientes regiones:

- MV: CC-01 WestEurope
- MV: CC-02 NorthEurope
- MV: CC-03 EastUs
- MV: CC-04 CentralFrance
- MV: CC-05 WestUK


Para poder realizar estas pruebas, se han construido cinco máquinas virtuales utilizando el script **[acopio.sh](https://github.com/jmv74211/Proyecto-cloud-computing/acopio.sh)** y especificando los nuevos parámetros como el grupo de recursos, su ubicación y el nombre de la máquina.

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/vms.png)

El proceso de creación ha sido demasiado sencillo, ya que se han construido y aprovisionado dichas máquinas automáticamente gracias al script acopio.sh.

A continuación, se ha ejecutado en cada máquina el microservicio en el puerto 80.

El test se ha realizado utilizando la utilidad apache benchmark empleando la siguiente sintaxis.

    ab -n <número peticiones> -c <Número peticiones concurrentes> <direcciónIP>

En este caso, nos vamos a quedar con los datos de número de peticiones por segundo respondidas y la latencia correspondiente a la comunicación con el servidor.

Para poder realizar el test de forma automática, se ha creado un script que almacena en un [fichero](https://github.com/jmv74211/Proyecto-cloud-computing/files/) el número de peticiones que se han realizado junto con el número de peticiones contestadas y su latencia.

El [script](https://github.com/jmv74211/Proyecto-cloud-computing/files/script_abTest.sh) es el siguiente:

    #!/bin/bash

    #IP MV WEST-EU          CC-01:      51.136.25.13
    #IP MV NORTH-EU         CC-02:      137.116.232.139
    #IP MV EAST-US          CC-03:      40.121.10.71
    #IP MV CENTRAL-FRANCE   CC-04:      40.89.158.99
    #IP MV WEST-UK          CC-05:      51.141.31.225

    echo -e Número de peticiones '\t' Peticiones/sh '\t' LatenciaMedia > salida.txt
    echo ------------------------------------------------------------------------ >> salida.txt

    for (( c=500; c<=5000; c=c+500 ))
    do
      `ab -n $c -c 20 http://40.121.10.71/ > aux.txt`
      pts=`cat aux.txt | grep "Requests per second" | cut -d " " -f 7`
      ltm=`cat aux.txt | grep "Time per request" | head -n 1 | cut -d " " -f 10`
      echo -e $c '\t' $pts '\t' $ltm >> salida.txt
    done

    rm aux.txt

Básicamente lo que hace es realizar diferentes pruebas para un número de peticiones entre 500 y 5000 incrementándose en 500 en cada iteración con un número constante de 20 peticiones concurrentes, y almacenar la información en un fichero.

A continuación se ha creado un [script](https://github.com/jmv74211/Proyecto-cloud-computing/files/plot_result.py) de python que utiliza [matplotlib](https://matplotlib.org/) para representar la información que se ha almacenado en los ficheros(cada fichero corresponde con una ubicación geográfica diferente).

Las gráficas obtenidas son las siguientes:

![img](https://raw.githubusercontent.com/jmv74211/Proyecto-cloud-computing/master/images/hito4/comparativa_regiones.png)

Como se puede observar, se ha obtenido una latencia bastante elevada (alrededor de 200-300ms) en EastUs, una latencia moderada en NorthEurope (alrededor de 100-125ms) y una latencia baja en WestEurope, CentralFrance y WestUK ( más o menos por debajo de 100ms). La ubicación que menor latencia da, y por lo tanto que mayor número de peticiones responde por segundo es la situada en CentralFrance, por lo que se ha concluido que se va a utilizar la región de **CentralFrance** (además de que contiene la imagen del SO que se quiere instalar) para crear la máquina virtual que ejecute los servicios.

---

# Elección de la imagen del sistema operativo a instalar

Para poder elegir correctamente la imagen del sistema operativo que va a usar nuestra máquina virtual para ejecutar el servicio he estado buscando en la web recomendaciones e información para poder decidirme.

He leído todo tipo de foros y artículos( [este](https://www.solvetic.com/page/recopilaciones/s/recopilacion/mejores-distribuciones-para-servidor-linux) es uno de ellos que he considerado interesante).

Según una recopilación de información que he leído, la mayoría de los usuarios recomendaban usar **CentOS o UbuntuServer LTS** debido a la gran estabilidad que presenta CentOs y las constantes actualizaciones y gran comunidad de Ubuntu.

A continuación, he estado informándome más detenidamente acerca de esas dos distribuciones y he instado dos máquinas virtuales cada una con ese sistema operativo. La instalación la he realizado utilizando el script **acopio.sh** y buscando el URN de la imagen a través de los siguientes comandos de azure:

Para **UbuntuServer**:

      az vm image list --all -p Canonical -f UbuntuServer -s 18.04-LTS --output table

La imagen seleccionada es la siguiente:

    Offer         Publisher    Sku        Urn                                               Version
    ------------  -----------  ---------  ------------------------------------------------  ---------------
    UbuntuServer  Canonical    18.04-LTS  Canonical:UbuntuServer:18.04-LTS:18.04.201812060  18.04.201812060


Para **CentOS**:

    az vm image list --offer CentOs --output table

La imagen que se ha seleccionado es la siguiente:

    Offer    Publisher    Sku    Urn                          UrnAlias    Version
    -------  -----------  -----  ---------------------------  ----------  ---------
    CentOS   OpenLogic    7.5    OpenLogic:CentOS:7.5:latest  CentOS      latest

(Para cada resultado de ambas distribuciones he elegido la versión más actualizada).

Tras haber instalado dichas máquinas virtuales, he comprobado que UbuntuServer 18.04 LTS trae por defecto instalada la versión de python 3.6 que es la que necesita el proyecto, mientras que CentOS solo trae la versión 2.7. Además, también he leído que para utilizar aplicaciones y frameworks que usen python como Flask... es mejor UbuntuServer, ya que el número de actualizaciones es bastante más elevado y está añadiendo continuamente nuevas librerías y versiones de python, cosa que facilita bastante la tarea de administración y actualización de la aplicación.

Por estos motivos, he decidido que finalmente la imagen del sistema operativo que voy a utilizar para ejecutar mi aplicación en python sea **UbuntuServer 18.04 LTS** (Debido a esto, he suprimido un rol de ansible que era el encargado de instalar y configurar python 3.6.)

---

# Desarrollo del servicio smartage (versión 4.0)

Hasta ahora se había desarrollado un microservicio de tareas y otro referente a los usuarios e identificación.

Dado que en el hito 2 no entendí bien el concepto de servicio web, (realicé una estructura y contenido basado en rutas y parámetros, no en peticiones PUT,POST,GEST Y DELETE), he decidido que en este nuevo hito voy a implementar nuevamente dicho microservicio web junto con un proceso de identificación basado en un token de acceso que se envía en la cabecera de las peticiones, y un mecanismo de cifrado utilizando sha256 para las contraseñas de los usuarios.

El principal motivo de realizar este cambio en este hito, es que quiero tener apunto un servicio de tareas que necesite autenticación para su funcionamiento. Hasta ahora dichos servicios se utilizan de forma independiente, es decir, no se llama el uno al otro, pero como en el siguiente hito se tienen que orquestar varias máquinas virtuales, el objetivo es que cada microservicio se ejecute en una máquina, y que el servicio de tareas utilice el microservicio de usuarios e identificación para poder mostrar y gestionar dicha información.

Por ello, he vuelto a implementar dicho microservicio junto con sus correspondientes test, en el que se utiliza un token de acceso y una restricción de acceso a las diferentes funcionalidades.

## Guía y uso del microservicio de identificación y login

### Creación de usuarios

Para poder acceder al conjunto de funcionalidades (posteriormente será el conjunto de microservicios de la aplicación) es necesario crearse un usuario y posteriormente identificarse en el sistema. Empecemos creando un usuario mediante la siguiente petición **PUT**.

    [PUT] --> {
                'usuario':'nombreUsuario', 'password':'contraseña', 'email':'direccionEmail'
              } --> http://DirecciónIP/user

Si el usuario se ha creado correctamente nos devolverá el siguiente json:

    [RESPONSE] --> {
                      message' : 'New user created!
                   }

### Login

Tras haberse creado un usuario, el siguiente paso es identificarse en el sistema para poder acceder al conjunto de funcionalidades de la aplicación. Tras dicha identificación, se devolverá un mensaje de bienvenida al usuario y el token de sesión que se necesita enviar en la cabecera de cada petición para acceder a las diferentes funcionalidades.

Para ello realizamos una petición **POST** de la siguiente forma:

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

**Nota importante: A partir de ahora, será necesario haberse identificado y haber obtenido el token de acceso que se debe de enviar en la cabecera de todas las siguientes peticiones.**

### Listado de usuarios

Esta funcionalidad nos permite obtener un json con un listado de todos los usuarios registrados en el sistema. Esta funcionalidad solo estará disponible para usuarios que tienen el rol de administrador (dicho rol será descrito en un siguiente apartado).

Suponemos que un usuario administrador previamente identificado realiza la siguiente petición GET:

      [GET] --> {
                  headers={ 'content-type': 'application/json',
                            'access-token': 'tokenHash'
                          }
                } --> http://DirecciónIP/login

El microservicio nos responde con la información de los usuarios. Un ejemplo sería:

    [RESPONSE] --> {
                      users' :
                            {
                                "admin": "False",
                                "email": "email@correo.ugr.es",
                                "password": "sha256$8gyJWifM$78e76359473b9fefdbc888ec47eaa98571458b368ff74c19a7be68d7e6160c45",
                                "public_id": "b0c8b763-0bad-41bc-ad16-032cb8e3f10f",
                                "username": "usuarioPrueba"
                            },
                            {
                              ...
                            },...
                    }

Si intentamos listar los usuarios habiéndonos identificado con un usuario no administrador, se nos motrará el siguiente mensaje:

    [RESPONSE] --> {
                      'message' : 'You cannot perform that action!'
                   }

### Buscar información de un usuario

Esta funcionalidad nos permite mostrar la información de un usuario buscado a través de su *public id*. Un usuario administrador podrá ver la información de cualquier usuario, mientras que un usuario normal solo podrá ver su propia información y no la de los demás.

Para listar la información de un usuario, basta con realizar la siguiente petición GET:

    [GET] --> {
                headers={ 'content-type': 'application/json',
                          'access-token': 'tokenHash'
                        }
              } --> http://DirecciónIP/user/<public_id>

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

### Promocionar administrador a un usuario

Para promocionar a un usuario administrador, se puede utilizar la siguiente petición **POST**:

    [POST] --> {
                  headers={ 'content-type': 'application/json',
                            'access-token': 'tokenHash'
                          }
               } --> http://DirecciónIP/user/<public_id>

Si la petición se ha ejecutado correctamente, nso devolverá el siguiente mensaje:

    [RESPONSE] --> {
                      'message' : 'The user has been promoted!'
                   }


En el caso de que nos hayamos equivocado al escribir el identificador de usuario, se nos mostrará el siguiente mensaje de error:

    [RESPONSE] --> {
                      'message' : 'User not found!'
                   }

### Eliminar a un usuario

Esta funcionalidad nos permite eliminar permanentemente un usuario del sistema. Para eliminar a un usuario basta con realizar la siguiente petición **DELETE**:

    [DELETE] --> {
                    headers={ 'content-type': 'application/json',
                              'access-token': 'tokenHash'
                            }
                  } --> http://DirecciónIP/user/<public_id>

Tras eliminar al usuario, se nos devolverá un mensaje con código de error 204.

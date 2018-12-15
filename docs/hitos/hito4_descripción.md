
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

    RESOURCE_GROUP_NAME="cc-resource-group"
    LOCATION_RESOURCE_GROUP="westeurope"
    VIRTUAL_MACHINE_NAME="CC-02"
    IP_NAME="CC-02-public-ip-address"
    SO_IMAGE="UbuntuLTS"
    #SO_IMAGE="credativ:Debian:10-DAILY:10.0.201811290"
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

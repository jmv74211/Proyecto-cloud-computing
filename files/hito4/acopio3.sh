
############# LOCATION VARS #############

RESOURCE_GROUP_NAME="cc-resource-group-EastUS"
LOCATION_RESOURCE_GROUP="EastUS"
VIRTUAL_MACHINE_NAME="CC-03"
IP_NAME="CC-03-public-ip-address"
SO_IMAGE="UbuntuLTS"
#SO_IMAGE="credativ:Debian:10-DAILY:10.0.201811290"
PLAYBOOK_PATH="./provision/azure/playbook_principal.yml"

#########################################

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

echo "======================================================== \n"
echo "Creando la máquina virtual con los siguientes parámetros \n"
echo "======================================================== \n"


echo "virtual_machine_name = $VIRTUAL_MACHINE_NAME \n"
echo "resource-group = $RESOURCE_GROUP_NAME \n"
echo "SO_image= $SO_IMAGE \n"

#Creamos la máquina virtual
az vm create \
  --resource-group $RESOURCE_GROUP_NAME \
  --name $VIRTUAL_MACHINE_NAME \
  --image $SO_IMAGE \
  --generate-ssh-keys \
  --public-ip-address-allocation static \
  --public-ip-address $IP_NAME

# Obtiene la dirección IP pública de la máquina que acabamos de crear
PUBLIC_IP=$(az network public-ip show --resource-group $RESOURCE_GROUP_NAME --name $IP_NAME | jq -r '.ipAddress')

#########################################

echo "======================================================== \n"
echo "         Configurando puertos HTTP Y SSH (80,22) \n"
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

#########################################

echo "======================================================== \n"
echo "              Provisionando la máquina \n"
echo "======================================================== \n"

#Ejecutamos el playbook principal de ansible para provisionar la máquina
ansible-playbook -i $PUBLIC_IP, $PLAYBOOK_PATH


############# LOCATION VARS #############

USER_SERVICE_PORT="80:80" # 80 en máquina, 80 en contenedor
TASK_SERVICE_PORT="5000:80" #100 en máquina, 80 en contenedor
ENVIRONMENT_VARS_LIST="./env.list"
TASK_SERVICE_IMAGE="jmv74211/task_service"
USER_SERVICE_IMAGE="jmv74211/user_service"

PATH_USER_SERVICE_DOCKERFILE="contenedores/user_service/Dockerfile"
PATH_TASK_SERVICE_DOCKERFILE="contenedores/task_service/Dockerfile"

########################################

echo "======================================================== \n"
echo "Creando la imagen del user_service \n"
echo "======================================================== \n"

docker build -t $USER_SERVICE_IMAGE  --build-arg mongoVar=${MONGODB_USERS_KEY} --build-arg passVar=${ENCODING_PHRASE} -f $PATH_USER_SERVICE_DOCKERFILE .

echo "======================================================== \n"
echo "Creando la imagen del task_service \n"
echo "======================================================== \n"

docker build -t $TASK_SERVICE_IMAGE --build-arg passVar=${ENCODING_PHRASE} -f $PATH_TASK_SERVICE_DOCKERFILE .

echo "======================================================== \n"
echo "Ejecuta el contenedor de user_service \n"
echo "======================================================== \n"

docker run -d -p $USER_SERVICE_PORT --name user_service $USER_SERVICE_IMAGE

echo "======================================================== \n"
echo "Ejecuta el contenedor de task_service \n"
echo "======================================================== \n"

docker run -d -p $TASK_SERVICE_PORT --name task_service $TASK_SERVICE_IMAGE

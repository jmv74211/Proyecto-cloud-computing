# -*- coding: utf-8 -*-

# TEST PARA COMPROBAR LAS RESPUESTAS DADAS POR EL MICROSERVICIO TAREAS USANDO USER-SERVICE

import unittest

import sys
sys.path.append("../app/task_service")
sys.path.append("src/app/task_service")

from task_class import Task
import task_model as model
from task_service import *

import requests
import json

# Test de las peticiones que devuelve el microservicio de identificación y registro
class TestTaskService(unittest.TestCase):
    # Variables estáticas
    token = ""
    userId= ""

    @classmethod
    def setUpClass(self):
        print("Ejecutando conjunto de tests de peticiones en el servicio de tareas")

        self.app=app.test_client()

        self.user_test = 'jmv74211'
        self.password_user_test = 'jmv74211'

        self.user = 'testUserExclusive'
        self.name = 'task name'
        self.description = 'task_description'
        self.estimation = 5
        self.difficulty = 8
        self.max_date = 'task max_date'

        self.task_object_test = Task(self.user,self.name,self.description,
        self.estimation,self.difficulty,self.max_date)

        self.task_id = self.task_object_test.task_id

        self.put_data = json.dumps({ "user": self.user, "name": self.name, "description": self.description,"estimation": self.estimation, "difficulty": self.difficulty, "max_date": self.max_date})
        #self.put_data = "{ 'user': 'testUserExclusive', 'name': 'task name', 'description': 'task_description','estimation': 5, 'difficulty': 8, 'max_date': 'task max_date'}"



################################################################################


    # Test para hacer login y obtener el token de sesión
    def test_1_login(self):

        # Realizamos la petición para autenticarnos pasando las credenciales
        req = requests.post('http://0.0.0.0:5000/login' ,auth=(self.user_test, self.password_user_test))
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Almacenamos el token de identificación para utilizarlo en las siguientes comprobaciones.
        TestTaskService.token = output['token']
        print(TestTaskService.token)

    #Test para comprobar si se crea correctamente una tarea con PUT y elimina con DELETE
    def test_2_PUT_DELETE_service(self):

        print('test_PUT_DELETE_service')

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestTaskService.token}

        #Petición PUT al servidor
        req =  self.app.put('/task',data=self.put_data, headers= headers)

        print(req.data)
        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 201)

        output = req.data.decode('utf8')
        result = json.loads(output)

        #Comprobamos que al salida sea insertado
        self.assertTrue(result['result'] == 'inserted')

        #Comprobamos que se haya insertado dicha tarea
        self.assertTrue(model.exist(result['id']))

        #Petición DELETE al servidor para eliminar la tarea

        req =  self.app.delete('/task', headers= headers
        ,data=json.dumps({ "task_id": result['id'] }))

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 204)

        #Comprobamos que la tarea se ha eliminado.
        self.assertFalse(model.exist(result['id']))


################################################################################

#Test para comprobar si se muestran correctamente las tareas con GET.

    def test_3_GET_service(self):

        print('test_GET_service')

        #Petición GET no válida al servidor
        req = self.app.get('/rutaNoValida')

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 404)

        #Insertamos la tarea
        model.insert_task(self.task_object_test)

        #Comprobamos que se haya creado dicha tarea
        self.assertTrue(model.exist(self.task_id))

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestTaskService.token}

        #Petición GET al servidor
        req = self.app.get('/task', headers = headers)
        output = req.data.decode('utf8')
        list = json.loads(output)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

        tasks = []

        for x in list['result']:
            result = eval(x)
            tasks.append(result['user'])

        #Comprobamos que el usuario de test está en la lista devuelta por GET
        self.assertTrue(self.user in tasks)

        #Eliminamos la tarea de prueba
        model.delete_task(self.task_id)

        #Comprobamos que se ha eliminado la tarea de prueba
        self.assertFalse(model.exist(self.task_id))

################################################################################

#Test para comprobar si se muestran correctamente las tareas con GET.
    def test_4_UPDATE_service(self):

        print('test_UPDATE_service')

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestTaskService.token}

        #Insertamos al tarea
        model.insert_task(self.task_object_test)

        #Comprobamos que se haya creado dicha tarea
        self.assertTrue(model.exist(self.task_id))

        #Creamos los nuevos datos para asociar a esa tarea

        new_name ="Update task"
        new_estimation =10
        new_max_date = "2018-12-30"

        post_data = json.dumps({ "task_id":self.task_id,"user": self.user,
        "name": new_name, "description": self.description,
        "estimation": new_estimation, "difficulty": self.difficulty , "max_date": new_max_date})

        #Petición POST al servidor
        req = self.app.post('/task',data=post_data, headers=headers)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

        #Comprobamos los nuevos datos de dicha tarea
        self.assertEqual(model.get_name(self.task_id),new_name)

        self.assertEqual(model.get_estimation(self.task_id),new_estimation)

        self.assertEqual(model.get_max_date(self.task_id),new_max_date)

        #Eliminamos la tarea de prueba
        model.delete_task(self.task_id)

        #Comprobamos que se ha eliminado la tarea de prueba
        self.assertFalse(model.exist(self.task_id))

################################################################################

    def test_5_PUT_user_service(self):

        headers={'content-type': 'application/json'}
        put_data = json.dumps({ "username": "UsuarioPruebaPutTaskService", "password": "pwdtestUser", "email": "emailPutUserTest@gmail.com"})

        req = self.app.put('/user',data=put_data, headers=headers)

        # Comprobamos que se devuelve el estado Created
        self.assertEqual(req.status_code, 201)
        output = json.loads(req.data.decode('utf8'))

        # Comprobamos que se devuelve el mensaje de usuario creado
        self.assertEqual(output['message'], 'New user created!')

################################################################################

    def test_6_GET_user_service(self):

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestTaskService.token}

        req = self.app.get('/user/UsuarioPruebaPutTaskService', headers=headers)

        # Comprobamos que devuelve status OK
        self.assertEqual(req.status_code, 200)
        output = json.loads(req.data.decode('utf8'))

        result = output['user']

        # Comprobamos que el usuario existe y obtenemos su información
        self.assertEqual(result['username'], 'UsuarioPruebaPutTaskService')

################################################################################

    def test_7_POST_user_service(self):

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestTaskService.token}

        req = self.app.post('/user/UsuarioPruebaPutTaskService', headers=headers)

        # Comprobamos que devuelve status OK
        self.assertEqual(req.status_code, 200)
        output = json.loads(req.data.decode('utf8'))

        # Comprobamos que se informa al usuario de dicha acción
        self.assertEqual(output['message'], 'The user has been promoted!')

################################################################################

    def test_8_DELETE_user_service(self):

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestTaskService.token}

        req = self.app.delete('/user/UsuarioPruebaPutTaskService', headers=headers)

        #output = json.loads(req.data.decode('utf8'))
        print(req.data)

        # Comprobamos que devuelve status 204 NO CONTENT
        self.assertEqual(req.status_code, 204)


if __name__ == '__main__':
     unittest.main()

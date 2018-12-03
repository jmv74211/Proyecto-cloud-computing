# -*- coding: utf-8 -*-

# TEST PARA COMPROBAR LAS RESPUESTAS DADAS POR EL MICROSERVICIO TAREAS

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

    @classmethod
    def setUpClass(self):
        print("Ejecutando conjunto de tests de peticiones en el servicio de tareas")

        self.app=app.test_client()

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


    #Test para comprobar si se crea correctamente una tarea con PUT y elimina con DELETE
    def test_PUT_DELETE_service(self):

        print('test_PUT_DELETE_service')

        #Petición PUT al servidor
        req =  self.app.put('/task',data=self.put_data, headers={'content-type': 'application/json'})

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 201)

        output = req.data.decode('utf8')
        result = json.loads(output)

        #Comprobamos que al salida sea insertado
        self.assertTrue(result['result'] == 'inserted')

        #Comprobamos que se haya insertado dicha tarea
        self.assertTrue(model.exist(result['id']))

        #Petición DELETE al servidor para eliminar la tarea

        req =  self.app.delete('/task', headers={'content-type': 'application/json'}
        ,data=json.dumps({ "task_id": result['id'] }))

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 204)

        #Comprobamos que la tarea se ha eliminado.
        self.assertFalse(model.exist(result['id']))


################################################################################

#Test para comprobar si se muestran correctamente las tareas con GET.
    def test_GET_service(self):

        print('test_GET_service')

        #Petición GET no válida al servidor
        req = self.app.get('/rutaNoValida')

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 404)

        #Insertamos al tarea
        model.insert_task(self.task_object_test)

        #Comprobamos que se haya creado dicha tarea
        self.assertTrue(model.exist(self.task_id))

        #Petición GET al servidor
        req = self.app.get('/task')
        output = req.data.decode('utf8')
        list = json.loads(output)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

        tasks = []

        for x in list['result']:
           tasks.append((eval(list['result'][0])['user']))

        #Comprobamos que el usuario de test está en la lista devuelta por GET
        self.assertTrue(self.user in tasks)

        #Eliminamos la tarea de prueba
        model.delete_task(self.task_id)

        #Comprobamos que se ha eliminado la tarea de prueba
        self.assertFalse(model.exist(self.task_id))

################################################################################

#Test para comprobar si se muestran correctamente las tareas con GET.
    def test_UPDATE_service(self):

        print('test_UPDATE_service')

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
        req = self.app.post('/task',data=post_data, headers={'content-type': 'application/json'})

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


if __name__ == '__main__':
     unittest.main()

# -*- coding: utf-8 -*-

# TEST PARA COMPROBAR LAS FUNCIONES IMPLEMENTADAS EN EL MICROSERVICIO LOGIN-REGISTRO

import unittest

import sys
sys.path.append('../app/task_service')
sys.path.append('src/app/task_service')

from task_class import Task
import task_model as model

from flask import request
import json

# Test de las funciones del microservicio de identificación y registro
class TestFunctionsTaskModel(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print('Ejecutando conjunto de tests en funciones locales del servicio de tareas')
        self.user = 'testUser'
        self.name = 'task name'
        self.description = 'task_description'
        self.estimation = 5
        self.difficulty = 8
        self.max_date = 'task max_date'

        self.task_object_test = Task(self.user,self.name,self.description,
        self.estimation,self.difficulty,self.max_date)

        self.task_id = self.task_object_test.task_id

################################################################################

    def test_insert_task(self):

        print('test_insert')

        self.assertFalse(model.exist(self.task_id))

        model.insert_task(self.task_object_test)

        self.assertTrue(model.exist(self.task_id))

        model.delete_task(self.task_id)

        self.assertFalse(model.exist(self.task_id))

################################################################################

    def test_update_task(self):

        print('test_update')

        model.insert_task(self.task_object_test)

        new_name = 'Hito 3 CC'
        new_max_date = '2018-12-30'

        new_data = { 'user': self.user, 'name': new_name, 'description': self.description,
        'estimation':self.estimation, 'difficulty':self.difficulty, 'max_date':new_max_date }

        self.assertTrue(model.exist(self.task_id))

        model.update_task(self.task_id,new_data)

        self.assertEqual(model.get_name(self.task_id), new_name)

        self.assertEqual(model.get_max_date(self.task_id),new_max_date)

        model.delete_task(self.task_object_test.task_id)

        self.assertFalse(model.exist(self.task_id))

################################################################################

    def test_delete_task(self):

        print('test_delete')

        model.insert_task(self.task_object_test)

        self.assertTrue(model.exist(self.task_id))

        model.delete_task(self.task_id)

        self.assertFalse(model.exist(self.task_id))

################################################################################

    def test_getters(self):

        print('test_getters')

        model.insert_task(self.task_object_test)

        self.assertTrue(model.exist(self.task_id))

        self.assertEqual(model.get_user(self.task_id),self.user)

        self.assertEqual(model.get_name(self.task_id),self.name)

        self.assertEqual(model.get_description(self.task_id),self.description)

        self.assertEqual(model.get_estimation(self.task_id),self.estimation)

        self.assertEqual(model.get_difficulty(self.task_id),self.difficulty)

        self.assertEqual(model.get_max_date(self.task_id),self.max_date)

        model.delete_task(self.task_id)

        self.assertFalse(model.exist(self.task_id))


if __name__ == '__main__':
     unittest.main()

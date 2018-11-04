# -*- coding: utf-8 -*-

import unittest
from servicio_login_registro import Users
import requests
import json





class TestLoginRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Ejecutando conjunto de tests")
        cls.fakeName="asda123asd21"
        cls.userRegistered="jmv74211"


    def test_checkUsers(self):

        # Comprobamos que existe el usuario jmv74211 que está ya creado
        self.assertEqual(Users.query.filter(Users.username == self.userRegistered).count(), 1)

        # Comprobamos que no existe un usuario
        self.assertNotEqual(Users.query.filter(Users.username == self.fakeName).count(), 1)


    def test_users(self):

        #Petición GET al servidor
        req = requests.get('http://127.0.0.1:8000/users')

        #Comprobamos que el servidor está ON
        self.assertEqual(req.status_code, 200)

        result=json.dumps(req.json()) #Convierte de python a JSON
        list = json.loads(result) #Convierte de JSON a python

        users=[]

        for x in list['result']:
           users.append(x["usuario"])

        self.assertTrue(self.userRegistered in users)
        self.assertTrue("npc93" in users)
        self.assertTrue("fagomez" in users)
        self.assertFalse(self.fakeName in users)


if __name__ == '__main__':
     unittest.main()

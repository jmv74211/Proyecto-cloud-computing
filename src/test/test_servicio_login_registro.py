# -*- coding: utf-8 -*-

import unittest

import sys
sys.path.append("../app/servicio_login_registro")

from servicio_login_registro import *
import requests
import json

# Test de las peticiones que devuelve el microservicio de identificación y registro
class TestLoginRegisterService(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Ejecutando conjunto de tests de peticiones")
        cls.fakeName = "asda123asd21"
        cls.userRegistered = "jmv74211"
        cls.passwordUserRegistered = "pwdcc"


################################################################################

    #Test para comprobar si se muestran correctamente los usuarios predefinidos.
    def test_get_all_users_service(self):

        #Petición GET al servidor
        req = requests.get('http://127.0.0.1:8000/users')

        #Comprobamos que el servidor está ON
        self.assertEqual(req.status_code, 200)

        result = json.dumps(req.json()) #Convierte de python a JSON
        list = json.loads(result) #Convierte de JSON a python

        users = []

        for x in list['result']:
           users.append(x["usuario"])

        self.assertTrue(self.userRegistered in users)
        self.assertTrue("npc93" in users)
        self.assertTrue("fagomez" in users)
        self.assertFalse(self.fakeName in users)

################################################################################

    #Test para comprobar si se autentican los usuarios definidos
    def test_identify_service(self):

        ##  PRUEBA DE LOGIN CORRECTA ##

        #Petición GET al servidor
        req = requests.get('http://127.0.0.1:8000/identify/' + self.userRegistered
         + '/' + self.passwordUserRegistered)

        #Comprobamos que el servidor está ON
        self.assertEqual(req.status_code, 200)

        result = json.dumps(req.json()) #Convierte de python a JSON
        result = json.loads(result) #Convierte de JSON a python

        self.assertTrue(result['Details'] == 'LOGGED')

        ##  PRUEBA DE LOGIN USUARIO INCORRECTO ##

        #Petición2 GET al servidor
        req = requests.get('http://127.0.0.1:8000/identify/' + self.fakeName +'/pwdcc')

        result = json.dumps(req.json()) #Convierte de python a JSON
        result = json.loads(result) #Convierte de JSON a python

        self.assertTrue(result['Details'] == 'El usuario no existe')


        ##  PRUEBA DE LOGIN PASSWORD INCORRECTO ##

        #Petición2 GET al servidor
        req = requests.get('http://127.0.0.1:8000/identify/' + self.userRegistered
        + '/' + self.fakeName)

        result = json.dumps(req.json()) #Convierte de python a JSON
        result = json.loads(result) #Convierte de JSON a python

        self.assertTrue(result['Details'] == 'Password incorrecto')

################################################################################

    #Test para comprobar si se añade un usuario ficticio

    def test_add_user_service(self):

        userName = "prueba123zxc"
        userPassword = "pwdprueba"
        userEmail = "userzxc@gmail.com"

        #Petición GET al servidor
        req = requests.get('http://127.0.0.1:8000/register/' + userName
         + '/' + userPassword + '/' + userEmail)

        #Comprobamos que el servidor está ON
        self.assertEqual(req.status_code, 200)

        self.assertTrue(check_user(userName))

        # Se elimina al usuario ficticio que hemos creado
        x = Users.query.filter(Users.username == userName).first()
        x.remove()

        self.assertFalse(check_user(userName))


if __name__ == '__main__':
     unittest.main()

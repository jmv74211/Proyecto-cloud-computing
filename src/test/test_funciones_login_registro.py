# -*- coding: utf-8 -*-

# TEST PARA COMPROBAR LAS FUNCIONES IMPLEMENTADAS EN EL MICROSERVICIO LOGIN-REGISTRO

import unittest

import sys
sys.path.append("../app/servicio_login_registro")
sys.path.append("src/app/servicio_login_registro")

from servicio_login_registro import *
from flask import request
import json

# Test de las funciones del microservicio de identificación y registro
class TestFunctionsLoginRegister(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        print("Ejecutando conjunto de tests en funciones locales")
        cls.fakeName = "asda123asd21"
        cls.userRegistered = "jmv74211"
        cls.passwordUserRegistered = "pwdcc"

################################################################################

    #Test para comprobar si existe un usuario ya creado o no.
    def test_check_users(self):

        # Comprobamos que existe el usuario jmv74211 que está ya creado
        self.assertEqual(check_user(self.userRegistered),1)

        # Comprobamos que no existe un usuario
        self.assertNotEqual(check_user(self.fakeName),1)

################################################################################

    #Test para comprobar si se muestran correctamente los usuarios predefinidos.

    def test_get_all_users(self):

        # Solución a  RuntimeError: working outside of application context same
        # is happening on calling
        with app.app_context():
            req = get_all_users()
            data_list = req.get_json()

            users = []

            for data in data_list['result']:
                users.append(data["usuario"])

            self.assertTrue(self.userRegistered in users)
            self.assertTrue("npc93" in users)
            self.assertTrue("fagomez" in users)
            self.assertFalse(self.fakeName in users)

################################################################################

    #Test para comprobar si se autentican los usuarios definidos
    def test_identify(self):

        with app.app_context():

            ##  PRUEBA DE LOGIN CORRECTA ##

            req = identify(self.userRegistered,self.passwordUserRegistered)
            data = req.get_json()
            self.assertTrue(data['Details'] == 'LOGGED')

            ##  PRUEBA DE LOGIN USUARIO INCORRECTO ##

            req = identify(self.fakeName,self.fakeName)
            data = req.get_json()
            self.assertTrue(data['Details'] == 'El usuario no existe')


            ##  PRUEBA DE LOGIN PASSWORD INCORRECTO ##

            req = identify(self.userRegistered,self.fakeName)
            data = req.get_json()
            self.assertTrue(data['Details'] == 'Password incorrecto')


################################################################################

    #Test para comprobar si se añade un usuario ficticio

    def test_add_user(self):

        userName = "prueba123zxc"
        userPassword = "pwdprueba"
        userEmail = "userzxc@gmail.com"

        with app.app_context():
            add_user(userName,userPassword,userEmail)

            self.assertTrue(check_user(userName))

            # Se elimina al usuario ficticio que hemos creado
            x = Users.query.filter(Users.username == userName).first()
            x.remove()

            self.assertFalse(check_user(userName))

if __name__ == '__main__':
     unittest.main()

# -*- coding: utf-8 -*-

# TEST PARA COMPROBAR LAS RESPUESTAS DADAS POR EL MICROSERVICIO LOGIN-REGISTRO

import unittest

import sys
sys.path.append("../app/servicio_login_registro")
sys.path.append("src/app/servicio_login_registro")

from servicio_login_registro import *
import requests
import json

# Test de las peticiones que devuelve el microservicio de identificación y registro
class TestLoginRegisterService(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        print("Ejecutando conjunto de tests de peticiones")
        self.fakeName = "asda123asd21"
        self.userRegistered = "jmv74211"
        self.passwordUserRegistered = "pwdcc"
        self.app=app.test_client()


################################################################################

    #Test para comprobar si se muestran correctamente los usuarios predefinidos.
    def test_get_all_users_service(self):

        #Petición GET no válida al servidor
        req = self.app.get('/rutaNoValida')

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 404)

        #Petición GET al servidor
        req = self.app.get('/users')
        output = req.data.decode('utf8')
        list = json.loads(output)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

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
        req =  self.app.get('/identify/' + self.userRegistered
         + '/' + self.passwordUserRegistered)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        output = req.data.decode('utf8')
        result = json.loads(output)

        self.assertTrue(result['Details'] == 'LOGGED')

        ##  PRUEBA DE LOGIN USUARIO INCORRECTO ##

        #Petición2 GET al servidor
        req = self.app.get('/identify/' + self.fakeName +'/pwdcc')

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

        output = req.data.decode('utf8')
        result = json.loads(output)

        self.assertTrue(result['Details'] == 'El usuario no existe')


        ##  PRUEBA DE LOGIN PASSWORD INCORRECTO ##

        #Petición2 GET al servidor
        req = self.app.get('/identify/' + self.userRegistered + '/' + self.fakeName)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

        output = req.data.decode('utf8')
        result = json.loads(output)

        self.assertTrue(result['Details'] == 'Password incorrecto')

################################################################################

    #Test para comprobar si se añade un usuario ficticio

    def test_add_user_service(self):

        userName = "prueba123zxc"
        userPassword = "pwdprueba"
        userEmail = "userzxc@gmail.com"

        #Petición GET al servidor
        req = self.app.get('/register/' + userName
         + '/' + userPassword + '/' + userEmail)

        #Comprobamos el estado de la respuesta
        self.assertEqual(req.status_code, 200)

        #Comprobamos el tipo de contenido que devuelve la petición GET
        self.assertEqual(req.headers['content-type'],'application/json')

        self.assertTrue(check_user(userName))

        # Se elimina al usuario ficticio que hemos creado
        x = Users.query.filter(Users.username == userName).first()
        x.remove()

        self.assertFalse(check_user(userName))


if __name__ == '__main__':
     unittest.main()

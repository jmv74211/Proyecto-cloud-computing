# -*- coding: utf-8 -*-

# TEST PARA COMPROBAR LAS FUNCIONES IMPLEMENTADAS EN EL MICROSERVICIO USER_SERVICE

import unittest

import sys
sys.path.append("../app/user_service")
sys.path.append("src/app/user_service")

from user_service import *
import requests
import json

# Test de las funciones del servicio de usuarios
class TestUserService(unittest.TestCase):

    # Variables estáticas
    token = ""
    public_id = ""

    @classmethod
    def setUpClass(self):

        # Variables locales de la clase
        print("Ejecutando conjunto de tests de user_service")
        self.app=app.test_client()
        self.user_test = "asda123asd21"
        self.password_user_test= "pwdcc"
        self.email_test = "emailtesting2@correo.nothing.es"
        self.user2_test = "bbhjbjghjhj"
        self.password_user2_test= "pwdcc"
        self.email2_test = "email2dtesting@correo.nothing.es"
        self.put_data = json.dumps({ "username": self.user_test,
            "password": self.password_user_test, "email": self.email_test})

        self.data_user_test_two = json.dumps({ "username": self.user2_test,
            "password": self.password_user2_test, "email": self.email2_test})

################################################################################

    # Test para comprobar una ruta inválida
    def test_1_invalid_path(self):

        # Petición GET de una ruta no válida al servidor
        req = self.app.get('/rutaNoValida')
        self.assertEqual(req.status_code, 404)

################################################################################

    # Test para comprobar el estado del servidor
    def test_2_status(self):

        req =  self.app.get('/')
        self.assertEqual(req.status_code, 200)
        output = json.loads(req.data.decode('utf8'))

        #Comprobamos que el estado sea OK
        self.assertEqual(output['status'], 'OK')

################################################################################

    #Test para comprobar si un usuario se crea correctamente
    def test_3_PUT_user(self):

        # Realizamos petición para añadir un usuario
        req =  self.app.put('/user',data=self.put_data, headers={'content-type': 'application/json'})

        # Comprobamos que se devuelve el estado Created
        self.assertEqual(req.status_code, 201)
        output = json.loads(req.data.decode('utf8'))

        # Comprobamos que se devuelve el mensaje de usuario creado
        self.assertEqual(output['message'], 'New user created!')

        # Guardamos su identificador para posteriormente usarlo en las búsquedas.
        TestUserService.public_id = output['public_id']

################################################################################

    # Test para hacer login y obtener el token de sesión
    def test_4_login(self):

        # Realizamos la petición para autenticarnos pasando las credenciales
        req = requests.post('http://127.0.0.1:5000/login' ,auth=(self.user_test, self.password_user_test))
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Almacenamos el token de identificación para utilizarlo en las siguientes comprobaciones.
        TestUserService.token = output['token']

################################################################################

    # Test para comprobar privilegios de usuario y mostrar los usuarios del sistema
    def test_5_GET_all_users(self):

        # Intentamos acceder al listado de usuarios sin identificarnos
        req = self.app.get('/user')
        self.assertEqual(req.status_code, 401)

        # Comprobamos que nos devuelve el mensaje para que nos identifiquemos
        output = json.loads(req.data.decode('utf8'))
        self.assertEqual(output['message'], 'Autentication token is missing!')

        # Definimos la cabecera utilizando el token de acceso
        headers={'content-type': 'application/json', 'access-token': TestUserService.token}

        # Volvemos a realizar la petición para ver el listado de usuarios, pero no tenemos
        # permiso para visualizarlo dado que no somos administrador
        req = requests.get('http://127.0.0.1:5000/user', headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Nos muestra el mensaje de que no tenemos permiso para realizar dicha acción
        self.assertEqual(output['message'], 'You cannot perform that action!')

        # Ahora damos privilegios de administrador a dicho usuario
        req = requests.post('http://127.0.0.1:5000/user/' + TestUserService.public_id, headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Comprobamos que se informa al usuario de dicha acción
        self.assertEqual(output['message'], 'The user has been promoted!')

        # Volvemos a realizar la petición para mostrar los usuarios
        req = requests.get('http://127.0.0.1:5000/user', headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Comprobamos que se devuelve el listado de usuarios
        self.assertFalse(output['users']==None)

################################################################################

    # Test para comprobar los resultados de la búsqueda de un usuario
    def test_6_GET_info_user(self):

        # Definimos la cabecera con el token de sesión
        headers={'content-type': 'application/json', 'access-token': TestUserService.token}

        req = requests.get('http://127.0.0.1:5000/user/1212ad', headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()
        self.assertEqual(output['message'], 'User not found!')

        req = requests.get('http://127.0.0.1:5000/user/'+TestUserService.public_id, headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()
        self.assertFalse(output['user']==None)

        # Añade otro usuarios para realizar pruebas de acceso
        req =  self.app.put('/user',data=self.data_user_test_two, headers={'content-type': 'application/json'})

        self.assertEqual(req.status_code, 201)
        output = json.loads(req.data.decode('utf8'))
        self.assertEqual(output['message'], 'New user created!')
        user_two_public_id = output['public_id']

        # Comprobamos que el primer usuario con privilegios de administrador puede visualizar
        # el contenido de este segundo usuario.

        req = requests.get('http://127.0.0.1:5000/user/'+ user_two_public_id, headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()
        # Comprobamos que devuelve la información del usuario
        self.assertFalse(output['user']==None)

        # Ahora se va a comprobar que el segundo usuario sin privilegios de administrador
        # no puede visualizar la información del primer usuario

        # Hacemos login con el segundo usuario
        req = requests.post('http://127.0.0.1:5000/login' ,auth=(self.user2_test, self.password_user2_test))
        self.assertEqual(req.status_code, 200)
        output = req.json()

        #Almacenamos el token de identificación para utilizarlo en las siguientes comprobaciones.
        token_user_two = output['token']

        # Ahora intentamos visualizar la información de otro usuario con la sesión de
        # el usuario sin privilegios de administrador.
        req = requests.get('http://127.0.0.1:5000/user/'+TestUserService.public_id,
            headers={'content-type': 'application/json', 'access-token': token_user_two})
        self.assertEqual(req.status_code, 401)
        output = req.json()

        # Nos muestra el mensaje de que no tenemos permiso para realizar dicha acción
        self.assertEqual(output['message'], 'You cannot perform that action!')

        # Eliminamos al segundo usuario
        req = requests.delete('http://127.0.0.1:5000/user/' + user_two_public_id,
            headers={'content-type': 'application/json', 'access-token': token_user_two})
        self.assertEqual(req.status_code, 204)

################################################################################

    # Test para comprobar la concesión de privilegios de administrador a un usuario
    def test_7_POST_admin_promotion(self):

        # Definimos la cabecera con el token de sesión
        headers={'content-type': 'application/json', 'access-token': TestUserService.token}

        # Ahora damos privilegios de administrador a dicho usuario
        req = requests.post('http://127.0.0.1:5000/user/' + TestUserService.public_id, headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Comprobamos que se informa al usuario de dicha acción
        self.assertEqual(output['message'], 'The user has been promoted!')

        # Realizamos petición para ver si tenemos permisos para listar usuarios
        req = requests.get('http://127.0.0.1:5000/user', headers=headers)
        self.assertEqual(req.status_code, 200)
        output = req.json()

        # Comprobamos que se devuelve el listado de usuarios
        self.assertFalse(output['users']==None)

################################################################################

    # Test para comprobar el borrado de usuarios
    def test_8_DELETE_user(self):

        # Definimos la cabecera con el token de sesión
        headers={'content-type': 'application/json', 'access-token': TestUserService.token}

        # Ahora damos privilegios de administrador a dicho usuario
        req = requests.delete('http://127.0.0.1:5000/user/' + TestUserService.public_id, headers=headers)
        self.assertEqual(req.status_code, 204)

################################################################################

if __name__ == '__main__':
     unittest.main()

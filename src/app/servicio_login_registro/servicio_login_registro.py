# -*- coding: utf-8 -*-

# SERVICIO LOGIN-REGISTRO

from flask import Flask,jsonify
from flask_mongoalchemy import MongoAlchemy
import os

app = Flask(__name__)

#Parámetros del servidor
app.config["MONGOALCHEMY_DATABASE"] = "heroku_5tv2mk96"

# Variable de entorno para la conexión con la Base de datos
app.config["MONGOALCHEMY_CONNECTION_STRING"] = os.environ.get('MONGODB_USERS_KEY')

db = MongoAlchemy(app)

# Colección Usuarios
class Users(db.Document):
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()

# Comprueba si un usuario ya está registrado
def check_user(_username):
    return Users.query.filter(Users.username == _username).count()

@app.route("/")
# Muestra comandos de ayuda
def index():
    return  jsonify({'status':'OK'})


@app.route("/users", methods=['GET'])
# Muestra todos los usuarios registrados
def get_all_users():
    users = Users.query.all()

    results = []

    for user in users:
        results.append({'email': user.email, 'password':user.password, 'usuario':user.username})

    if len(results) == 0:
        results.append({'result':"No hay ningun usuario"})

    return jsonify({'result': results})

# Comprueba si el login de un usuario es correcto
@app.route("/identify/<string:_username>/<string:_password>",methods=['GET'])
def identify(_username,_password):

    if not check_user(_username):
        result = {'Details':"El usuario no existe"}
    else:
        user = Users.query.filter(Users.username == _username and Users.password ==_password).count()

        if not user:
            result = {'Details':"Password incorrecto"}
        else:
            result = {'Details': "LOGGED"}

    return jsonify(result)

# Registro de un usuario en el sistema
@app.route("/register/<string:_username>/<string:_password>/<string:_email>",methods=['GET'])
def add_user(_username,_password,_email):

    if not check_user(_username):
        userAdd = Users(username=_username, password=_password, email=_email)
        userAdd.save()

        result = jsonify({'Details': "El usuario ha sido creado correctamente"})
    else:
        result = jsonify({'Details': "Error al crear usuario: El usuario ya existe"})

    return result


if __name__ == "__main__":
app.run(debug=True)

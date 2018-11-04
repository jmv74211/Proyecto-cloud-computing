# -*- coding: utf-8 -*-

from flask import Flask,jsonify
from flask_mongoalchemy import MongoAlchemy

app = Flask(__name__)

#Parámetros del servidor
app.config["MONGOALCHEMY_DATABASE"] = "users"

db = MongoAlchemy(app)

# Colección Usuarios
class Users(db.Document):
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()

# Comprueba si un usuario ya está registrado
def checkUser(_username):
    return Users.query.filter(Users.username == _username).count()

@app.route("/")
# Muestra comandos de ayuda
def index():
    return  jsonify({'result': "Ayuda --- Ver usuarios: /users ||||  Registrar usuario: /register/usuario/password/email ||||  Identificarse /identify/usuario/password"})

# Muestra todos los usuarios registrados
@app.route("/users", methods=['GET'])
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

    if not checkUser(_username):
        result={'Details':"El usuario no existe"}
    else:
        user = Users.query.filter(Users.username == _username and Users.password==_password).count()

        if not user:
            result={'Details':"Password incorrecto"}
        else:
            result={'Details': "LOGGED"}

    return jsonify(result)

# Registro de un usuario en el sistema
@app.route("/register/<string:_username>/<string:_password>/<string:_email>",methods=['GET'])
def add_user(_username,_password,_email):
    userAdd=Users(username=_username, password=_password, email=_email)
    userAdd.save()

    return jsonify({'result': "El usuario ha sido creado correctamente"})


if __name__ == "__main__":
    app.run(debug=True,port=8000)
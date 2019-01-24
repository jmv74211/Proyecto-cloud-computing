from flask import Flask, request, jsonify, make_response
from flask_mongoalchemy import MongoAlchemy

import os

# Para generar aleatoriamente un public_id
import uuid

# Para cifrar la contraseña y autenticarla --
from werkzeug.security import generate_password_hash, check_password_hash

#Para codificar y decodificar  JSON Web Tokens -- https://pyjwt.readthedocs.io/en/latest/
import jwt

#Para codificar el token utilizando el tiempo
import datetime

#Para usar un decorador sin perder información sobre la función reemplazada.
#https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
from functools import wraps

import json

###############################################################################

app = Flask(__name__)

#Parámetros del servidor
app.config["MONGOALCHEMY_DATABASE"] = "heroku_5tv2mk96"

# Variable de entorno para la conexión con la Base de datos
app.config["MONGOALCHEMY_CONNECTION_STRING"] = os.environ.get('MONGODB_USERS_KEY')

#Clave secreta para codificar el token
app.config['SECRET_KEY'] = os.environ.get('ENCODING_PHRASE')

db = MongoAlchemy(app)

###############################################################################

"""
Clase para representar a los usuarios
"""
class User(db.Document):
    public_id = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    admin = db.StringField()

###############################################################################

"""
Función decorador que se encarga de la validación del token de acceso.
"""
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = None

        if 'access-token' in request.headers:
            token = request.headers['access-token']

        if not token:
            return jsonify({'message' : 'Autentication token is missing!'}), 401
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'])
            current_user = User.query.filter_by(username = data['public_username']).first()
        except:
            return jsonify({'message' : 'Autentication token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

###############################################################################

"""
Función que muestra el estado del servicio.
"""
@app.route('/', methods=['GET'])
def index():
    return  jsonify({'status':'OK'})

###############################################################################

"""
Función que muestra el estado del servicio.
"""
@app.route('/status', methods=['GET'])
def index_status():
    return  jsonify({'status':'OK'})


###############################################################################
"""
Función para crear un usuario.
"""
@app.route('/user', methods=['PUT'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id = str(uuid.uuid4()), username = data['username'],
        password = hashed_password, email = data['email'], admin = 'False')

    new_user.save()

    return jsonify({'message' : 'New user created!', 'public_id' : new_user.public_id}),201

###############################################################################

"""
Función para mostrar todos los usuarios del sistema. Solo un usuario administrador
podrá listar a todos los usuarios del sistema
"""
@app.route('/user', methods=['GET'])
@token_required
def get_all_users(current_user):

    if current_user.admin == "False":
        return jsonify({'message' : 'You cannot perform that action!'})
    else:
        users = User.query.all()
        output = []

        for user in users:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['username'] = user.username
            user_data['password'] = user.password
            user_data['email'] = user.email
            user_data['admin'] = user.admin
            output.append(user_data)

        return jsonify({'users' : output})

###############################################################################

"""
Función para mostrar los datos del usuario
"""
@app.route('/user/<user_id>', methods=['GET'])
@token_required
def get_user(current_user,user_id):

    user = User.query.filter_by(username = user_id).first()

    if not user:
        return jsonify({'message' : 'User not found!'})

    if current_user.admin == "False":
        #Si no es administrador y pide obtener sus datos -> se muestran
        if current_user.username == user_id:
            user_data = {}
            user_data['public_id'] = user.public_id
            user_data['username'] = user.username
            user_data['password'] = user.password
            user_data['email'] = user.email
            user_data['admin'] = user.admin
            return jsonify({'user' : user_data})
        #Si intenta listar datos de otro usuario, entonces se deniega
        else:
            return jsonify({'message' : 'You cannot perform that action!'}),401
    # El usuario actual es administrador -> puede listar cualquier usuario
    else:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['admin'] = user.admin

        return jsonify({'user' : user_data})

###############################################################################

"""
Función para eliminar a un usuario.
"""
@app.route('/user/<user_id>', methods=['DELETE'])
@token_required
def delete_user(current_user,user_id):

    user = User.query.filter_by(username = user_id).first()

    if not user:
        #return make_response('{ \"message\" : \"User not found!\" }', 204)
        jsonify({'message' : 'User not found!'})

    user.remove()

    return jsonify({'message' : 'The user has been deleted'})
    #return make_response('{ \"message\" : \"The user has been deleted!\" }', 204)

###############################################################################

"""
Función para promocionar administrador a un usuario.
"""
@app.route('/user/<user_id>', methods=['POST'])
@token_required
def promote_user(current_user, user_id):

    user = User.query.filter_by(username = user_id).first()

    if not user:
        return jsonify({'message' : 'User not found!'})

    user.admin = "True"
    user.save()

    return jsonify({'message' : 'The user has been promoted!'})

###############################################################################

@app.route('/checkLogin', methods=['POST'])
def chekLogin():

    data = request.data
    result = json.loads(data)

    user = result['username']
    password = result['password']

    # Elimina el último caracter en blanco que mete el formulario por defecto
    temp = len(user)
    if user[temp-1] == " ":
        user = user[:temp - 1]

    user = User.query.filter_by(username = user).first()

    if not user:
        return make_response('{ \"result\" : \"User does not exist!\" }', 401,
        {'WWW-Authenticate' :'Basic realm="Login required!"'})

    if check_password_hash(user.password, password):
        return make_response('{ \"result\":\"true\"}', 200,
        {'WWW.Authenticate' : 'Basic realm="Login required!"'})
    else:
        return make_response('{ \"result\":\"Password incorrect!\"}', 401,
        {'WWW.Authenticate' : 'Basic realm="Login required!"'})

"""
Función que comprueba los datos de acceso y genera el token de autenticación.
"""

@app.route('/login', methods=['POST'])
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('{ \"result\" : \"Could not verify, invalid arguments!\" }', 401,
        {'WWW-Authenticate' :'Basic realm="Login required!"'})

    user = User.query.filter_by(username = auth.username).first()

    if not user:
        return make_response('{ \"result\" : \"User does not exist!\" }', 401,
        {'WWW-Authenticate' :'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_username' : auth.username,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'])

        return jsonify({'message' : 'Bienvenid@ ' + user.username,
        'token' : token.decode('UTF-8')})
    else:
        return make_response('{ \"result\":\"Password incorrect!\"}', 401,
        {'WWW.Authenticate' : 'Basic realm="Login required!"'})

###############################################################################

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)

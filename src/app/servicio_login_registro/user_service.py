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

###############################################################################

app = Flask(__name__)

#Parámetros del servidor
app.config["MONGOALCHEMY_DATABASE"] = "heroku_5tv2mk96"

# Variable de entorno para la conexión con la Base de datos
app.config["MONGOALCHEMY_CONNECTION_STRING"] = os.environ.get('MONGODB_USERS_KEY')

#Clave secreta para codificar el token
app.config['SECRET_KEY'] = 'thiswillbeasecreykey'

db = MongoAlchemy(app)

###############################################################################

# Clase para representar a los usuarios
class User(db.Document):
    public_id = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    admin = db.StringField()

###############################################################################

@app.route('/user', methods=['PUT'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id = str(uuid.uuid4()), username = data['username'],
        password = hashed_password, email = data['email'], admin = 'False')

    new_user.save()

    return jsonify({'message' : 'New user created!'})

###############################################################################

@app.route('/user', methods=['GET'])
def get_all_users():
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

@app.route('/user/<user_id>', methods=['GET'])
def get_user(user_id):

    user = User.query.filter_by(public_id = user_id).first()

    if not user:
        return jsonify({'message' : 'User not found!'})
    else:
        user_data = {}
        user_data['public_id'] = user.public_id
        user_data['username'] = user.username
        user_data['password'] = user.password
        user_data['email'] = user.email
        user_data['admin'] = user.admin

        return jsonify({'user' : user_data})

###############################################################################

@app.route('/user/<user_id>', methods=['DELETE'])
def delete_user(user_id):

    user = User.query.filter_by(public_id = user_id).first()

    if not user:
        return jsonify({'message' : 'User not found!'})

    user.remove()

    return jsonify({'message' : 'The user has been deleted!'})

###############################################################################

@app.route('/login')
def login():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('Could not verify, invalid arguments!', 401,
        {'WWW-Authenticate' :'Basic realm="Login required!"'})

    user = User.query.filter_by(username = auth.username).first()

    if not user:
        return make_response('User does not exist!', 401,
        {'WWW-Authenticate' :'Basic realm="Login required!"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode({'public_id' : user.public_id,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'])

        return jsonify({'token' : token.decode('UTF-8')})
    else:
        return make_response('Password incorrect!', 401,
        {'WWW.Authenticate' : 'Basic realm="Login required!"'})



if __name__ == "__main__":
    app.run(debug=True)

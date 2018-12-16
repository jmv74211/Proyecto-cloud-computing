from flask import Flask, request, jsonify
from flask_mongoalchemy import MongoAlchemy

import os

# Para generar aleatoriamente un public_id
import uuid

# Para cifrar la contraseña y autenticarla --
from werkzeug.security import generate_password_hash, check_password_hash

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

if __name__ == "__main__":
    app.run(debug=True)

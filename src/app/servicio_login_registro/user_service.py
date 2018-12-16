from flask import Flask, request, jsonify, make_response
from flask_mongoalchemy import MongoAlchemy

import os

app = Flask(__name__)

#Parámetros del servidor
app.config["MONGOALCHEMY_DATABASE"] = "heroku_5tv2mk96"

# Variable de entorno para la conexión con la Base de datos
app.config["MONGOALCHEMY_CONNECTION_STRING"] = os.environ.get('MONGODB_USERS_KEY')

#Clave secreta para codificar el token
app.config['SECRET_KEY'] = 'thiswillbeasecreykey'

db = MongoAlchemy(app)

# Clase para representar a los usuarios
class User(db.Document):
    public_id = db.StringField()
    username = db.StringField()
    password = db.StringField()
    email = db.StringField()
    admin = db.StringField()


@app.route('/user', methods=['PUT'])
def create_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id = str(uuid.uuid4()), username = data['username'],
        password = hashed_password, email = data['email'], admin = 'False')

    new_user.save()

    return jsonify({'message' : 'New user created!'})


if __name__ == "__main__":
    app.run(debug=True)

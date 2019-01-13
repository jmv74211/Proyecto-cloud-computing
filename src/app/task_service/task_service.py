# -*- coding: utf-8 -*-

# SERVICIO TAREA

from flask import Flask,jsonify,make_response
import os
from flask import request,redirect,url_for
from task_class import Task
import task_model as model
import requests
import json

#Para usar un decorador sin perder información sobre la función reemplazada.
#https://stackoverflow.com/questions/308999/what-does-functools-wraps-do
from functools import wraps

#Para codificar y decodificar  JSON Web Tokens -- https://pyjwt.readthedocs.io/en/latest/
import jwt

#Para codificar el token utilizando el tiempo
import datetime

app = Flask(__name__)

#Clave secreta para codificar el token
app.config['SECRET_KEY'] = os.environ.get('ENCODING_PHRASE')

#URL del microservicio de usuarios
user_service_url = "127.0.0.1:5000"

@app.route("/")
def index():
    return  jsonify({'status':'OK'})

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

            r = requests.get("http://" + user_service_url + "/user/"+ data['public_username'] +"", headers=request.headers)
            result = r.json()
            current_user = result ['user']
        except:
            return jsonify({'message' : 'Autentication token is invalid!'}), 401

        return f(current_user, *args, **kwargs)


    return decorated


@app.route('/user', methods=['PUT'])
def add_user():
    r = requests.put("http://" + user_service_url + "/user", headers=request.headers, data = request.data);

    return make_response(jsonify(r.json()), 201)


@app.route('/user/<user_id>',  methods=['GET', 'POST', 'DELETE'])
# Utiliza otro microservicio para la identificación y registro de usuarios
@token_required
def user_proccess(current_user,user_id):
    if request.method == 'GET':
        r = requests.get("http://" + user_service_url + "/user/" + user_id + "", headers=request.headers);
        code = 200
    elif request.method == 'DELETE':
        r = requests.delete("http://" + user_service_url + "/user/" + user_id + "", headers=request.headers);
        code = 204
    elif request.method == 'POST':
        r = requests.post("http://" + user_service_url + "/user/" + user_id + "", headers=request.headers, data = request.data);
        code = 200

    data = r.json()

    return jsonify(data), code

@app.route("/task", methods=['GET', 'PUT', 'POST', 'DELETE'])
# Muestra todos los usuarios registrados
@token_required
def manage_task(current_user):
    if request.method == 'GET':
        data_list = model.get_all_tasks()
        return jsonify({'result':data_list})

    elif request.method == 'PUT':
        object_task = Task(request.json['user'],request.json['name'], request.json['description'],
        request.json['estimation'], request.json['difficulty'], request.json['max_date'])

        if(model.insert_task(object_task)):
            return jsonify({'result':'inserted', 'id':object_task.task_id}),201
        else:
            return jsonify({'result':'Error, not inserted'}),400

    elif request.method == 'DELETE':
        delete_task_id = request.json['task_id']

        if(model.delete_task(delete_task_id)):
            return jsonify({'result':'deleted'}),204
        else:
            return jsonify({'result':'Error, not deleted'}),204

    elif request.method == 'POST':
        if model.exist(request.json['task_id']):
            new_data = {
                "task_id": request.json['task_id'],
                "user": request.json['user'],
                "name": request.json['name'],
                "description": request.json['description'],
                "estimation": request.json['estimation'],
                "difficulty": request.json['difficulty'],
                "max_date": request.json['max_date']
            }

            model.update_task(request.json['task_id'],new_data)

            return jsonify({'status':"updated",'result':new_data}),200

        else:
            return jsonify({'result':'no content'}),204


@app.route('/login', methods=['POST'])
def login():

    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response(jsonify({'result' : 'Could not verify, invalid arguments!'}), 401,
        {'WWW-Authenticate' :'Basic realm="Login required!"'})

    data = "{ \"username\" : \"" + auth.username + " \", \"password\" : \"" + auth.password + "\" }";

    r = requests.post("http://" + user_service_url + "/checkLogin", headers=request.headers, data = data)

    json = r.json()
    result = json['result']

    if result == "true":
        token = jwt.encode({'public_username' : auth.username,
        'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=30)},
        app.config['SECRET_KEY'])

        return jsonify({'message' : 'Bienvenid@ ' + auth.username,
        'token' : token.decode('UTF-8')})

    elif result == "Password incorrect!" :
        return make_response(jsonify({'result' : 'Password incorrect!'}), 401,
        {'WWW.Authenticate' : 'Basic realm="Login required!"'})

    elif result == "User does not exist!":
        return make_response(jsonify({'result' : 'User does not exist!'}), 401,
        {'WWW.Authenticate' : 'Basic realm="Login required!"'})

if __name__ == "__main__":
    app.run(debug=True, port=3000)

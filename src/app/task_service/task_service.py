# -*- coding: utf-8 -*-

# SERVICIO TAREA

from flask import Flask,jsonify
import os
from flask import request,redirect,url_for
from task_class import Task
import task_model as model
import requests
import json

app = Flask(__name__)

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
            current_user = User.query.filter_by(public_id = data['public_id']).first()
        except:
            return jsonify({'message' : 'Autentication token is invalid!'}), 401

        return f(current_user, *args, **kwargs)

    return decorated

@app.route('/login', methods=['POST'])
# Utiliza otro microservicio para la identificación y registro de usuarios
def login():

    r = requests.post("http://127.0.0.1:5000/login", headers=request.headers);

    return jsonify(r.json())


@app.route('/user/<user_id>',  methods=['GET', 'PUT', 'POST', 'DELETE'])
# Utiliza otro microservicio para la identificación y registro de usuarios
def user_proccess():

    if request.method == 'GET':
        print("http://127.0.0.1:5000/user/" + user_id + "")
        r = requests.post("http://127.0.0.1:5000/user/" + user_id + "", headers=request.headers, data = request.data);

    return jsonify(r.json())


@app.route("/task", methods=['GET', 'PUT', 'POST', 'DELETE'])
# Muestra todos los usuarios registrados
def manage_task():
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


if __name__ == "__main__":
    app.run(debug=True, port=3000)

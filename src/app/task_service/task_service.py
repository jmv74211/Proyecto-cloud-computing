# -*- coding: utf-8 -*-

# SERVICIO TAREA

from flask import Flask,jsonify
import os
from flask import request
from task_class import Task
import task_model as model

app = Flask(__name__)

@app.route("/")
def index():
    return  jsonify({'status':'OK'})


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

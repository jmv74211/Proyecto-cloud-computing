import sys

sys.path.append("../app/class")
sys.path.append("src/app/servicio_login_registro")

import pymongo
import os
from class import task



myclient = pymongo.MongoClient(os.environ.get('MONGODB_USERS_KEY'))
database_name = "heroku_5tv2mk96"
collection_name = "tasks"

mydb = myclient[database_name]
mycol = mydb[collection_name]

def collection_init():
    if not collection_name in collist:
      mydict = { "task_id":0, "user": "jmv74211", "description": "Entregar hito3 CC", "estimation":5, "difficulty":8, "max_date":"2018-12-03" }
      mycol.insert_one(mydict)

def get_user(query_task_id):
    return mydb.collection_name.find( { task_id: query_task_id }, { user: 1, _id: 0 } )

def get_description(_task_id):
    return mydb.collection_name.find( { task_id: query_task_id }, { description: 1, _id: 0 } )

def get_estimation(_task_id):
    return mydb.collection_name.find( { task_id: query_task_id }, { estimation: 1, _id: 0 } )

def get_difficulty(_task_id):
    return mydb.collection_name.find( { task_id: query_task_id }, { difficulty: 1, _id: 0 } )

def get_max_date(_task_id):
    return mydb.collection_name.find( { task_id: query_task_id }, { max_date: 1, _id: 0 } )

def

import sys

import pymongo
import os

import task_class


myclient = pymongo.MongoClient(os.environ.get('MONGODB_USERS_KEY'))
database_name = "heroku_5tv2mk96"

mydb = myclient.get_database(database_name)
collection = mydb.tasks

def get_user(query_task_id):
    result = collection.find_one( {"task_id": query_task_id } )
    return result['user']

def get_description(query_task_id):
    result = collection.find_one( {"task_id": query_task_id } )
    return result['description']

def get_name(query_task_id):
    result = collection.find_one( {"task_id": query_task_id } )
    return result['name']

def get_estimation(query_task_id):
    result = collection.find_one( {"task_id": query_task_id } )
    return result['estimation']

def get_difficulty(query_task_id):
    result = collection.find_one( {"task_id": query_task_id } )
    return result['difficulty']

def get_max_date(query_task_id):
    result = collection.find_one( {"task_id": query_task_id } )
    return result['max_date']

def get_task_info(query_task_id):
    result = collection.find_one( {"task_id": query_task_id }, {"_id": False})
    return repr(result)

def get_all_tasks():

    data_list = []

    for row in collection.find({}, {"_id":False}):
        data_list.append(repr(row))

    return data_list

def insert_task(task_object):
    collection.insert_one(task_object.to_dict())
    return exist(task_object.task_id)

def delete_task(query_task_id):
    myquery = { "task_id": query_task_id }
    collection.delete_one(myquery)
    return not exist(query_task_id)

def update_task(query_task_id, new_data):
    collection.update_one( {'task_id': query_task_id}, {'$set': new_data} )

def exist(query_task_id):
    results = collection.count( {'task_id': query_task_id})
    return results

def get_next_task_id():
    if(collection.count() > 0):
        result = collection.find().sort('task_id', pymongo.DESCENDING).limit(1)
        return ((result[0]['task_id']) +1)
    else:
        return 0

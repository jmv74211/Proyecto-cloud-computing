from flask import Flask,jsonify
import requests
import json

"""
    Aplicación de prueba que realiza peticiones al microservicio login-registro para realizar
    peticiones y observar la salida generada por éste.

    NO TIENE IMPACTO EN NINGÚN MICROSERVICIO, SOLO ES DE PRUEBA
"""
app= Flask(__name__)

@app.route("/")

def index():
    req = requests.get('http://127.0.0.1:8000/')
    result=json.dumps(req.json())
    return result

@app.route("/users")
def get_users():
    req = requests.get('http://127.0.0.1:8000/users')
    result = json.dumps(req.json())

    return result


@app.route("/identify/<string:_username>/<string:_password>")
def identify(_username,_password):
    req = requests.get("http://127.0.0.1:8000/identify/"+_username +"/"+_password)
    result = json.dumps(req.json())

    x = json.loads(result)
    print (x['Details'])

    return result

@app.route("/register/<string:_username>/<string:_password>/<string:_email>")
def register(_username,_password,_email):
    req = requests.get("http://127.0.0.1:8000/"+_username+"/"+_password+"/"+_email)
    result = json.dumps(req.json())
    return result


if __name__ == "__main__":
    app.run(debug=True,port=8150)

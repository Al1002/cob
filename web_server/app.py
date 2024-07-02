import flask
from flask import Flask
from flask import request
import requests


app = Flask(__name__)

@app.route("/upload_files", methods=['POST'])
def upload():
    files = request.files.lists() # (name, [values])
    responce_body = ''
    for pair in files:
        responce_body += str(pair)
        
    return flask.Response(responce_body, 200)

@app.route("/hello_world")
def hello_world():
    return '<p>Hello world!</p>'

app.run()
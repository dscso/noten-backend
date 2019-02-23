import os
import inspect
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from time import time
import datetime


# import sys
# print(sys.path)

# initialize 'app' with Flask instance
app = Flask(__name__)
CORS(app)
f=open("secret.key", "r")
app.secret_key = f.read()
print(app.secret_key)
#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

from models import *
from auth import auth, login_required, usertype_required, decor

# Hello.
print("Mip.")

# ROUTING

@app.route("/css/<path:path>")
def css(path):
    return send_from_directory('templates/css', path)

@app.route("/img/<path:path>")
def img(path):
    return send_from_directory("templates/img", path)

@app.route("/")
@login_required
def index():
    #TODO load index file
    return "index here"

@app.route("/login", methods=['POST'])
def login():
    try:
        param = request.get_json()
        mail = param['mail']
        password = param['password']
        user = auth(mail, password)
    except:
         return sendError(400, "Bad request")
    if (user != False):
        return jsonify(user.json())
    else:
        return sendError(401, "Login Failed")

# TODO add user exists check!!!
@app.route("/register", methods=["GET","POST"])
def register():
    if(request.method == 'POST'):
        mail = request.args.get("mail")
        pwhash = request.args.get("hash")
        name = request.args.get("name")
        firstname = request.args.get("firstname")
        if(mail != None and hash != None):
            u = User(mail=mail, name=name, firstname=firstname, pwhash=pwhash)
            db.session.add(u)
            db.session.commit()
            return "created"
        else:
            return sendError(400, "Bad request")
    else:
        return sendError(405, "Method not allowed")

@app.route("/ccp")
@usertype_required(2)
def ccp():
    return "skkrrr"

def sendError(code, msg="", cause=""):
    return jsonify({"error": code, "msg":msg}), code

def get(json, name):
    try:
        return json[name]
    except:
        return None

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)

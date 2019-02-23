import os
import inspect
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from time import time
import datetime

# initialize 'app' with Flask instance
app = Flask(__name__)
# Cross origin
CORS(app)

# secret key (currently not needet)
f=open("secret.key", "r")
app.secret_key = f.read()

#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

from models import *
from auth import auth, login_required, usertype_required


@app.route("/")
def index():
    return jsonify({
        "version":"v0.1"
    })

# ----------------------------  LOGIN  ---------------------------------------

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

# ----------------------- Get user data ---------------------------------------------

@app.route("/user/<int:id>", methods=['GET'])
@login_required
def user(id):
    return "{}"

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

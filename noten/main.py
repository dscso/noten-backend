import os
import inspect
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from time import time
import models
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
from auth import auth, login_required, parseAuth, admin


@app.route("/")
def index():
    return jsonify({
        "version":"v0.1"
    })

# ----------------------------  LOGIN  ---------------------------------------

@app.route("/login", methods=['POST']) # params: mail and password (generates token)
def login():
    try:
        param = request.get_json()
        mail = param.get('mail')
        password = param.get('password')
        if(mail != None and password != None):
            user = auth(mail, password)
    except:
        return sendError(400, "Bad request")
    if (user != False):
        json = user.json()
        json['token'] = user.getToken()
        json['expiration'] = user.getExpiration()
        print(json)
        return jsonify(json)
    else:
        return sendError(401, "Login Failed")



# TODO: add POST Methode
@app.route("/profile", methods=['GET']) 
@login_required
def profile():
    return jsonify(g.user.json())

import json
@app.route("/teachers/<int:id>/courses")
#@login_required
def getTeacherCourses(id):
    return jsonify([e.serialize() for e in Course.query.filter_by(teacherid=id).all()])
#    return (str(Course.query.filter_by(teacherid=id).all()))

@app.route("/students/<int:id>/courses")
#@login_required
def getStudentCourses(id):
    s = Student.query.filter_by(uid=id).first()
    if(s != None):
        return s.getCourses()
    return sendError(404, "Not Found")

@app.route("/classes/<int:id>/students")
def getClassStudents(id):
    c = Class.query.filter_by(classid=id).first()
    if(c != None):
        return c.getStudents()
    return sendError(404, "Not Found")

# ----------------------- Get user data ------------------------------

@app.route("/users/<int:id>", methods=['GET'])
@login_required
def user(id):
    if (g.user['uid'] != id):
        return sendError(403, "Forbidden")
    user = models.User.query.filter_by(uid=id).first()
    if (user == None):
        return sendError(404, "Bad Request")
    return jsonify(user.json())

@app.route("/ccp")
@admin
def ccp():
    return "skkrrr"

def sendError(code, msg=""):
    return jsonify({"error": code, "msg":msg}), code

def get(json, name):
    try:
        return json[name]
    except:
        return None

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)

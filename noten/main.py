import os
import inspect

from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # cross-origin support
from time import time
import models
import datetime

# initialize 'app' with Flask instance
app = Flask(__name__)
# cross origin
CORS(app)

# secret key to encrypt session - obsolet due to changed authentication
f=open("secret.key", "r")
app.secret_key = f.read()

#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

from models import *
from auth import auth, login_required, parseAuth, admin

# index - actually obsolet, used for version now
@app.route("/")
def index():
    return jsonify({
        "version":"v0.1"
    })

# login
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
        return jsonify(json)
    else:
        return sendError(401, "Login Failed")

# profile
# TODO Post Method?
@app.route("/profile", methods=['GET']) 
@login_required
def profile():
    return jsonify(g.user.json())

# courses
# course-students
@app.route("/courses/<int:id>/students")
@login_required
def getCourseStudents(id):
    c = Course.query.filter_by(cid=id).first()
    if(c != None):
        return c.getStudents()
    return sendError(404, "Not Found")

# teachers
# teacher-courses
@app.route("/teachers/<int:id>/courses")
@login_required
def getTeacherCourses(id):
    t = Teacher.query.filter_by(uid=id).first()
    if(t != None):
        return t.getCourses()
    return sendError(404, "Not Found")

# students
# student-courses
@app.route("/students/<int:id>/courses")
@login_required
def getStudentCourses(id):
    s = Student.query.filter_by(uid=id).first()
    if(s != None):
        return s.getCourses()
    return sendError(404, "Not Found")

# classes
# class-students
@app.route("/classes/<int:id>/students")
def getClassStudents(id):
    c = Class.query.filter_by(classid=id).first()
    if(c != None):
        return c.getStudents()
    return sendError(404, "Not Found")

# users
@app.route("/users/<int:id>", methods=['GET'])
@login_required
def user(id):
    if (g.user['uid'] != id):
        return sendError(403, "Forbidden")
    user = models.User.query.filter_by(uid=id).first()
    if (user == None):
        return sendError(404, "Bad Request")
    return jsonify(user.json())

# admin control panel
@app.route("/acp")
@admin
def ccp():
    return jsonify("\"I can hit every software deadline given enough time.\"")

def sendError(code, msg=""):
    return jsonify({"error": code, "msg":msg}), code

# run the app
if __name__ == '__main__':
    app.run(debug=True, host= '0.0.0.0', port=5000) # host argument runs flask on the local ip so it's visible in the network

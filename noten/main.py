from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # cross-origin support
from time import time
import models, datetime, os, inspect, traceback


app = Flask(__name__) # initializing 'app' with Flask instance
CORS(app) # cross origin support

#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

from models import *
from auth import auth, login_required, parseAuth, admin
import manipulate

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
        mail = param['mail']
        password = param['password']
        user = auth(mail, password)
    except:
        # print(traceback.format_exc()) # Debug Traceback
        return sendError(400, "Bad request")
    if (user != False):
        json = user.json()
        json['token'] = user.getToken()
        json['expiration'] = user.getExpiration()
        return jsonify(json)
    else:
        return sendError(401, "Login Failed")

# PROFILE
# TODO Post Method?
@app.route("/profile", methods=['GET']) 
@login_required
def profile():
    return jsonify(g.user.json())

# COURSES
# course-students
@app.route("/courses/<int:id>/students")
@login_required
def getCourseStudents(id):
    c = Course.query.filter_by(cid=id).first()
    if(c != None):
        return c.getStudents()
    return sendError(404, "Not Found")

@app.route("/courses/<int:id>/marks")
#@login_required
def getCourseMarks(id):
    c = Course.query.filter_by(cid=id).first()
    if(c != None):
        return c.getMarks()
    return sendError(404, "Not Found")

@app.route("/courses/<int:cid>/markmetas", methods=['POST'])
#@login_required
def createMarkMeta(cid):
    try:
        param = request.get_json()
        name = param['name']
        valence = param['valence']
        manipulate.createMarkMeta(name, valence, cid)
        return jsonify({"success":True})
    except:
        #print(traceback.format_exc()) # Debug
        return sendError(400, "Bad Request")


@app.route("/courses/<int:cid>/markmetas/<int:mid>", methods=['PUT', 'DELETE'])
def updateMarkMeta(cid, mid):
    try:
        if(request.method == 'PUT'):
            params = request.get_json()
            name = params['name']
            valence = params['valence']
            meta = models.MarkMeta.query.filter_by(mid=mid, cid=cid).first()
            if(meta != None):
                meta.name = name
                meta.valence = valence
                manipulate.commit()
                return jsonify({"success":True})
            else:
                return sendError(404, "Not Found")
        elif(request.method == 'DELETE'):
            return jsonify({
                "success":True,
                "msg":manipulate.deleteMarkMeta(mid)
                })
    except:
        #print(traceback.format_exc()) # Debug
        return sendError(400, "Bad Request")

# TEACHERS
# teacher-courses
@app.route("/teachers/<int:id>/courses")
@login_required
def getTeacherCourses(id):
    t = Teacher.query.filter_by(uid=id).first()
    if(t != None):
        return t.getCourses()
    return sendError(404, "Not Found")

# STUDENTS
# student-courses
@app.route("/students/<int:id>/courses")
@login_required
def getStudentCourses(id):
    s = Student.query.filter_by(uid=id).first()
    if(s != None):
        return s.getCourses()
    return sendError(404, "Not Found")

@app.route("/students/<int:id>/marks")
#@login_required
def getStudentMarks(id):
    s = Student.query.filter_by(uid=id).first()
    if(s != None):
        return s.getMarks()
    return sendError(404, "Not Found")

@app.route("/courses/<int:courseid>/students/<int:studentid>/marks/<int:markmetaid>",methods=['POST'])
#@login_required
def setMark(courseid, studentid, markmetaid):
    try:
        param = request.get_json()
        mark = param['mark']
        manipulate.updateMark(metaid=markmetaid, studentid=studentid, mark=mark)
        manipulate.commit()
        return jsonify({"success": True})
    except:
        return sendError(400, "Bad Request")

# CLASSES
# class-students
@app.route("/classes/<int:id>/students")
@login_required
def getClassStudents(id):
    c = Class.query.filter_by(classid=id).first()
    if(c != None):
        return c.getStudents()
    return sendError(404, "Not Found")

# USERS
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
def acp():
    return "\"I can hit every software deadline given enough time.\""

# ERRORHANDLING
def sendError(code, msg=""):
    return jsonify({"error": code, "msg":msg}), code

@app.errorhandler(404)
def not_found(e):
    return sendError(404, "Not Found")

# run the app
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # host argument runs flask on the local ip so it's visible in the local network
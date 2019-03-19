from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory, g
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS # cross-origin support
from time import time
import models, datetime, os, inspect, traceback


app = Flask(__name__) # initializing 'app' with Flask instance
CORS(app) # cross origin support

# configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

# importing app-files
from models import *
from auth import auth, courseAllowed, userAllowed, login_required, parseAuth
import manipulate


# general info
@app.route("/")
def index():
    return jsonify({
        "name":"MarkManager",
        "version":"v0.1_alpha",
        "date":"04.01.2019 - 20.03.2019",
        "authors":[ "Jurek", "Florian", "Myrijam", "Christopher", "Youshua", "Felix" ]
    })


# Login
# handels the information provided by the Login-Form in the frontend
@app.route("/login", methods=['POST']) # params: mail and password (generates token)
def login():
    try:
        param = request.get_json()
        mail = param['mail']
        password = param['password']
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


# PROFILE
# TODO Post Method - not necessary due to mission Admin-Control-Panel
# Provides general information about the current sessions user
@app.route("/profile", methods=['GET']) 
@login_required # indicates that the user must be signed in
def profile():
    if(g.user != None):
        return jsonify(g.user.json())
    else:
        return sendError(401, "If you see this, everything is screwed. grab the nearest fire extinguisher and empty it on your device.")


# COURSES
# course-students - returns a list of <Students> in a <Course>
@app.route("/courses/<int:cid>/students")
@login_required
def getCourseStudents(cid):
    if(courseAllowed(cid)):
        c = Course.query.filter_by(cid=cid).first()
        if(c != None):
            return c.getStudents()
        return sendError(404, "Not Found")
    else:
        return sendError(403, "You may not access this URL")


# returns a list of all <Marks> assigned to <Students> in a <Course>
@app.route("/courses/<int:cid>/marks")
@login_required
def getCourseMarks(cid):
    if(courseAllowed(cid)):
        c = Course.query.filter_by(cid=cid).first()
        if(c != None):
            return c.getMarks()
        return sendError(404, "Not Found")
    else:
        return sendError(403, "You may not access this URL")


# creates a <MarkMeta> and assigns it to a <Course>
@app.route("/courses/<int:cid>/markmetas", methods=['POST'])
@login_required
def createMarkMeta(cid):
    if(courseAllowed(cid)):
        try:
            param = request.get_json()
            name = param['name']
            valence = param['valence']
            if(name != "" and valence != ""):
                manipulate.createMarkMeta(name, valence, cid)
                return jsonify({"success":True})
        except:
            return sendError(400, "Bad Request")
    else:
        return sendError(403, "You may not access this URL")


# updates a specific <MarkMeta> in a <Course>
@app.route("/courses/<int:cid>/markmetas/<int:mid>", methods=['POST', 'PUT', 'DELETE'])
@login_required
def updateMarkMeta(cid, mid):
    if(courseAllowed(cid)):
        try:
            if(request.method == 'POST' or request.method == 'PUT'):
                meta = models.MarkMeta.query.filter_by(metaid=metaid, cid=cid).first()
                if(meta != None):
                    meta.name = name
                    meta.valence = valence
                    if(name != "" and valence != ""):
                        manipulate.commit()
                        return jsonify({"success":True})
                else:
                    return sendError(404, "MarkMeta not found")
            elif(request.method == 'DELETE'):
                return jsonify({
                    "success":True,
                    "msg":manipulate.deleteMarkMeta(mid)
                })
        except:
            return sendError(400, "Bad Request")
    else:
        return sendError(403, "You may not access this URL")


# TEACHERS
# return a list of all <Courses> of a <Teacher>
@app.route("/teachers/<int:id>/courses")
@login_required
def getTeacherCourses(id):
    if(userAllowed(id)):
        t = Teacher.query.filter_by(uid=id).first()
        if(t != None):
            return t.getCourses()
        return sendError(404, "Not Found")
    else:
        return sendError(403, "You may not access this URL")

# STUDENTS
# returns a list of all <Courses> of a <Student>
@app.route("/students/<int:id>/courses")
@login_required
def getStudentCourses(id):
    if(userAllowed(id)):
        s = Student.query.filter_by(uid=id).first()
        if(s != None):
            return s.getCourses()
        return sendError(404, "Not Found")
    else:
        return sendError(403, "You may not access this URL")


# returns a list of all <Marks> assigned to a <Student>
@app.route("/students/<int:id>/marks")
@login_required
def getStudentMarks(id):
    if(userAllowed(id)):
        s = Student.query.filter_by(uid=id).first()
        if(s != None):
            return s.getMarks()
        return sendError(404, "Not Found")
    else:
        return sendError(403, "You may not access this URL")


# updates/creates a <Mark> for a specific <Student> in a specific <Course>
@app.route("/courses/<int:courseid>/students/<int:studentid>/marks/<int:markmetaid>",methods=['POST'])
@login_required
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
# returns a list of all <Students> in a class
@app.route("/classes/<int:id>/students")
@login_required
def getClassStudents(id):
    c = Class.query.filter_by(classid=id).first()
    if(c != None):
        return c.getStudents()
    return sendError(404, "Not Found")

# USERS
# returns information about a <User>
@app.route("/users/<int:id>", methods=['GET'])
@login_required
def user(id):
    if (g.user['uid'] != id):
        return sendError(403, "Forbidden")
    user = models.User.query.filter_by(uid=id).first()
    if (user == None):
        return sendError(404, "Bad Request")
    return jsonify(user.json())

# Admin Control Panel (ACP)
@app.route("/acp")
def acp():
    return "\"I can hit every software deadline given enough time.\""

# ERRORHANDLING
def sendError(code, msg=""):
    return jsonify({"error": code, "msg":msg}), code

@app.errorhandler(404)
def not_found(e):
    return sendError(404, "No method linked to requested URL")

# run the app (Debug only)
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) # host argument runs flask on the local ip so it's visible in the local network
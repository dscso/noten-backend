import os
import inspect
# dir_path = os.path.dirname(os.path.realpath(__file__))
# print(dir_path)

from flask import Flask, abort, redirect, render_template, request, url_for, jsonify, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from time import time
import datetime


# import sys
# print(sys.path)

# initialize 'app' with Flask instance
app = Flask(__name__)
app.secret_key = b'x"(ka7:is=7a_+/ayT5'
#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///../database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

from models import *
from auth import *

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

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        # uid = request.args.get("uid")
        # if(uid != None):
        #     token = request.args.get("token")
        #     if(token != None):
        #         return verify_token(uid, token)  
        # else:
        mail = request.form.get("mail")
        pwhash = request.form.get("hash")
        if(mail != None and pwhash != None):
            return auth(mail, pwhash)
        return sendError(400, "bad request", "main.py#login")
    else:
        return render_template('login.html')

# TODO add user exists check!!!
@app.route("/register", methods=["GET","POST"])
def register():
    if(request.method == 'POST'):
        mail = request.args.get("mail")
        pwhash = request.args.get("hash")
        if(mail != None and hash != None):
            u = User(mail=mail, pwhash=pwhash)
            db.session.add(u)
            db.session.commit()
            return url_for("index")
        else:
            return sendError(400, "bad request", "main.py#register")
    else:
        return sendError(405, "post method required", "main.py#register")

def sendError(code, msg="", cause=""):
    print(code)
    return render_template("error.html", code=code, cause=cause, msg=msg)

# run the app
if __name__ == '__main__':
    app.run(debug=True, port=5000)

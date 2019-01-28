from flask import Flask, abort, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from time import time
import datetime
import os 
dir_path = os.path.dirname(os.path.realpath(__file__))


# initialize 'app' with Flask instance
app = Flask(__name__)

#configure sqlalchemy
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:\\nerd\\GitHub\\noten_backend\\database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize 'db' with SQLAlchemy instance
db = SQLAlchemy(app)

# Hello.
print("Mip.")
print(dir_path)

# ROUTING

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        uid = request.args.get("uid")
        if(uid != None):
            token = request.args.get("token")
            if(token != None):
                return token_auth(uid, token)
        else:
            mail = request.form.get("mail")
            pwhash = request.form.get("hash")
            if(mail != None and pwhash != None):
                return auth(mail, pwhash)
        return "argument error"
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
            return "success"
        else:
            return "argument error"
    else:
        return "register form here"

@app.route("/")
def index():
    #TODO load index file
    return "index here"

# run the app
if __name__ == '__main__':
    from models import *
    from auth import *
    app.run(debug=True, port=5000)

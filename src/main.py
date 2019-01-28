from flask import Flask, abort, redirect, render_template, request, url_for
from flask_sqlalchemy import SQLAlchemy
from time import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///D:\\nerd\\GitHub\\noten_backend\\database.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

print("Mip")

@app.route("/login", methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        print(len(request.args))
        mail = request.args.get("mail")
        pwhash = request.args.get("hash")
        if(mail != None and hash != None):
            return auth(mail, pwhash)
        else:
            return "argument error"
    else:
        return "login form here"

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

if __name__ == '__main__':
    from models import *
    from auth import auth
    app.run(debug=True, port=5000)

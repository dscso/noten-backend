from main import db
from models.user import User
from flask import jsonify

def auth(mail, pwhash):
    user = User.query.filter_by(mail=mail).first()
    if(user != None):
        if(user.pwhash == pwhash):
            return jsonify(user.json())
    return "denied"

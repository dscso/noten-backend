from main import db
from models import *
from flask import jsonify

def auth(mail, pwhash):
        user = User.query.filter_by(mail=mail).first()
        if(user != None):
                if(user.pwhash == pwhash):
                        t = Token(uid=user.uid, token="awd")
                        db.session.add(t)
                        db.session.commit()
                        return jsonify(user.json())
        return "denied"

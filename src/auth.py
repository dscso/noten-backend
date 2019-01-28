from main import db
from models import *
from flask import jsonify
import random
import string

def auth(mail, pwhash):
        user = User.query.filter_by(mail=mail).first()
        if(user != None):
                if(user.pwhash == pwhash):
                        oldt = Token.query.filter_by(uid=user.uid).first()
                        if(oldt != None):
                                oldt.token = generate_token()
                        else:
                                db.session.add(Token(uid=user.uid, token=generate_token()))
                        db.session.commit()
                        return jsonify(user.json())
        return "denied"

def generate_token(lenght=16, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(lenght))
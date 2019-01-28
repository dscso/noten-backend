from main import db
from models import User, Token
from flask import jsonify
import random
import string

# matches login credentials with db - return status-string
# TODO response error code with flask.Request
def auth(mail, pwhash):
        user = User.query.filter_by(mail=mail).first()
        if(user != None):
                if(user.pwhash == pwhash):
                        oldt = user.token[0] if len(user.token) == 1 else None
                        if(oldt != None):
                                oldt.token = generate_token()
                                oldt.update_expiration()
                        else:
                                db.session.add(Token(uid=user.uid, token=generate_token()))
                        db.session.commit()
                        return jsonify(user.json())
        return "denied"

# matches login token with db
# TODO responses
# TODO cleanup?
def token_auth(uid, token):
        user = User.query.filter_by(uid=uid).first()
        if(user != None):
                db_token = user.token[0] if len(user.token) == 1 else None
                if(db_token != None):
                        if(db_token.token == token):
                                if(not db_token.is_expired()):
                                        return jsonify(user.json())
        return "denied"

# generates a random auth token
def generate_token(lenght=32, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(lenght))
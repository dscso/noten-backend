from flask import Flask, session, redirect, url_for, escape, request, jsonify, render_template
from functools import wraps
import models
import main
import random
import string
import inspect

db = main.db

# matches login credentials with db - return status-string
# TODO response error code with flask.Request

def auth(mail, password):
    user = models.User.query.filter_by(mail=mail).first()
    if(user != None):
        if(user.password == password):
            token = user.token[0] if len(user.token) == 1 else None
            if(token != None):
                token.token = generate_token()
                token.update_expiration()
            else:
                token = models.Token(uid=user.uid, token=generate_token())
                db.session.add(token)
            db.session.commit()
            return user
    session.clear()
    return False

# generates a random auth token
def generate_token(lenght=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(lenght))

def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        auth = request.headers["Authorization"].split(":")
        if (len(auth) == 2):
            if(verify_token(auth[0], auth[1])):
                return func(*args, **kwargs)
        return main.sendError(401, "Not Authenticated")
    return decorated


def usertype_required(usertype):
    @wraps
    def decorator(f):
        uid = session.get('uid')
        if(uid != None):
            user = models.User.query.filter_by(uid=uid).first()
            db_type = user.usertype if user != None else None
            if(user != None and db_type != None):
                if(db_type == usertype):
                    return f
        # TODO redirect?
        # return redirect(url_for("login"))
        return main.sendError(401, "no perission", "usertype")
    return decorator

def verify_token(uid, token):
    user = models.User.query.filter_by(uid=uid).first()
    if(user != None):
        db_token = user.token[0] if len(user.token) == 1 else None
        if(db_token != None):
            if(db_token.token == token):
                if(not db_token.is_expired()):
                    return True
    return False
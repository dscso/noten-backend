from flask import Flask, session, redirect, url_for, escape, request, jsonify, render_template, g
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
                token.updateExpiration()
            else:
                token = models.Token(uid=user.uid, token=generate_token())
                db.session.add(token)
            db.session.commit()
            return user
    session.clear()
    return False

# generates a random auth token
def generate_token():
    from time import time
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))

# Checks login and returns user object in g.user
def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        g.user = verify_token(parseAuth(request.headers)) # http://flask.pocoo.org/docs/1.0/appcontext/
        if(g.user != None):
            return func(*args, **kwargs)
        return main.sendError(401, "Not Authenticated")
    return decorated

# parses the header and puts info into dict
def parseAuth(headers):
    try:
        auth = request.headers['Authorization'].split(":")
        if (len(auth) == 2):
            return {
                "uid": int(auth[0]),
                "token": auth[1]
            }
    except:
        pass
    return {"uid": None, "token": None}

def admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        uid = session.get('uid')
        if(uid != None):
            user = models.User.query.filter_by(uid=uid).first()
            db_type = user.usertype if user != None else None
            if(user != None and db_type != None):
                if(db_type == 4):
                    return f
        # TODO redirect?
        # return redirect(url_for("login"))
        return main.sendError(401, "no perission")
    return decorator


#*****************************************************************
# --------------------------- Helper functions ------------------


# checks token based on parseHeader dict
def verify_token(auth): # {uid: 123, token: xyz}
    if (auth['uid'] == None):
        return None
    user = models.User.query.filter_by(uid=auth['uid']).first()
    if(user != None):
        db_token = user.token[0] if len(user.token) == 1 else None
        if(db_token != None):
            if(db_token.token == auth['token']):
                if(not db_token.is_expired()):
                    return user
    return None

generate_token()
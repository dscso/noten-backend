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


def auth(mail, pwhash):
    user = models.User.query.filter_by(mail=mail).first()
    if(user != None):
        if(user.pwhash == pwhash):
            token = user.token[0] if len(user.token) == 1 else None
            if(token != None):
                token.token = generate_token()
                token.update_expiration()
            else:
                token = models.Token(uid=user.uid, token=generate_token())
                db.session.add(token)
            updateCookies(user, token)
            db.session.commit()
            return redirect(url_for("index"), 302)
    session.clear()
    return main.sendError(401, "login failed", "auth.py#auth")

# sets session cookies (Token-Auth)
def updateCookies(user, token):
    session['uid'] = user.uid
    session['token'] = token.token
    session['type_id'] = user.usertype
    session['expiration'] = token.expiration

# generates a random auth token
def generate_token(lenght=32, chars=string.ascii_letters + string.digits):
    return ''.join(random.choice(chars) for _ in range(lenght))

def login_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        uid = session.get('uid')
        token = session.get('token')
        if(uid != None and token != None):
            if(verify_token(uid, token)):
                return func(*args, **kwargs)
        # TODO redirect?
        # return redirect(url_for("login"))
        return main.sendError(401, "login requiered", "decorator")
    return decorated_view

def verify_token(uid, token):
    user = models.User.query.filter_by(uid=uid).first()
    if(user != None):
        db_token = user.token[0] if len(user.token) == 1 else None
        if(db_token != None):
            if(db_token.token == token):
                if(not db_token.is_expired()):
                    return True
    return False
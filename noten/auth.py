from flask import Flask, session, redirect, url_for, request, jsonify, g
from functools import wraps # used for decorators
import main, models, random, string, inspect, hashlib

db = main.db

# matches login credentials with db - returns user as json or False
def auth(mail, password):
    user = models.User.query.filter_by(mail=mail).first()
    if(user != None):
        #print(user.password, sha512(password))
        if(user.password == sha512(password)):
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

def sha512(string):
    sha_signature = hashlib.sha512(string.encode()).hexdigest()
    return sha_signature

# generates a random auth token
def generate_token():
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

# decorator to grant access only to admins
def admin(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        try:
            auth = request.headers.get('Authorization').split(" ")
            if (len(auth) == 2):
                t = models.Token.query.filter_by(token=auth[1]).first()
                uid = t.uid if t != None else None
                if(uid != None):
                    user = models.User.query.filter_by(uid=uid).first()
                    db_type = user.usertype if user != None else None
                    if(db_type != None):
                        if(db_type == 4):
                            return f(*args, **kwargs)
        except:
            pass
        return main.sendError(401, "no perission")
    return decorator

# checks token based on parseHeader dict
def verify_token(auth): # {uid: 123, token: xyz}
    if (auth['uid'] == None):
        return None
    user = models.User.query.filter_by(uid=auth['uid']).first()
    if(user != None):
        db_token = user.token[0] if len(user.token) == 1 else None
        if(db_token != None):
            if(db_token.token == auth['token']):
                if(not db_token.isExpired()):
                    return user
    return None

# parses the header and puts info into dict
def parseAuth(headers):
    try:
        if('Authorization' in request.headers):
            auth = request.headers['Authorization'].split(" ")
            if (len(auth) == 2):
                t = models.Token.query.filter_by(token=auth[1]).first()
                if(t != None):
                    uid = t.uid
                    return {
                        "token": auth[1],
                        "uid": uid
                    }
    except:
        pass
    return {"uid": None, "token": None}

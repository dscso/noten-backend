from flask import Flask, session, redirect, url_for, request, jsonify, g
from functools import wraps # used for decorators
import main, models, random, string, inspect, hashlib

db = main.db

# matches login credentials with db - returns user as json or False
def auth(mail, password):
    user = models.User.query.filter_by(mail=mail).first()
    if(user != None):
        #if(user.password == sha512(password)): # NOTE: no time for security, no hashing
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

# unused
def sha512(string):
    sha_signature = hashlib.sha512(string.encode()).hexdigest()
    return sha_signature

# generates a random auth token
def generate_token():
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(128))

# NOTE: Works perfecly fine with any database that does not suck as hard as SQLite.
# Because this Method is querying data, the db gets locked due to SQLites sh*ttyness what leads to errors when
# the function is called multiple times in a short span of time because Querys can't be performed while db is locked.
# SOLUTION: Migrate to MySQL or smth. better (what wouldn't be useful for testing)
#
# checks if a user should have access to a requested <Course> object
def courseAllowed(cid):
    return True
    try:
        utype = g.user.usertype
        if(utype == 2):
            c = models.Course.query.filter_by(cid=cid).first()
            if(c != None):
                return True if c.teacherid == g.user.uid else False
        elif(utype == 1):
            if(g.user.uid in [s.uid for s in models.Course.query.filter_by(cid=cid).first().getStudents()]):
                return True
    except:
        pass
    return False

# Used to verify that the user is permitted to receive the requested userinfo
# No Querying, no stupid problems. Great.
def userAllowed(uid):
    return uid == g.user.uid if g.user != None else False

# Checks login and returns user object in g.user
def login_required(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        g.user = verify_token(parseAuth(request.headers)) # http://flask.pocoo.org/docs/1.0/appcontext/
        if(g.user != None):
            return func(*args, **kwargs)
        return main.sendError(401, "Not Authenticated")
    return decorated

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

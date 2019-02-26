import main
from datetime import datetime
from time import time
db = main.db

# User Model (Database)
class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True)
    name = db.Column(db.String)
    firstname = db.Column(db.String)
    password = db.Column(db.String)
    usertype = db.Column(db.Integer, default=0)
    token = db.relationship("Token", backref=db.backref("users", uselist=False), lazy=True)

    def json(self):
        return {
            "type": self.usertype, 
            "uid": self.uid,
            "firstname": self.firstname,
            "surname": self.name
        }
    def getToken(self):
        return str(self.token[0].token)
    
    def getExpiration(self):  # TODO: modify timestamp?
        return str(self.token[0].expiration.timestamp() * 1000)
    
    def is_teacher(self):
        return self.usertype


# Token Model (Database)
class Token(db.Model):
    __tablename__ = 'tokens'
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    token = db.Column(db.String(32))
    expiration = db.Column(
        db.DateTime, default=datetime.fromtimestamp(time() + 900))
    # obsolet
    # creation = db.Column(db.DateTime, default=datetime.fromtimestamp(time()))

    # returns True if token is expired
    def is_expired(self):
        return self.expiration < datetime.now()

    # 'resets' the creation & expiration date
    def update_expiration(self):
        #self.creation = datetime.fromtimestamp(time())
        self.expiration = datetime.fromtimestamp(time() + 900)

# Subject like math, english, german, PE
class Subject(db.Model):
    __tablename__ = "subjects"
    subid = db.Column(db.Integer, primary_key=True)
    subname = db.Column(db.String)
    short = db.Column(db.String(4))

# course with one teacher and students
class Course(db.Model):
    __tablename__ = "courses"
    cid = db.Column(db.Integer, primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey("classes.classid")) # welche klasse 10a 10b oder 11/12
    subid = db.Column(db.Integer, db.ForeignKey("subjects.subid")) 
    teacherid = db.Column(db.Integer, db.ForeignKey("users.uid"))
    ctype = db.Column(db.Integer) # 0 = sek1 fach; 1 = sek2 gk; 2 = sek2 lk;
    # relations
    teacher = db.relationship("User", backref=db.backref(__tablename__), lazy=True)
    clazz = db.relationship("Class", backref=db.backref(__tablename__), lazy=True)
    subject = db.relationship("Subject", backref=db.backref(__tablename__), lazy=True)
 
# 10a 10b etc
class Class(db.Model):
    __tablename__ = "classes"
    classid = db.Column(db.Integer, primary_key=True)
    grade = db.Column(db.Integer)
    label = db.Column(db.String)
    # wichtig! Gucken ob die Klasse auch wirklich eine SEK I Klasse ist
    #teacher = db.relationship("Teacher", backref=db.backref("class"), lazy=True)

class MarkMeta(db.Model):
    __tablename__ = "meta"
    mid = db.Column(db.Integer, primary_key=True)

class S1Mark(db.Model):
    __tablename__ = "marks_sek_I"
    nid = db.Column(db.Integer, primary_key=True)


class S2Mark(db.Model):
    __tablename__ = "marks_sek_II"
    nid = db.Column(db.Integer, primary_key=True)

db.create_all()
"""import defaults
defaults.load_defaults()"""

import main
from datetime import datetime
from time import time
from flask import jsonify
import json
db = main.db

student_to_course = db.Table('student_to_course', db.Column('uid', db.Integer, db.ForeignKey('students.uid')), db.Column('cid', db.Integer, db.ForeignKey('courses.cid')))

student_to_class = db.Table(
    'student_to_class',
    db.Column('uid', db.Integer, db.ForeignKey('students.uid')),
    db.Column('classid', db.Integer, db.ForeignKey('classes.classid')))


# User Model (Database)
class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True)
    name = db.Column(db.String)
    firstname = db.Column(db.String)
    password = db.Column(db.String)
    usertype = db.Column(db.Integer, default=0)
    token = db.relationship("Token", backref=db.backref("users"), lazy=True)

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

    def isTeacher(self):
        return self.usertype


class Student(User):
    __tablename__ = 'students'
    __mapper_args__ = {'polymorphic_identity': 'students'}
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey("classes.classid"))

    clazz = db.relationship("Class", back_populates=__tablename__)
    courses = db.relationship("Course", secondary=student_to_course, back_populates=__tablename__)

    def serialize(self):
        return {
            "uid": self.uid,
            "surname": self.name,
            "firstname": self.firstname,
            "classid": self.classid,
        }

    def getGrade(self):
        return self.clazz.grade

    def getCourses(self):
        return jsonify([e.serialize() for e in self.courses])
        # return jsonify([e.serialize() for e in student_to_course.query.filter_by(uid=self.uid).all()])


class Teacher(User):
    __tablename__ = "teachers"
    # sqlalchemy-mapper settings
    __mapper_args__ = {'polymorphic_identity': 'teachers'}
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    courses = db.relationship("Course", backref=db.backref(__tablename__))

    def getCourses(self):
        return jsonify([e.serialize() for e in self.courses])


# Token Model (Database)
class Token(db.Model):
    __tablename__ = 'tokens'
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    token = db.Column(db.String(128))
    expiration = db.Column(db.DateTime, default=datetime.fromtimestamp(time() + 900))

    # returns True if token is expired
    def isExpired(self):
        return self.expiration < datetime.now()

    # 'resets' the creation & expiration date
    def updateExpiration(self):
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
    # welche klasse 10a 10b oder 11/12
    classid = db.Column(db.Integer, db.ForeignKey("classes.classid"))
    subid = db.Column(db.Integer, db.ForeignKey("subjects.subid"))
    teacherid = db.Column(db.Integer, db.ForeignKey("teachers.uid"))
    # 1 = SekI-Normal; 2 = SekI-WPU; 3 = SekII-GK; 4 = SekII-LK
    ctype = db.Column(db.Integer)

    # relations
    # ,backref=db.backref(__tablename__), lazy=True
    teacher = db.relationship("Teacher")
    clazz = db.relationship("Class", backref=db.backref(__tablename__), lazy=True)
    subject = db.relationship("Subject", backref=db.backref(__tablename__), lazy=True)
    students = db.relationship("Student", secondary=student_to_course, back_populates=__tablename__, lazy=True)

    def getStudents(self):
        if (self.ctype == 1):
            return self.clazz.getStudents()
        elif (self.ctype >= 2):  # 2:WPU, 3:GK, 4:LK
            return jsonify([e.serialize() for e in self.students])

    def serialize(self):
        return {
            "cid": self.cid,
            "classid": self.classid,
            "subject": self.subject.subname,
            # "subid": self.subject.subid,
            "short": self.subject.short,
            "teacherid": self.teacherid,
            "ctype": self.ctype
        }


class Class(db.Model):
    __tablename__ = "classes"
    classid = db.Column(db.Integer, primary_key=True)
    teacherid = db.Column(db.Integer, db.ForeignKey("teachers.uid"))
    grade = db.Column(db.Integer)  # 7,8...10,11,12
    label = db.Column(db.String)  # A,B,C... oder ''
    # is_grouped = db.Column(db.Boolean) # True für Sek I; False für Sek II (Tutorium)
    # wichtig! Gucken ob die Klasse auch wirklich eine SEK I Klasse ist

    teacher = db.relationship("Teacher", backref=db.backref(__tablename__), lazy=True)
    students = db.relationship("Student", backref=db.backref(__tablename__), lazy=False)

    def getStudents(self):
        return jsonify([e.serialize() for e in self.students])


class MarkMeta(db.Model):
    __tablename__ = "markmeta"
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    valance = db.Column(db.Float)
    cid = db.Column(db.Integer, db.ForeignKey("courses.cid"))


class S1Mark(db.Model):
    __tablename__ = "marks_sek_I"
    nid = db.Column(db.Integer, primary_key=True)
    metaid = db.Column(db.Integer, db.ForeignKey("markmeta.mid"))
    mark = db.Column(db.Integer)

    meta = db.relationship("MarkMeta", backref=db.backref(__tablename__), lazy=True)


class S2Mark(db.Model):
    __tablename__ = "marks_sek_II"
    nid = db.Column(db.Integer, primary_key=True)
    metaid = db.Column(db.Integer, db.ForeignKey("markmeta.mid"))
    points = db.Column(db.Integer)

    meta = db.relationship("MarkMeta", backref=db.backref(__tablename__), lazy=True)

db.create_all()
db.session.commit()

import defaults
defaults.load_defaults()

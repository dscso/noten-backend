import main, random, string, json
from datetime import datetime
from time import time
from flask import jsonify
db = main.db


student_to_course = db.Table('student_to_course', 
    db.Column('uid', db.Integer, db.ForeignKey('students.uid')), 
    db.Column('cid', db.Integer, db.ForeignKey('courses.cid')))

student_to_class = db.Table('student_to_class',
    db.Column('uid', db.Integer, db.ForeignKey('students.uid')),
    db.Column('classid', db.Integer, db.ForeignKey('classes.classid')))


# User-Representation for db
class User(db.Model):
    __mapper_args__ = {
        'polymorphic_identity':'users',
        'concrete': True
    }
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True)
    surname = db.Column(db.String)
    firstname = db.Column(db.String)
    password = db.Column(db.String)
    #salt = db.Column(db.String, default=generateSalt()) # NOTE: no time for security :c
    usertype = db.Column(db.Integer, default=1) # 1=Student;2=Teacher;3=Admin
    token = db.relationship("Token", backref=db.backref("users"), lazy=True)

    def json(self):
        return {
            "type": self.usertype,
            "uid": self.uid,
            "firstname": self.firstname,
            "surname": self.surname
        }

    def getToken(self):
        return str(self.token[0].token)

    def getExpiration(self):
        return str(self.token[0].expiration.timestamp() * 1000)

    def isTeacher(self):
        return self.usertype == 2


# Student-Representation for db
class Student(User):
    __tablename__ = 'students'
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey("classes.classid"))

    clazz = db.relationship("Class", back_populates=__tablename__) # class object
    courses = db.relationship("Course", secondary=student_to_course, back_populates=__tablename__) # list of all courses
    marks = db.relationship("Mark", backref=db.backref(__tablename__)) # list of all marks

    def serialize(self):
        return {
            "uid": self.uid,
            "surname": self.surname,
            "firstname": self.firstname,
            "classid": self.classid,
            "grade":self.getGrade(),
        }

    def getGrade(self):
        return self.clazz.grade

    def getCourses(self):
        return jsonify([e.serialize() for e in self.courses])
        # return jsonify([e.serialize() for e in student_to_course.query.filter_by(uid=self.uid).all()])

    def getMarks(self):
        metas = {e.cid:[m.serialize() for m in e.markmetas] for e in self.courses}
        marks = [e.serialize() for e in self.marks]
        courses = [e.serialize() for e in self.courses]
        return jsonify({"metas":metas, "marks":marks, "courses":courses})


# Teacher-Representation for db
class Teacher(User, db.Model):
    __tablename__ = "teachers"
    uid = db.Column(db.Integer, db.ForeignKey('users.uid'), primary_key=True)

    courses = db.relationship("Course", backref=db.backref(__tablename__)) # list of all courses

    def getCourses(self):
        return jsonify([e.serialize() for e in self.courses])


# Token Model (Database)
class Token(db.Model):
    __tablename__ = 'tokens'
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    token = db.Column(db.String(128))
    expiration = db.Column(db.DateTime, default=datetime.fromtimestamp(time() + 14400)) # valid for 4 hours

    # returns True if token is expired
    def isExpired(self):
        return self.expiration < datetime.now()

    # 'resets' the creation & expiration date
    def updateExpiration(self):
        #self.creation = datetime.fromtimestamp(time())
        self.expiration = datetime.fromtimestamp(time() + 900)


# Subject-Representation for db
class Subject(db.Model):
    __tablename__ = "subjects"
    subid = db.Column(db.Integer, primary_key=True)
    subname = db.Column(db.String) # name
    short = db.Column(db.String(4)) # short form for subname


# Course-Representation for db
# Represents a single <Course> NOT a class
class Course(db.Model):
    __tablename__ = "courses"
    cid = db.Column(db.Integer, primary_key=True)
    classid = db.Column(db.Integer, db.ForeignKey("classes.classid")) # used to assign SEK-I classes to a Course
    subid = db.Column(db.Integer, db.ForeignKey("subjects.subid"))
    teacherid = db.Column(db.Integer, db.ForeignKey("teachers.uid"))
    # 1 = SekI-Normal; 2 = SekI-WPU; 3 = SekII-GK; 4 = SekII-LK
    ctype = db.Column(db.Integer)

    # relations
    teacher = db.relationship("Teacher", back_populates=__tablename__)
    clazz = db.relationship("Class", backref=db.backref(__tablename__), lazy=True)
    subject = db.relationship("Subject", backref=db.backref(__tablename__), lazy=True)
    students = db.relationship("Student", secondary=student_to_course, back_populates=__tablename__, lazy=True)
    markmetas = db.relationship("MarkMeta", backref=db.backref(__tablename__))

    def getStudents(self):
        if(self.ctype > 1):
            return jsonify([e.serialize() for e in self.students])
        else:
            return self.clazz.getStudents()
    
    def getMarks(self):
        students = {}
        for markmeta in self.markmetas:
            for mark in markmeta.getMarks():
                try:
                    students[mark.student.uid].append(mark.serialize())
                except:
                    students[mark.student.uid] = []
                    students[mark.student.uid].append(mark.serialize())
        return jsonify({
            "metas":{e.mid:e.serialize() for e in self.markmetas},
            "students":students
            })

    def serialize(self):
        return {
            "cid": self.cid,
            "classid": self.classid,
            "subject": self.subject.subname, # name of subject
            "short": self.subject.short, # abbreviation for subname
            "teacher":{
                "teacherid": self.teacherid,
                "name":self.teacher.firstname + " " + self.teacher.surname
            },
            "ctype": self.ctype # Kurstyp
        }

# Class-Representation for db
class Class(db.Model):
    __tablename__ = "classes"
    classid = db.Column(db.Integer, primary_key=True)
    teacherid = db.Column(db.Integer, db.ForeignKey("teachers.uid"))
    grade = db.Column(db.Integer)  # 7,8...10,11,12
    label = db.Column(db.String)  # A,B,C... oder ''
    name = db.column_property(str(grade) + label)

    teacher = db.relationship("Teacher", backref=db.backref(__tablename__), lazy=True)
    students = db.relationship("Student", secondary=student_to_class, backref=db.backref(__tablename__), lazy=True)

    def getStudents(self):
        return jsonify([e.serialize() for e in self.students])

# MarkMeta-Representation for db
# discribes a 'global' mark in a <Course>
class MarkMeta(db.Model):
    __tablename__ = "markmeta"
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    valence = db.Column(db.Float)
    cid = db.Column(db.Integer, db.ForeignKey("courses.cid"))
    
    course = db.relationship("Course", backref=db.backref(__tablename__))
    marks = db.relationship("Mark", backref=db.backref(__tablename__))

    def getMarks(self):
        return [mark for mark in self.marks]
        
    def serialize(self):
        return {
            "mid":self.mid,
            "name":self.name,
        }

# Mark-Representation for db
# represents a specific <Mark> asigned to one specific <Student> in a specific <Course>
class Mark(db.Model):
    __tablename__ = "marks"
    __table_args__ = (
        db.UniqueConstraint("metaid", "studentid", name="MetaStudentUnique"), # just one mark per student
    )
    mid = db.Column(db.Integer, primary_key=True)
    metaid = db.Column(db.Integer, db.ForeignKey("markmeta.mid"))
    studentid = db.Column(db.Integer, db.ForeignKey("students.uid"))
    mark = db.Column(db.Integer)

    meta = db.relationship("MarkMeta", back_populates=__tablename__, lazy=True)
    student = db.relationship("Student", back_populates=__tablename__, lazy=True)

    def serialize(self): 
        return {
            "name":self.meta.name,
            "metaid":self.metaid,
            "studentid":self.studentid,
            "mark":self.mark,
            "subject":self.meta.course.subject.subname
        }

db.create_all()
db.session.commit()

import defaults
defaults.load_defaults()

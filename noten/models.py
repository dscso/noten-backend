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

# update: no time for security, no salts, we eat too much salt anyway.
def generateSalt():
    # may use secure random instead.
    # when db is created and filled we get the same salts for all the users.
    return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(16))

# User Model (Database)
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
    #salt = db.Column(db.String, default=generateSalt())
    usertype = db.Column(db.Integer, default=0)
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
        marks = {}
        return marks

class Teacher(User, db.Model):
    __tablename__ = "teachers"
    # sqlalchemy-mapper settings
    # __mapper_args__ = {'polymorphic_identity': 'teachers'}
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
    teacher = db.relationship("Teacher", back_populates=__tablename__)
    clazz = db.relationship("Class", backref=db.backref(__tablename__), lazy=True)
    subject = db.relationship("Subject", backref=db.backref(__tablename__), lazy=True)
    students = db.relationship("Student", secondary=student_to_course, back_populates=__tablename__, lazy=True)
    markmetas = db.relationship("MarkMeta", backref=db.backref(__tablename__))

    def getStudents(self):
        return jsonify([e.serialize() for e in self.students])
    
    def getMarks(self):
        students = {}
        for markmeta in self.markmetas:
            for mark in markmeta.getMarks():
                try:
                    students[mark.student.uid].append(mark.serialize())
                except KeyError:
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
    name = db.column_property(str(grade) + label)
    # is_grouped = db.Column(db.Boolean) # True für Sek I; False für Sek II (Tutorium)
    # wichtig! Gucken ob die Klasse auch wirklich eine SEK I Klasse ist

    teacher = db.relationship("Teacher", backref=db.backref(__tablename__), lazy=True)
    students = db.relationship("Student", backref=db.backref(__tablename__), lazy=False)

    def getStudents(self):
        return jsonify([e.serialize() for e in self.students])

######## OLD - remove?
    def getSek(self):
        return 1 if self.grade < 11 else 2

class MarkMeta(db.Model):
    __tablename__ = "markmeta"
    mid = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    valance = db.Column(db.Float)
    cid = db.Column(db.Integer, db.ForeignKey("courses.cid"))
    
    course = db.relationship("Course", backref=db.backref(__tablename__))
    #This solution is questionable.
    marks = db.relationship("Mark", backref=db.backref(__tablename__))

    def getMarks(self):
        return [mark for mark in self.marks]
        
    def serialize(self):
        return {
            "mid":self.mid,
            "name":self.name,
        }

class Mark(db.Model):
    __tablename__ = "marks"
    nid = db.Column(db.Integer, primary_key=True)
    metaid = db.Column(db.Integer, db.ForeignKey("markmeta.mid"))
    studentid = db.Column(db.Integer, db.ForeignKey("students.uid"))
    mark = db.Column(db.Integer)

    meta = db.relationship("MarkMeta", back_populates=__tablename__, lazy=True)
    student = db.relationship("Student", backref=db.backref(__tablename__), lazy=True)

    def serialize(self): 
        return {
            "nid":self.nid,
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

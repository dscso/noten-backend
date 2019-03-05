from main import db
from models import student_to_course, Subject, Class, Course, User, Student, Teacher

def addStudentToCourse(uid, cid):
    s = Student.query.filter_by(uid=uid).first()
    s.courses.append(Course.query.filter_by(cid=cid).first())

def update_sub(subid, subname, short):
    sub = Subject.query.filter_by(subid=subid).first()
    if(sub != None):
        sub.subname = subname
        sub.short = short
    else:
        db.session.add(Subject(subid=subid, subname=subname, short=short))

def update_student(uid, mail, password, name, firstname, classid):
    s = Student.query.filter_by(uid=uid).first()
    if(s != None):
        s.mail = mail
        s.name = name
        s.firstname = firstname
        s.password = password
        s.usertype = 1
        s.classid = classid
    else:
        db.session.add(Student(uid=uid, name=name,firstname=firstname, password=password, usertype=1))

def update_teacher(uid, mail, password, name, firstname):
    t = Teacher.query.filter_by(uid=uid).first()
    if(t != None):
        t.mail = mail
        t.name = name
        t.firstname = firstname
        t.password = password
        t.usertype = 3
    else:
        db.session.add(Teacher(uid=uid, name=name, firstname=firstname, password=password, usertype=3))


def update_class(classid, teacherid, grade, label):
    clazz = Class.query.filter_by(classid=classid).first()
    if(clazz != None):
        clazz.teacherid = teacherid
        clazz.grade = grade
        clazz.label = label
        clazz.is_grouped = getGroupState(grade)
    else:
        db.session.add(Class(classid=classid, teacherid=teacherid, grade=grade, label=label))

def getGroupState(grade):
    if(grade < 11):
        return True
    return False

def update_course(cid, classid, subjectid, teacherid, ctype):
    course = Course.query.filter_by(cid=cid).first()
    if(course != None):
        course.classid = classid
        course.subid = subjectid
        course.teacherid = teacherid
        course.ctype = ctype
    else:
        db.session.add(Course(cid=cid, classid=classid, subid=subjectid, ctype=ctype))

def load_defaults():

    # Subjects
    update_sub(subid=1, subname="Biologie", short="bio")
    update_sub(subid=2, subname="Bio Zusatz", short="bioz")
    update_sub(subid=3, subname="Chemie", short="ch")
    update_sub(subid=4, subname="Informatik", short="in")
    update_sub(subid=5, subname="Mathematik", short="ma")
    update_sub(subid=6, subname="Mathe Zusatz", short="maz")
    update_sub(subid=7, subname="Physik", short="ph")

    update_sub(subid=8, subname="Deutsch", short="de")
    update_sub(subid=9, subname="Englisch", short="en")
    update_sub(subid=10, subname="Französisch", short="fr")
    update_sub(subid=11, subname="Latein", short="la")
    update_sub(subid=12, subname="Primun", short="enz")
    update_sub(subid=13, subname="Spanisch", short="sn")

    update_sub(subid=14, subname="Ethik", short="eth")
    update_sub(subid=15, subname="Geografie", short="geo")
    update_sub(subid=16, subname="Geschichte", short="ge")
    update_sub(subid=17, subname="Gesellschaftswissenschaften", short="gewi")
    update_sub(subid=18, subname="Philosophie", short="phil")
    update_sub(subid=19, subname="Politikwissenschaften", short="pw")
    update_sub(subid=20, subname="Religion", short="rel")
    update_sub(subid=21, subname="Sozialwissenschaften", short="sowi")

    update_sub(subid=22, subname="Darstellendes Spiel", short="ds")
    update_sub(subid=23, subname="Musik", short="mu")
    update_sub(subid=24, subname="Musik Zusatz", short="muz")
    update_sub(subid=25, subname="Kunst", short="ku")

    update_sub(subid=26, subname="Beruf und Studium", short="bs")

    update_class(classid=1, teacherid=1, grade=7, label="D")
    update_class(classid=2, teacherid=1, grade=10, label="A")
    update_class(classid=3, teacherid=2, grade=11, label="")
    update_class(classid=4, teacherid=2, grade=12, label="")

    update_course(cid=1, classid=4, subjectid=8, teacherid=2, ctype=3)
    update_course(cid=2, classid=4, subjectid=5, teacherid=1, ctype=3)
    update_course(cid=3, classid=4, subjectid=1, teacherid=2, ctype=3)

    update_teacher(1, "jurgen@plg", "kek", "Schulz", "Jürgen")
    update_teacher(2, "rainer@plg", "sip", "Wahnsinn", "Rainer")

    update_student(3, "hugh@plg", "meme", "Mungus", "Hugh", 4)
    update_student(4, "big@plg", "meme", "Chungus", "Big", 4)

    addStudentToCourse(3, 1)
    addStudentToCourse(3, 2)

    addStudentToCourse(4, 1)
    addStudentToCourse(4, 3)

    db.session.commit()
from main import db
from models import Subject, Class, Course

def update_sub(subid, subname, short):
    sub = Subject.query.filter_by(subid=subid).first()
    if(sub != None):
        sub.subname = subname
        sub.short = short
    else:
        db.session.add(Subject(subid=subid, subname=subname, short=short))

def update_class(classid, grade, label):
    clazz = Class.query.filter_by(classid=classid).first()
    if(clazz != None):
        clazz.grade = grade
        clazz.label = label
    else:
        db.session.add(Class(classid=classid, grade=grade, label=label))

def update_course(cid, classid, subjectid, ctype):
    course = Course.query.filter_by(cid=cid).first()
    if(course != None):
        course.classid = classid
        course.subjectid = subjectid
        course.ctype = ctype
    else:
        db.session.add(Course(cid=cid, classid=classid, subjectid=subjectid, ctype=ctype))

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
    update_sub(subid=17, subname="Philosophie", short="phil")
    update_sub(subid=18, subname="Politikwissenschaften", short="pw")
    update_sub(subid=19, subname="Religion", short="rel")
    update_sub(subid=20, subname="Sozialwissenschaften", short="sowi")

    update_sub(subid=21, subname="Darstellendes Spiel", short="ds")
    update_sub(subid=22, subname="Musik", short="mu")
    update_sub(subid=23, subname="Musik Zusatz", short="muz")
    update_sub(subid=24, subname="Kunst", short="ku")

    update_sub(subid=25, subname="Beruf und Studium", short="bs")

    update_class(classid=1, grade=7, label="D")
    update_class(classid=2, grade=10, label="A")
    update_class(classid=3, grade=11, label="")
    update_class(classid=4, grade=12, label="")

    update_course(1, 4, 4, 2)
    update_course(2, 1, 24, 0)
    update_course(3, 2, 22, 0)

    db.session.commit()
from main import db, models


# The functions in this File are used to modify the database.
# The names of the functions are speaking for themselves

def addStudentToCourse(uid, cid):
    s = models.Student.query.filter_by(uid=uid).first()
    s.courses.append(models.Course.query.filter_by(cid=cid).first())

def update_sub(subid, subname, short):
    sub = models.Subject.query.filter_by(subid=subid).first()
    if(sub != None):
        sub.subname = subname
        sub.short = short
    else:
        db.session.add(models.Subject(subid=subid, subname=subname, short=short))

def update_student(uid, mail, password, surname, firstname, classid):
    s = models.Student.query.filter_by(uid=uid).first()
    if(s != None):
        s.mail = mail
        s.surname = surname
        s.firstname = firstname
        s.password = password
        s.usertype = 1
        s.classid = classid
    else:
        db.session.add(models.Student(uid=uid, surname=surname,firstname=firstname, password=password, usertype=1))

def update_teacher(uid, mail, password, surname, firstname):
    t = models.Teacher.query.filter_by(uid=uid).first()
    if(t != None):
        t.mail = mail
        t.surname = surname
        t.firstname = firstname
        t.password = password
        t.usertype = 2
    else:
        db.session.add(models.Teacher(uid=uid, surname=surname, firstname=firstname, password=password, usertype=2))


def update_class(classid, teacherid, grade, label):
    clazz = models.Class.query.filter_by(classid=classid).first()
    if(clazz != None):
        clazz.teacherid = teacherid
        clazz.grade = grade
        clazz.label = label
        clazz.is_grouped = getGroupState(grade)
    else:
        db.session.add(models.Class(classid=classid, teacherid=teacherid, grade=grade, label=label))

def getGroupState(grade):
    if(grade < 11):
        return True
    return False

def update_course(cid, classid, subjectid, teacherid, ctype):
    course = models.Course.query.filter_by(cid=cid).first()
    if(course != None):
        course.classid = classid
        course.subid = subjectid
        course.teacherid = teacherid
        course.ctype = ctype
    else:
        db.session.add(models.Course(cid=cid, classid=classid, subid=subjectid, ctype=ctype))

def updateMarkMeta(mid, name, valence, cid):
    markMeta = models.MarkMeta.query.filter_by(mid=mid).first()
    if(markMeta != None):
        markMeta.name = name
        markMeta.valence = valence
        markMeta.cid = cid
    else:
        db.session.add(models.MarkMeta(mid=mid, name=name, valence=valence, cid=cid))

def updateMark(metaid, studentid, mark):
    m = models.Mark.query.filter_by(metaid=metaid, studentid=studentid).first()
    if(m != None):
        m.mark = mark
    else:
        db.session.add(models.Mark(metaid=metaid, studentid=studentid, mark=mark))

def createMarkMeta(name, valence, cid):
    db.session.add(models.MarkMeta(name=name, valence=valence, cid=cid))
    commit()

def deleteMarkMeta(mid):
    meta = models.MarkMeta.query.filter_by(mid=mid).first()
    if(meta != None):
        db.session.delete(meta)
        commit()
        return "Deleted successfully"
    else:
        return "Not Found"


# used to write cached changes to db
def commit():
    db.session.commit()
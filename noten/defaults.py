from manipulate import *


# this file provides a default Dataset

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

    update_course(cid=1, classid=3, subjectid=8, teacherid=1, ctype=3) # 11
    update_course(cid=2, classid=3, subjectid=5, teacherid=2, ctype=3) # 11
    update_course(cid=3, classid=3, subjectid=4, teacherid=4, ctype=3) # 11
    update_course(cid=4, classid=3, subjectid=3, teacherid=2, ctype=3) # 11
    update_course(cid=5, classid=4, subjectid=14, teacherid=3, ctype=3) # 12
    update_course(cid=6, classid=4, subjectid=25, teacherid=4, ctype=3) # 12
    update_course(cid=7, classid=4, subjectid=9, teacherid=3, ctype=3) # 12

    update_teacher(uid=1, mail="jurgen@plg", password="password", surname="Schulz", firstname="Jurgen")
    update_teacher(uid=2, mail="rainer@plg", password="schule", surname="Wahnsinn", firstname="Rainer")
    update_teacher(uid=3, mail="simon@plg", password="simon", surname="Suppe", firstname="Simon")
    update_teacher(uid=4, mail="peter@plg", password="schule", surname="Posaune", firstname="Peter")

    update_student(uid=5, mail="hugh@plg", password="login", surname="Mungus", firstname="Hugh", classid=3) # Klasse 11
    update_student(uid=6, mail="big@plg", password="test", surname="Chungus", firstname="Big", classid=3) # Klasse 11
    update_student(uid=7, mail="bob@plg", password="seees", surname="Marley", firstname="Bob", classid=4) # Klasse 12
    update_student(uid=8, mail="heinrich@plg", password="saaas", surname="Helm", firstname="Heinrich", classid=4) # Klasse 12

    addStudentToCourse(5, 1) # studentid, courseid
    addStudentToCourse(5, 2)
    addStudentToCourse(5, 3)

    addStudentToCourse(6, 1)
    addStudentToCourse(6, 3)
    addStudentToCourse(6, 4)

    addStudentToCourse(7, 5)
    addStudentToCourse(7, 6)
    addStudentToCourse(7, 7)

    addStudentToCourse(8, 5)
    addStudentToCourse(8, 7)

    updateMarkMeta(mid=1, name="LEK 1", valence=30, cid=1)
    updateMarkMeta(mid=2, name="Test 1", valence=20, cid=1)

    updateMarkMeta(mid=3, name="Test 1", valence=10, cid=2)
    updateMarkMeta(mid=4, name="Test 2", valence=10, cid=2)
    updateMarkMeta(mid=5, name="Kl 1", valence=10, cid=2)

    updateMarkMeta(mid=6, name="P1", valence=10, cid=3) # Protokoll 1
    updateMarkMeta(mid=7, name="V1", valence=30, cid=3) # Vortrag 1

    updateMarkMeta(mid=8, name="Test 1", valence=10, cid=4)
    updateMarkMeta(mid=9, name="LEK 1", valence=10, cid=4)

    updateMarkMeta(mid=10, name="Test 1", valence=10, cid=5)
    updateMarkMeta(mid=11, name="V1", valence=10, cid=5)
    updateMarkMeta(mid=12, name="Test 2", valence=10, cid=5)

    updateMarkMeta(mid=13, name="Test 1", valence=10, cid=6)
    updateMarkMeta(mid=14, name="Test 2", valence=10, cid=6)

    updateMarkMeta(mid=15, name="Test 1", valence=10, cid=7)
    updateMarkMeta(mid=16, name="Test 2", valence=10, cid=7)
    updateMarkMeta(mid=17, name="KL 1", valence=10, cid=7)
    
    updateMark(metaid=1, studentid=5, mark=11)
    updateMark(metaid=1, studentid=6, mark=11)
    updateMark(metaid=2, studentid=5, mark=10)
    updateMark(metaid=2, studentid=6, mark=15)
    updateMark(metaid=3, studentid=7, mark=9)
    updateMark(metaid=3, studentid=7, mark=13)
    updateMark(metaid=6, studentid=8, mark=10)
    updateMark(metaid=7, studentid=8, mark=10)
    updateMark(metaid=4, studentid=6, mark=9)
    
    
    db.session.commit()
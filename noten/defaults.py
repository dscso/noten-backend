from manipulate import *


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

    update_teacher(1, "jurgen@plg", "6a1a778143e4672886991729035807cabeb75ad42a3fe4bf580cfbdf5cea7c476705d878af5f0fd0dc07d19f2959e224b21788e561f046177f6752b4bcc59e2c", "Schulz", "Jürgen")
    update_teacher(2, "rainer@plg", "59a4515adec34b99e2d8a45364deadb378f01ff2ef5728b9a2c42cdac36f1af46f6d6e79a64648f64292a6be9b693b34e4b6b6b58eab649ddf402d6fc9a602a7", "Wahnsinn", "Rainer")

    update_student(3, "hugh@plg", "a8d5562e2c8f95053bb410a1fe18f88859b7df4c82ca41b25c0bcb9508004181c243f0756ea860d6d957e397f2bedfcbddd396cb6c7c2a2b5b9c59cae02c80ce", "Mungus", "Hugh", 4)
    update_student(4, "big@plg", "a8d5562e2c8f95053bb410a1fe18f88859b7df4c82ca41b25c0bcb9508004181c243f0756ea860d6d957e397f2bedfcbddd396cb6c7c2a2b5b9c59cae02c80ce", "Chungus", "Big", 4)

    addStudentToCourse(3, 1) # studentid, courseid
    addStudentToCourse(3, 2)

    addStudentToCourse(4, 1)
    addStudentToCourse(4, 2)

    updateMarkMeta(mid=1, name="Test 1", valence=10, cid=2)
    updateMarkMeta(mid=2, name="Test 2", valence=10, cid=2)
    updateMarkMeta(mid=3, name="LEK 1", valence=30, cid=1)
    updateMarkMeta(mid=4, name="Test 1", valence=20, cid=1)
    updateMarkMeta(mid=3, name="Protokoll", valence=10, cid=3)
    updateMarkMeta(mid=3, name="Präs 1", valence=30, cid=3)
    
    updateMark(metaid=1, studentid=3, mark=11)
    updateMark(metaid=2, studentid=4, mark=10)
    updateMark(metaid=1, studentid=4, mark=15)
    updateMark(metaid=2, studentid=3, mark=9)
    updateMark(metaid=3, studentid=3, mark=13)
    updateMark(metaid=3, studentid=4, mark=10)
    updateMark(metaid=4, studentid=3, mark=10)
    updateMark(metaid=4, studentid=4, mark=9)
    
    
    db.session.commit()
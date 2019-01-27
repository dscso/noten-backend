import main
db = main.db

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True)
    pwhash = db.Column(db.String, unique=True)

    def json(self):
        return {"uid":self.uid, "mail":self.mail}
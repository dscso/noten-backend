from sqlalchemy.orm import relationship
import main
db = main.db

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True)
    pwhash = db.Column(db.String, unique=True)
    token = db.relationship("Token", backref=db.backref("user", uselist=False), lazy=True)
    #token = relationship("Child", uselist=False, back_populates="parent")

    def json(self):
        return {"uid":self.uid, "mail":self.mail}

class Token(db.Model):
    __tablename__ = 'tokens'
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    token = db.Column(db.String)

db.create_all()
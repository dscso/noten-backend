import main
from datetime import datetime
from time import time
db = main.db


# User Model (Database)
class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.Integer, primary_key=True)
    mail = db.Column(db.String(120), unique=True)
    pwhash = db.Column(db.String, unique=True)
    is_teacher = db.Column(db.Boolean, default=False)
    token = db.relationship("Token", backref=db.backref("user", uselist=False), lazy=True)
    #token = relationship("Child", uselist=False, back_populates="parent")

    def json(self):
        token = self.token[0]
        # TODO: modify timestamp?
        return { "uid": self.uid, "token": str(token.token), "expiration": str(token.expiration.timestamp() * 1000) }

    def is_teacher():
        return self.is_teacher


# Token Model (Database)
class Token(db.Model):
    __tablename__ = 'tokens'
    uid = db.Column(db.Integer, db.ForeignKey("users.uid"), primary_key=True)
    token = db.Column(db.String(32))
    expiration = db.Column(db.DateTime, default=datetime.fromtimestamp(time() + 900))
    creation = db.Column(db.DateTime, default=datetime.fromtimestamp(time()))

    # returns True if token is expired
    def is_expired(self):
        return self.expiration < datetime.now()

    # 'resets' the creation & expiration date
    def update_expiration(self):
        self.creation = datetime.fromtimestamp(time())
        self.expiration = datetime.fromtimestamp(time() + 900)


db.create_all()

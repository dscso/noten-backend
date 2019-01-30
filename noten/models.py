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
    usertype = db.Column(db.Integer, default=0)
    token = db.relationship("Token", backref=db.backref("user", uselist=False), lazy=True)
    #token = relationship("Child", uselist=False, back_populates="parent")

    def json(self):
        token = self.token[0]
        # TODO: modify timestamp?
        return { "expiration": str(token.expiration.timestamp() * 1000), "token": str(token.token), "type":self.usertype, "uid": self.uid }

    def is_teacher(self):
        return self.usertype


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

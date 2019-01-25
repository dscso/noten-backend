from flask import Flask, request, abort, jsonify
import sqlite3

class User():
    def __init__(self, mail, hash):
        self.sql = sqlite3.connect("test.db", isolation_level=None).cursor()
        self.uid = None
        self.mail = mail
        self.hash = hash

    def login(self):
        if(self.checkHash()):
            self.uid = self.fetchUid()
            if(self.uid != None):
                return self.isPermitted()
            else:
                return self.makeResponse(1, "unknown user")
        else:
            # Replace this with normal exception! - just debug
            return self.makeResponse(1, "invalid hash")

    def checkHash(self):
        # TODO check if valid hash is supplied
        return True

    def fetchUid(self):
        self.sql.execute("SELECT uid FROM users WHERE mail='" + self.mail + "';")
        r = self.sql.fetchone()
        if(r != None):
            return r[0]
        return None
        
    def isPermitted(self):
        self.sql.execute("SELECT hash FROM users WHERE uid='" + str(self.uid) + "';")
        r = self.sql.fetchone()
        if(r != None):
            if(str(r[0]) == self.hash):
                return self.makeResponse(0)
            else:
                return self.makeResponse(1, "invalid password")
        return False

    def makeResponse(self, status, msg=None):
        if(status == 0):
            return jsonify({ "status": status, "cid": self.uid, "mail": self.mail })
        else:
            return jsonify({ "status": status, "message": str(msg)})

#u=User("felix@3xploit.net", "hi")

app = Flask(__name__)
#c = sql.cursor()
#c.execute("CREATE TABLE IF NOT EXISTS users(uid INTEGER PRIMARY KEY, mail TEXT, hash TEXT, salt VARCHAR(12));")
#c.execute("INSERT INTO users(uid, mail, hash) VALUES(NULL, \"{mail}\", \"{hash}\");".format(mail="felix@3xploit.net", hash="hio"))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if(request.method == 'POST'):
        mail = request.args.get("mail")
        hash = request.args.get("hash")
        if(mail != None and hash != None):
            u = User(mail, hash)
            return u.login()
        print(mail, hash)
        return "POST"
    else:
        return "Get"

if __name__ == '__main__':
    app.run(debug=True, port=5000)
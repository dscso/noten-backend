import sqlite3

# Opening Database
conn = sqlite3.connect('database.db')
c = conn.cursor()

class User():
    def __init__(self, UID = None):
        self.mail = None
        self.uid = None
        self.password = None
        if (UID != None):
            c.execute('SELECT * FROM User WHERE UID=?', str(UID))
            response = c.fetchone()
            if (response != None):
                self.mail = response[1]
                self.password = response[2]
                self.uid = UID
            else:
                raise Exception("Not found")
    def getUUID(self): # returns the UUID
        pass
    def getType(self): # if is teacher or not
        pass
    def passwordValidation(self, password): # validates password
        if (self.password == password):
            return True
        else:
            return False

print User(UID = 2).passwordValidation("124")
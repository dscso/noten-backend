import sqlite3

# Opening Database
conn = sqlite3.connect('database.db')
c = conn.cursor()

class User():
    def __init__(self, UID = None, mail = None):
        self.mail = None
        self.uid = None
        self.password = None
        self.__response = None
        # SQL for UID
        if (UID != None):
            c.execute('SELECT * FROM User WHERE UID=?', str(UID))
            self.__response = c.fetchone()
        # SQL for mail
        elif (mail != None):
            c.execute('SELECT * FROM User WHERE mail=?', mail)
            self.__response = c.fetchone()
        # if response worked
        if (self.__response != None):
            self.mail = response[1]
            self.password = response[2]
            self.uid = response[0]
        else:
            raise Exception("Not found")
    def getUUID(self): # returns the UUID
        pass # ------------------------------------------- TODO
    def getType(self): # if is teacher or not
        pass # ------------------------------------------- TODO
    def passwordValidation(self, password): # validates password
        if (self.password == password):
            return True
        else:
            return False

print User(UID = 2).passwordValidation("124")
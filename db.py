import sqlite3
from user import User

# Opening Database
conn = sqlite3.connect('example.db')
c = conn.cursor()

class User():
    def __init__(self, UUID = None, mail = None):
        self.conn = conn
        self.c = c
        self.username = None
        self.uuid = None
    def getUUID(self): # returns the UUID
        pass
    def getType(self): # if is teacher or not
        pass
    def passwordValidation(self, password) # validates password
        pass


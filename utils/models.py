import sqlite3


class User:

    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password = password 
    
    def __str__(self):
        return 'User(id=%s)' % self.id
    
    @classmethod
    def find_username(cls, username):
        connnection = sqlite3.connect('data.db')
        cursor = connnection.cursor()
        
        select_query = 'select * from users where username=?'
        cursor.execute(select_query, (username,))
        row = cursor.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        return user
    
    @classmethod
    def find_id(cls, _id):
        connnection = sqlite3.connect('data.db')
        cursor = connnection.cursor()
        
        select_query = 'select * from users where id=?'
        cursor.execute(select_query, (_id,))
        row = cursor.fetchone()

        if row:
            user = cls(*row)
        else:
            user = None
        
        return user


class User:
    def __init__(self, name, email, password, username):
        self.name   =   name
        self.email  =   email
        self.password   = password
        self.username   = username


    def toDBCollection(self):
        return {
            'name':self.name,
            'email': self.email,
            'password': self.password,
            'username': self.username 
        }    
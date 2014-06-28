from app.core.models import Users, UserDetails


class DatabaseModel():
    def __init__(self):
        pass

    def getInsertID(self):
        pass

    def createUser(self):
        pass

    def appendUserDetails(self):
        pass

    def validateUser(self):
        pass

    def getUserByUsername(self):
        pass

    def getAllUsers(self):
        return Users.query.all()


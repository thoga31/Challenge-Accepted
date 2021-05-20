from dbhelper.dbcontrol import *
from utils.read         import Read
from tui.cli            import crt


class User(object):
    NO_USER = -1

    def __init__(self, dbcontroller : DBControl):
        self._username  = ""
        self._password  = ""
        self._dbcontrol = dbcontroller
        self._logged    = False
        self._userid    = User.NO_USER


    def wipe(self):
        self._username = ""
        self._password = ""


    def getUsername(self):
        return self._username


    def getUserID(self):
        return self._userid


    def isLoggedIn(self):
        return self._logged


    def logout(self):
        self.wipe()
        self._logged = False
        self._userid = User.NO_USER


    def login(self):
        self._username = Read.asString("Username: ")
        self._password = Read.asPassword("Password: ")
        try:
            (ok, id_user) = self._dbcontrol.loginUser(self._username, self._password)
            if ok:
                self._logged = True
                self._userid = id_user
        except (UsernameNotFound, WrongPassword) as ex:
            crt.writeWarning(ex.message)
            self._logged = False
            self.wipe()
        return self._logged


    def signup(self):
        while True:
            email = Read.asString("Email: ")
            # TODO: validar Email
            if self._dbcontrol.emailExists(email):
                crt.writeWarning(f"User with email '{email}' already exists.")
            else:
                break
        while True:
            username = Read.asString("New username: ")
            # TODO: validar Username
            if self._dbcontrol.userExists(username):
                crt.writeWarning(f"User '{username}' already exists.")
            else:
                break
        while True:
            password = Read.asPassword("Password: ")
            password_check = Read.asPassword("Repeat password: ")
            if password != password_check:
                crt.writeWarning("Passwords do not coincide.")
            else:
                break
        return self._dbcontrol.registerUser(username, password, email)

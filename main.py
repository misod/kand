# main file to run
import connection

login_file = "./login.txt"

class Login(object):
    username = ""
    password = ""
    longitude = 0
    latitude = 0
    radius = 0

    """def __init__(self, username, password, longitude, latitude, radius):
        self.username = username
        self.password = password
        self.longitude = longitude
        self.latitude = latitude
        self.radius = radius
        """
    #def __init__(self):

# ----- main code ------

login = Login()

if connection.readLogin(login_file, login):

    print("able to read login info")

else:
    print("error: 3 - problem getting login info")

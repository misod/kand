# connection to the server and reciving stuff
import os.path


def connect(adress, username, password, longitude, latitude, radius):

    return ""

def writeLogin(filename, username, password, longitude, latitude, radius):

    return ""

def readLogin(filename, login_object):

    val_return = 0

    if os.path.isfile(filename) and os.access(filename, os.R_OK):
        #print ("file exists and is readable")
        with open(filename, 'r') as f:
           try:
               login_string = f.read()
               log_split = login_string.split(',')
               login_object.username = log_split[0]
               login_object.password = log_split[1]
               login_object.longitude = log_split[2]
               login_object.latitude = log_split[3]
               login_object.radius = log_split[4]
               val_return = 1
           except IOExeption: # whatever reader errors you care about
                print("problem reading user info \n\n solve this later on")
               # handle error
           finally:
               f.close()
               return val_return
    else:
        print("file doesn't exist")

    return val_return

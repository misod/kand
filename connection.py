# connection to the server and reciving stuff
import os.path
import socket

prog_name = "Kand"
prog_version = "0.0.2"

def connect(server, port, login_object):
    #create socket and connect
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((server, port))
    except Exception as e:
        print "error error error....."
        return -1


    USER = login_object.username              # Set to your username for sending data
    PASSCODE = login_object.password               # Passcode = -1 is readonly, set to your passcode for useranme to send data
    FILTER_DETAILS = "filter filter r/"+ login_object.longitude +"/"+ login_object.latitude +"/"+ login_object.radius +"\n "
    login = 'user %s pass %s vers %s %s %s'  % (USER, PASSCODE, prog_name, prog_version, FILTER_DETAILS)
    #login = 'user %s pass %s vers Python_Example 0.0.1'  % (USER, PASSCODE)
    try:
        sock.send(login)
    except Exception as e:
        print("it went crazy when trying to connect")
        return -1

    return sock

def create_socket_file(socket):
    try:
        sock_file = socket.makefile()
    except Exception as e:
        print "attans............"
        return -1

    return sock_file

def keepalive(connection_file):
    try:
        connection_file.write("keepalive")
        connection_file.flush()
        # here we send a log message of when the keepalive was sent so we can trace what happens
    except Exception, e:
        #for now we just print, but in the long run we log to file
        print "this didn't go as planed %s" % (e)
        return 0

    return 1

def write_login(filename, login_object):

    return ""

def read_login(filename, login_object):

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

def close(sock):

    # close socket -- must be closed to avoid buffer overflow
    try:
        sock.shutdown(0)
        sock.close()
        print "socket closed"
    except Exception as e:
        print "ojojojojojojojojoj"
        return -1


    return 1

def get_message(connection_file):
    try:
        # Read packet string from socket
        packet_str = connection_file.readline()
        print "packet string length is: ", len(packet_str), " packet is: ", packet_str
    except socket.error:
        print "Socket error on readline"
        return ""

    return packet_str

# database related stuff
import logging
import itertools
import pymysql



"""
Param:
None
Output:
Returns the active connection
Summary:
Logs onto the database which saves flight logs
"""
def login():

# Connect to the database
    try:
        connection = pymysql.connect(host="ny.eldibaken.se",    # your host, usually localhost
                                     user="RW",         # your username
                                     passwd="3Dmip8otnZuvDHmL",  # your password
                                     db="Kand") #The database name
                                     #charset='utf8') #Charset used for database
                                    # cursorclass=pymysql.cursors.DictCursor) #cursorclass used

    except pymysql.err.OperationalError as e:
        print('Could not connect to the database at login session')
        logging.add_log(2, 'Failed to connect to the database at database.login() - %s' %e)


    return connection

"""
Param:
connection - the active database connection to be closed
Output:
Returns 1 if connection closed, 0 otherwise
Summary:
Logs out from the connected database
"""
def logout(connection):
    val_return = 0
    try:
        connection.close()
        val_return = 1


    except Exception as e:
        print('Could not end connection to database')
        logging.add_log(2, 'Failed to logout from the database at database.logout() - %s' %e)

    return val_return

def get_glider_ids(connection):
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Flarm_ID FROM Glider"
            cursor.execute(sql)
            result = cursor.fetchall()
            array = list(itertools.chain.from_iterable(result))
            return array

def get_tow_plane_ids(connection):

            with connection.cursor() as cursor:
                # Read a single record
                sql = "SELECT Flarm_ID FROM Tow_Plane"
                cursor.execute(sql)
                result = cursor.fetchall()
                array = list(itertools.chain.from_iterable(result))
                return array



"""
Param:
connection - the active database connection to get plane IDs from
Output:
Returns a list of all the airplane IDs in the database
Summary:
Gets which planes are registered in the database
"""
def get_plane_ids(connection):
    a1 = get_glider_ids(connection)
    a2 = get_tow_plane_ids(connection)
    array = a1+a2
    return array

def get_started_flight(connection):

    return ""

def new_flight(connection):

    return ""

def get_airfields_height():
    # the height above sealevel for parked planes
    # mabye set this as a variable that the users define when setting up the system
    # or let the program determine this and see how it behaves

    return ""

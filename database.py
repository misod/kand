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

"""
Param:
connection - the active database connection
Output:
Returns a list of all the airplane IDs in the database
Summary:
Finds all ongoing flights in the database
"""
def get_started_flight(connection):
    with connection.cursor() as cursor:
        sql = "SELECT Glider_id FROM Flight_Data WHERE Landing is NULL"
        cursor.execute(sql)
        result = cursor.fetchall()
        array = list(itertools.chain.from_iterable(result))
        return array

"""
Param:
connection - the active database connection
flight_number - the numbered label to give the flight logging
flight_type - which type of flight it is (training etc)
glider_id - the ID of which glider is used in the flight
towing_id - the ID of any used towing plane if there is any used
Output:
0 if failed, 1 if successful
Summary:
Adds a new flight to the database which is not finished.
"""
def new_flight(connection, flight_number, flight_type, glider_id, towing_id):
    val_return = 0
    try:
        if towing_id is None:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Flight_Data(Flight_No, Takeoff, Logged_Date, Flight_Type, Glider_id, Flight_Status) VALUES (%s, CURRENT_TIMESTAMP, CURRENT_DATE, %s, %s, 'Ongoing')"
                cursor.execute(sql, (flight_number, flight_type, glider_id))
                connection.commit()
                val_return = 1
        else:
            with connection.cursor() as cursor:
                sql = "INSERT INTO Flight_Data(Flight_No, Takeoff, Logged_Date, Flight_Type, Glider_id, Towing_id, Towing_Takeoff, Flight_Status) VALUES (%s, CURRENT_TIMESTAMP, CURRENT_DATE, %s, %s, %s, CURRENT_TIMESTAMP, 'Ongoing')"
                cursor.execute(sql, (flight_number, flight_type, glider_id, towing_id))
                connection.commit()
                val_return = 1
    except Exception as e:
        print('Could not start a new flight')
        logging.add_log(2, 'Failed to start a new flight at database.new_flight() - %s' %e)

    return val_return


"""
Param:
connection - the active database connection
flarm_id - the flarm identifier of the tow plane which has landed
Output:
0 if failed, 1 if successful
Summary:
Lands a towing plane and logs it
"""
def tow_plane_landing(connection, flarm_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Towing_Landing = CURRENT_TIMESTAMP WHERE Towing_id = %s AND Towing_Landing is NULL"
            cursor.execute(sql, (flarm_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not land towing plane')
        logging.add_log(2, 'Failed to land towing plane at database.tow_plane_landing() - %s' %e)
    return val_return


"""
Param:
connection - the active database connection
flarm_id - flarm identifier of the glider which is landing
Output:
0 if failed, 1 if successful
Summary:
Ends an ongoing flight when glider is landing
"""
def end_flight(connection, flarm_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql  = "UPDATE Flight_Data SET Landing = CURRENT_TIMESTAMP, Flight_Status = 'Finished' WHERE Glider_id = %s AND Flight_Status = 'Ongoing'"
            cursor.execute(sql, (flarm_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not end flight')
        logging.add_log(2, 'Failed to end flight at database.end_flight() - %s' %e)
    return val_return


"""
Param:
connection - the active database connection
flight_number - the flight number ot add comment to
note - The comment to add
Output:
0 if failed, 1 if successful
Summary:
Adds a note to a flight logg
"""
def add_flight_notes(connection, flight_number, note):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Notes = %s WHERE Flight_No = %s"
            cursor.execute(sql, (note, flight_number))
            connection.commit()
            val_return = 1
    except Exception as e:
        Print('Could not add comment to flight log')
        logging.add_log(1, 'Failed to add a note to a flight log at database.add_flight_notes() - %s' %e)
    return val_return


"""
Param:
connection - the active database connection
aircraft_id - the flight clubs label of the aircraft
glider_id - the Flarm related id of the aircraft
Output:
0 if failed, 1 if successful
Summary:
Adds a new glider plane to the database.
"""
def add_glider(connection, aircraft_id, glider_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Glider(Glider_ID, Flarm_ID) VALUES (%s, %s)"
            cursor.execute(sql, (aircraft_id, glider_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not add a new glider')
        logging.add_log(2, 'Failed to add a glider at database.add_glider() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
aircraft_id - the flight clubs label of the aircraft
towing_id - the Flarm related id of the aircraft
Output:
0 if failed, 1 if successful
Summary:
Adds a new tow plane to the database.
"""
def add_tow_plane(connection, aircraft_id, towing_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Tow_Plane(Towing_ID, Flarm_ID) VALUES (%s, %s)"
            cursor.execute(sql, (aircraft_id, towing_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not add a new tow plane')
        logging.add_log(2, 'Failed to add a tow plane at database.add_tow_plane() - %s' %e)
    return val_return

def get_airfields_height():
    # the height above sealevel for parked planes
    # mabye set this as a variable that the users define when setting up the system
    # or let the program determine this and see how it behaves

    return ""

# database related stuff
import logging
import itertools
import pymysql
import helpers
import datetime

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
        logging.add_log(0, 'Connecting to database successful')
        return connection

    except pymysql.err.OperationalError as e:
        print('Could not connect to the database at login session')
        logging.add_log(2, 'Failed to connect to the database at database.login() - %s' %e)
        return (-1)


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
        logging.add_log(0, 'Logging out from database successful')
        val_return = 1


    except Exception as e:
        print('Could not end connection to database')
        logging.add_log(2, 'Failed to logout from the database at database.logout() - %s' %e)

    return val_return

"""
Param:
connection - the active database connection to get plane IDs from
Output:
Returns a list of all the glider IDs in the database
Summary:
Gets which gliders are registered in the database
"""
def get_glider_ids(connection):
    try:
        with connection.cursor() as cursor:
            # Read a single record
            sql = "SELECT Flarm_ID FROM Glider"
            cursor.execute(sql)
            result = cursor.fetchall()
            array = list(itertools.chain.from_iterable(result))
            ret_array =  [helpers.hex_string_to_int(e) for e in array]
            return ret_array
    except Exception as e:
        print('Could not list all gliders')
        logging.add_log(1, 'Failed to list all gliders registered in the database at database.get_glider_ids() - %s' %e)
        return (-1)


"""
Param:
connection - the active database connection to get plane IDs from
Output:
Returns a list of all the tow plane IDs in the database
Summary:
Gets which tow planes are registered in the database
"""
def get_tow_plane_ids(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT Flarm_ID FROM Tow_Plane"
            cursor.execute(sql)
            result = cursor.fetchall()
            array = list(itertools.chain.from_iterable(result))
            ret_array =  [helpers.hex_string_to_int(e) for e in array]
            return ret_array
    except Exception as e:
        print('Could not list all tow planes')
        logging.add_log(1, 'Failed to list all tow planes registered in the database at database.get_tow_plane_ids() - %s' %e)
        return (-1)


"""
Param:
connection - the active database connection to get plane IDs from
Output:
Returns a list of all the airplane IDs in the database
Summary:
Gets which planes are registered in the database
"""
def get_plane_ids(connection):
    try:
        a1 = get_glider_ids(connection)
        a2 = get_tow_plane_ids(connection)
        array = a1+a2
        return array
    except Exception as e:
        print('Could not list all aircrafts')
        logging.add_log(1, 'Failed to list all aircrafts registered in the database at database.get_plane_ids() - %s' %e)
        return (-1)


"""
Param:
connection - the active database connection
Output:
Returns a list of all the airplane IDs in the database
Summary:
Finds all ongoing flights in the database
"""
def get_started_flight(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT Glider_id, Towing_id, Takeoff, Max_Height, Towing_Height FROM Flight_Data WHERE Flight_Status = %s"
            cursor.execute(sql, 'Ongoing')
            result = cursor.fetchall()
            array = list(result)
            new_array = [(helpers.hex_string_to_int(e[0]),helpers.hex_string_to_int(e[1]), e[2].total_seconds(), e[3], e[4]) for e in array]
            return new_array
    except Exception as e:
        print('Could not list ongoing flights')
        logging.add_log(1, 'Failed to list all ongoing flights registered in the database at database.get_started_flight() - %s' %e)
        return (-1)

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
Adds a new flight to the database which != finished.
"""
def new_flight(connection, glider_id, towing_id, time):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Flight_Data(Takeoff, Logged_Date, Glider_id, Towing_id, Flight_Status) VALUES (%s, CURRENT_DATE, %s, %s, 'Ongoing')"
            cursor.execute(sql, (time, glider_id, towing_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not start a new flight')
        logging.add_log(2, 'Failed to start a new flight at database.new_flight() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
glider_id - the ID of which glider to assign to flight
towing_id - the ID of tow plane which is in flight
Output:
0 if failed, 1 if successful
Summary:
Adds a glider to an assisting flight log in the database.
"""
def assign_glider(connection, glider_id, towing_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Glider_id = %s where Towing_id = %s"
            cursor.execute(sql, (glider_id, towing_id))
            connection.commit()
            val_return  = 1
    except Exception as e:
        print('Could not assign glider to flight')
        logging.add_log(1, 'Failed to add a glider to a flight at database.assign_glider() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
glider_id - the ID of which glider is in flight
towing_id - the ID of tow plane to assign to flight
Output:
0 if failed, 1 if successful
Summary:
Adds a glider to an assisting flight log in the database.
"""
def assign_tow_plane(connection, glider_id, towing_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Towing_id = %s where Glider_id = %s"
            cursor.execute(sql, (towing_id, glider_id))
            connection.commit()
            val_return  = 1
    except Exception as e:
        print('Could not assign tow plane to flight')
        logging.add_log(1, 'Failed to add a tow plane to a flight at database.assign_tow_plane() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
flarm_id - the ID of which aircraft is used in the flight
flight_type - flight type to be assigned to the flight
Output:
0 if failed, 1 if successful
Summary:
Adds a flight type to a flight log
"""
def assign_flight_type(connection, aircraft_id, flight_type):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Flight_Type = %s where Glider_id = %s OR Towing_id = %s"
            cursor.execute(sql, (flight_type, aircraft_id, aircraft_id))
            val_return  = 1
    except Exception as e:
        print('Could not assign tow plane to flight')
        logging.add_log(1, 'Failed to add a tow plane to a flight at database.assign_tow_plane() - %s' %e)



"""
Param:
connection - the active database connection
flarm_id - the flarm identifier of the tow plane which has landed
Output:
0 if failed, 1 if successful
Summary:
Lands a towing plane and logs it
"""
def tow_plane_landing(connection, flarm_id, time):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Towing_Landing = %s, Towing_Time = TIMEDIFF(%s, Takeoff) WHERE Towing_id = %s AND Towing_Landing is NULL"
            cursor.execute(sql, (time, time, flarm_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not land towing plane')
        logging.add_log(2, 'Failed to land towing plane at database.tow_plane_landing() - %s' %e)
    return val_return

def end_towplane_flight(connection, flarm_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql  = "UPDATE Flight_Data SET Flight_Status = 'Finished' WHERE Towing_id = %s AND Flight_Status = 'Ongoing' AND Glider_id is Null"
            cursor.execute(sql, flarm_id)
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not end flight')
        logging.add_log(2, 'Failed to end flight at database.end_towplane_flight() - %s' %e)
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
def end_flight(connection, flarm_id, time):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql  = "UPDATE Flight_Data SET Glider_Landing = %s, Flight_Status = 'Finished', Flight_Time = TIMEDIFF(%s, Takeoff) WHERE Glider_id = %s AND Flight_Status = 'Ongoing'"
            cursor.execute(sql, (time, time, flarm_id))
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
            sql = "INSERT INTO Glider(Glider_ID, Flarm_ID, Daily_Surveillance_Performed) VALUES (%s, %s, 'No')"
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
            sql = "INSERT INTO Tow_Plane(Towing_ID, Flarm_ID, Daily_Surveillance_Performed) VALUES (%s, %s, 'No')"
            cursor.execute(sql, (aircraft_id, towing_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not add a new tow plane')
        logging.add_log(2, 'Failed to add a tow plane at database.add_tow_plane() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
id - the id of the pilot to be added
name - the actualy name of the pilot
Output:
0 if failed, 1 if successful
Summary:
Adds a new pilot to the database
"""
def add_pilot(connection, id, name):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Pilot(Pilot_ID, Name) VALUES (%s, %s)"
            cursor.execute(sql, (id, name))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not add a new pilot')
        logging.add_log(2, 'Failed to add a pilot at database.add_pilot() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
Output:
A list of all registered pilots
Summary:
Lists pilots
"""
def list_pilot(connection):
    try:
        with connection.cursor() as cursor:
            sql = "SELECT * FROM Pilot"
            cursor.execute(sql)
            result = cursor.fetchall()
        return result
    except Exception as e:
        print('Could not list all pilots')
        logging.add_log(1, 'Failed to list all pilots registered in the database at database.list_pilot() - %s' %e)

"""
Param:
connection - the active database connection
fligt_number - number of the flight log to assign pilot to
pilot_id - pilot to assign to the flight
flight_type - which type of flight it was
Output:
0 if failed, 1 if successful
Summary:
Adds a flew instance to database for the flight log with given pilot
"""
def assign_flight(connection, flight_number, pilot_id, flight_type):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO Flew(Flight_No, Pilot_ID, Flight_Type) VALUES (%s, %s, %s)"
            cursor.execute(sql, (flight_number, pilot_id, flight_type))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not assign pilot to flight')
        logging.add_log(2, 'Failed to add a pilot to a flight at database.assign_flight() - %s' %e)
    return val_return


"""
Param:
connection - the active database connection
fligt_number - number of the flight log to assign pilot to
pilot_id - pilot to assign to the flight
flight_type - which type of flight it was
Output:
0 if failed, 1 if successful
Summary:
Adds a flew instance to database for the flight log with given pilot
"""
def assign_tow_pilot(connection, flight_number, pilot_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Towing_Pilot = %s WHERE Flight_No = %s"
            cursor.execute(sql, (pilot_id, flight_number))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not assign tow pilot to flight')
        logging.add_log(2, 'Failed to add a pilot to a flight at database.assign_tow_pilot() - %s' %e)
    return val_return

def assign_glider_pilot(connection, flight_number, pilot_id):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Glider_Pilot = %s WHERE Flight_No = %s"
            cursor.execute(sql, (pilot_id, flight_number))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not assign glider pilot to flight')
        logging.add_log(2, 'Failed to add a pilot to a flight at database.assign_glider_flight() - %s' %e)
    return val_return

"""
Param:
connection - the active database connection
glider_id - gider which was surveilled
pilot_id - pilot which performed the surveillance
notes - any notes to add to the surveillance
Output:
0 if failed, 1 if successful
Summary:
Adds a surveillance performed for the current date.
"""
def surveilled_glider(connection, glider_id, pilot_id, notes):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql1 = "INSERT INTO Daily_Surveillance(Flarm_ID, Logged_Date, Note) VALUES (%s, CURRENT_DATE, %s)"
            cursor.execute(sql1, (glider_id, notes))
            sql2 = "INSERT INTO Surveilled(Flarm_ID, Logged_Date, Pilot_ID) VALUES (%s, CURRENT_DATE, %s)"
            cursor.execute(sql2, (glider_id, pilot_id))
            sql3 = "UPDATE Glider SET Daily_Surveillance_Performed = 'Yes' WHERE Flarm_ID = %s"
            cursor.execute(sql3, (glider_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not perform surveillance')
        logging.add_log(2, 'Failed to perform surveillance at database.surveilled_glider() - %s' %e)
    return val_return


"""
Param:
connection - the active database connection
towing_id - tow plane which was surveilled
pilot_id - pilot which performed the surveillance
notes - any notes to add to the surveillance
Output:
0 if failed, 1 if successful
Summary:
Adds a surveillance performed for the current date.
"""
def surveilled_tow_plane(connection, towing_id, pilot_id, notes):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql1 = "INSERT INTO Daily_Surveillance(Flarm_ID, Logged_Date, Note) VALUES (%s, CURRENT_DATE, %s)"
            cursor.execute(sql1, (towing_id, notes))
            sql2 = "INSERT INTO Surveilled(Flarm_ID, Logged_Date, Pilot_ID) VALUES (%s, CURRENT_DATE, %s)"
            cursor.execute(sql2, (towing_id, pilot_id))
            sql3 = "UPDATE Tow_Plane SET Daily_Surveillance_Performed = 'Yes' WHERE Flarm_ID = %s"
            cursor.execute(sql3, (towing_id))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not perform surveillance')
        logging.add_log(2, 'Failed to perform surveillance at database.surveilled_glider() - %s' %e)
    return val_return


"""
Param:
connection - the active database connection
Output:
0 if failed, 1 if successful
Summary:
Resets all surveillances of tow planes and gliders to 'No' to be used at midnight to reset daily surveillances
"""
def reset_surveillance(connection):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql1 = "UPDATE Glider SET Daily_Surveillance_Performed = 'No'"
            sql2 = "UPDATE Tow_Plane SET Daily_Surveillance_Performed = 'No'"
            cursor.execute(sql1)
            cursor.execute(sql2)
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not reset daily surveillance')
        logging.add_log(2, 'Failed to reset daily surveillances at database.reset_surveillance() - %s' %e)
    return val_return


def update_glider_height(connection, flarm_id, height):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Max_Height = %s WHERE Glider_id = %s AND Flight_Status = %s"
            cursor.execute(sql, (height, flarm_id, "Ongoing"))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not update gliders max height')
        logging.add_log(2, 'Failed to update gliders max height at database.update_glider_height() - %s' %e)
    return val_return

def update_tow_height(connection, flarm_id, height):
    val_return = 0
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE Flight_Data SET Towing_Height = %s WHERE Towing_id = %s AND Towing_Landing IS %s"
            cursor.execute(sql, (height, flarm_id, None))
            connection.commit()
            val_return = 1
    except Exception as e:
        print('Could not update towing height')
        logging.add_log(2, 'Failed to update towing height at database.update_tow_height() - %s' %e)
    return val_return

def get_airfields_height():
    # the height above sealevel for parked planes
    # mabye set this as a variable that the users define when setting up the system
    # or let the program determine this and see how it behaves

    return 10

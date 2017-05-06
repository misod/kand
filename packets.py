# for packet processing and evaluation

import logging
import helpers
import database
from ctypes import *

threshold_speed = 30 # in km/h
threshold_landing_speed = 10 # in mk/h
dif_time = 90 # in sec
dif_height = 15 # in meters

def relevant_package(array_whit_id, package):
    if package.src_callsign is not None and len(package.src_callsign) > 6:
        try:
            id_hex = helpers.get_flarm_id(package)
            if helpers.array_contains(array_whit_id, id_hex):
                return True


        except Exception as e:
            logging.add_log(1, ("Galet->packets, funk relevant_package, %s ->>> %s" % (e, package[0].orig_packet)))

    return False

def processing(glider_ids, towing_ids, package, database_con):

    ret = False
    package_flarm_id = helpers.get_flarm_id(package)
    active_plane_flarms = active_flight(package, database_con)
    if active_plane_flarms is -1:

        if package.speed > threshold_speed:
            if helpers.array_contains(glider_ids, package_flarm_id):
                if not database.new_flight(database_con, package_flarm_id, None, package.timestamp):
                    logging.add_log(2, "Failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
                ret = True
            elif helpers.array_contains(towing_ids, package_flarm_id):
                if not database.new_flight(database_con, None, package_flarm_id, package.timestamp):
                    logging.add_log(2, "Failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
                ret = True
        else:
            logging.add_log(0, "Slane package recived, not moving fast enough and not active_flight ---> %s" %package.orig_packet.encode('string-escape'))
            ret = True
    elif len(active_plane_flarms) > 0:
        if fix_connected_plane(active_plane_flarms, package, database_con):
            ret = True
        elif check_plane_landed(package):
            if not update_landed_plane(active_plane_flarms, package, database_con):
                ret = False
            ret = True
        elif update_height_of_flight(active_plane_flarms, package, database_con):
            ret = True
        ret = False
    else:
        logging.add_log(1, "Something went wrong in processing package ---> %s " %package.orig_packet.encode('string-escape'))
        ret = False

    return ret

def update_landed_plane(active_plane_flarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)

    for e in active_plane_flarms:
        if e[0] == package_flarm_id:
            return database.end_flight(database_con, package_flarm_id, package.timestamp)
        if e[1] == package_flarm_id:
            return database.tow_plane_landing(database_con, package_flarm_id, package.timestamp)
    return False

def update_height_of_flight(active_plane_flarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)
    try:
        for e in active_plane_flarms:
            if e[0] == package_flarm_id and e[3] < package.altitude:

                if database.update_glider_height(database_con, helpers.long_to_hex_str(package_flarm_id), int(package.altitude.contents.value)):
                    return False
                return True
            elif e[1] == package_flarm_id and e[4] < package.altitude:
                if not database.update_towing_height(database_con, helpers.long_to_hex_str(package_flarm_id), int(package.altitude.contents.value)):
                    return False
                return True
    except Exception as e:
        logging.add_log(2, "Something went wrong when trying to update flight height ---> %s" %e)

    return False

def check_plane_landed(package):
    if package.altitude < ( dif_height + database.get_airfields_height()) and package.speed < threshold_landing_speed :
        return True
    return False

def fix_connected_plane(active_plane_flarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)
    for e in active_plane_flarms:

        if ( e[0] == None or e[1] == None ) and (e[2] < (dif_time + helpers.timestamp_to_seconds(package.timestamp)) and  (e[2] > dif_time - helpers.timestamp_to_seconds(package.timestamp))):

            if e[0] is not package_flarm_id and e[1] == None:
                if not database.assign_tow_plane(database_con, e[0], package_flarm_id):
                    logging.add_log(2, "Adding to database went wrong in fix_connected_plane --- kod 1")
                    return -1
            elif e[1] is not package_flarm_id and e[0] == None:
                if not database.assign_glider(database_con, package_flarm_id, e[1]):
                    logging.add_log(2, "Adding to database went wrong in fix_connected_plane --- kod 2")
                    return -1
            return True


    return None

def active_flight(packet, database_con):

    active_plane_flarms = database.get_started_flight(database_con)

    if active_plane_flarms is not -1:

        active_flights = [e[0] for e in active_plane_flarms]
        active_flights +=  [e[1] for e in active_plane_flarms]

        if helpers.array_contains(active_flights, helpers.get_flarm_id(packet)):
            return active_plane_flarms

    return -1

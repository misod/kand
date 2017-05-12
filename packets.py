# for packet processing and evaluation

import logging
import helpers
import database
from ctypes import *

threshold_speed = 30 # in km/h
threshold_landing_speed = 10 # in km/h
dif_time = 120 # in sec
dif_height = 15 # in meters

def relevant_package(array_whit_id, package):
    if package.src_callsign != None and len(package.src_callsign) > 6:
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
    if not active_plane_flarms[0]:
        if fix_connected_plane(towing_ids, active_plane_flarms[1], package, database_con):
            ret = True
            logging.add_log(0, "Plane connected to another flight")
        elif  helpers.get_value_converted_int(package.speed) >= threshold_speed:
            if helpers.array_contains(glider_ids, package_flarm_id):
                if not database.new_flight(database_con, helpers.long_to_hex_str(package_flarm_id), None, int(package.raw_timestamp)):
                    logging.add_log(2, "Failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
                else:
                    ret = True
            elif helpers.array_contains(towing_ids, package_flarm_id):
                if not database.new_flight(database_con, None, helpers.long_to_hex_str(package_flarm_id), int(package.raw_timestamp)):
                    logging.add_log(2, "Failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
                else:
                    ret = True
        else:
            logging.add_log(0, "Plane package recived, not moving fast enough and not active_flight ---> %s" %package.orig_packet.encode('string-escape'))
            ret = True
    elif len(active_plane_flarms[1]) > 0:
        if check_plane_landed(active_plane_flarms[1], package):
            if not update_landed_plane(active_plane_flarms[1], package, database_con):
                logging.add_log(1, "problem regestring plane landing ----> kod 32")
                ret = False
            else:
                ret = True
        elif update_height_of_flight(active_plane_flarms[1], package, database_con):
            ret = True
    else:
        logging.add_log(1, "Something went wrong in processing package ---> %s " %package.orig_packet.encode('string-escape'))

    return ret

def update_landed_plane(active_plane_flarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)
    for e in active_plane_flarms:
        if e[0] == package_flarm_id:
            return database.end_flight(database_con, helpers.long_to_hex_str(package_flarm_id), int(package.raw_timestamp))
        elif e[1] == package_flarm_id and e[0] is not None:
            return database.tow_plane_landing(database_con, helpers.long_to_hex_str(package_flarm_id), int(package.raw_timestamp))
        elif e[1] == package_flarm_id and e[0] is None:
            if database.tow_plane_landing(database_con, helpers.long_to_hex_str(package_flarm_id), int(package.raw_timestamp)):
                return database.end_towplane_flight(database_con, helpers.long_to_hex_str(package_flarm_id))

    return False

def update_height_of_flight(active_plane_flarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)
    try:
        for e in active_plane_flarms:
            if e[0] is not None and e[0] == package_flarm_id and ( e[3] is None or e[3] < helpers.get_value_converted_int(package.altitude)):
                if not database.update_glider_height(database_con, helpers.long_to_hex_str(package_flarm_id), helpers.get_value_converted_int(package.altitude)):
                    return False
                return True
            elif e[1] is not None and e[1] == package_flarm_id and (e[4] is None or e[4] < helpers.get_value_converted_int(package.altitude)):
                if not database.update_tow_height(database_con, helpers.long_to_hex_str(package_flarm_id), helpers.get_value_converted_int(package.altitude)):
                    return False
                return True

    except Exception as e:
        logging.add_log(2, "Something went wrong when trying to update flight height ---> %s" %e)
        print "Something went wrong when trying to update flight height ---> %s" %e
        return False

    logging.add_log(0, "plane height not updated")
    return True

def check_plane_landed(active_plane_flarms, package):
    package_flarm_id = helpers.get_flarm_id(package)
    for e in active_plane_flarms:
        if (e[0] is not None and e[0] == package_flarm_id) or (e[1] is not None and e[1] == package_flarm_id):
            if helpers.get_value_converted_int(package.altitude) < (dif_height + database.get_airfields_height()) and (helpers.get_value_converted_int(package.speed) <= threshold_landing_speed) and (e[2]+dif_time < helpers.raw_timestamp_to_seconds(package.raw_timestamp)):
                return True
    return False

def fix_connected_plane(towing_ids, active_plane_flarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)
    for e in active_plane_flarms:
        if (e[0] is None or e[1] is None) and (e[2] <= (dif_time + helpers.raw_timestamp_to_seconds(package.raw_timestamp)) and (e[2] >= (-dif_time + helpers.raw_timestamp_to_seconds(package.raw_timestamp)))):

            if e[0] != package_flarm_id and e[1] is None and helpers.array_contains(towing_ids, package_flarm_id):
                if not database.assign_tow_plane(database_con, helpers.long_to_hex_str(e[0]), helpers.long_to_hex_str(package_flarm_id)):
                    logging.add_log(2, "Adding to database went wrong in fix_connected_plane --- kod 1")
                    return False
                return True
            elif e[1] != package_flarm_id and e[0] is None and not helpers.array_contains(towing_ids, package_flarm_id):
                if not database.assign_glider(database_con, helpers.long_to_hex_str(package_flarm_id), helpers.long_to_hex_str(e[1])):
                    logging.add_log(2, "Adding to database went wrong in fix_connected_plane --- kod 2")
                    return False
                return True
    return False

def active_flight(packet, database_con):

    active_plane_flarms = database.get_started_flight(database_con)
    if active_plane_flarms != -1:

        active_flights = [e[0] for e in active_plane_flarms]
        for e in active_plane_flarms:
            if e[5]:
                active_flights += [e[1]]

        if helpers.array_contains(active_flights, helpers.get_flarm_id(packet)):
            return (1, active_plane_flarms)

    return (0, active_plane_flarms)

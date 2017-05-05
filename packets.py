# for packet processing and evaluation

import logging
import helpers

threshold_speed = 30 # in km/h
threshold_landing_speed = 10 # in mk/h
dif_time = 90 # in sec
dif_hight = 15 # in meters

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

    #determin if plane is on ground
    #se which is the towing plane
    #log to database
    #starting flight or landing?
    ret = False
    package_flarm_id = helpers.get_flarm_id(package)
    active_plane_falarms = active_flight(package, database_con)
    if active_plane_falarms is -1:

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
    elif len(active_plane_falarms) > 0:
        if fix_connected_plane(active_plane_falarms, package):
            ret = True
        elif plane_landed(package):
            # TODO register plane as landed and se if it was a legit Flight
            ret = True
        elif update_height_of_flight(active_plane_falarms, package, database_con):
            # TODO register updated height for a flight
            ret = True
        else:
            logging.add_log(1, "somethin we didnt expect just happned ---> kod 4")
            ret = False

    else:
        logging.add_log(1, "Something went wrong in processing package ---> %s " %package.orig_packet.encode('string-escape'))
        ret = False

    return ret

def update_height_of_flight(active_plane_falarms, package, database_con):

    return ""

def plane_landed(package):
    if package.altitude < ( dif_hight + database.get_airfields_height()) and package.speed < threshold_landing_speed :
        return True
    return False

def fix_connected_plane(active_plane_falarms, package, database_con):
    package_flarm_id = helpers.get_flarm_id(package)
    for e in active_plane_falarms:

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

    active_plane_falarms = database.get_started_flight(database_con)

    if active_plane_falarms is not -1:

        active_flights = [e[0] for e in active_plane_falarms]
        active_flights +=  [e[1] for e in active_plane_falarms]

        if helpers.array_contains(active_flights, helpers.get_flarm_id(packet)):
            return active_plane_falarms

    return -1

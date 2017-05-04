# for packet processing and evaluation

import logging
import helpers

threshold_speed = 30

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
                    logging.add_log(2, "failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
                ret = True
            elif helpers.array_contains(towing_ids, package_flarm_id):
                if not database.new_flight(database_con, None, package_flarm_id, package.timestamp):
                    logging.add_log(2, "failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
                ret = True
        else:
            logging.add_log(0, "plane package recived, not moving fast enough and not active_flight ---> %s" %package.orig_packet.encode('string-escape'))
            ret = True
    elif len(active_plane_falarms) > 0:
        
        ret = True
    else:
        logging.add_log(1, "something went wrong in processing package ---> %s " %package.orig_packet.encode('string-escape'))
        ret = False

    return ret

def no_connected_plane(package):

    return ""

def active_flight(packet, database_con):
    active_plane_falarms = database.get_started_flight(database_con)
    if active_plane_falarms is not -1:
        if helpers.array_contains(active_plane_falarms, helpers.get_flarm_id(packet)):
            return active_plane_falarms
        else:
            return -1

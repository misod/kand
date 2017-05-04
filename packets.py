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
    package_flarm_id = helpers.get_flarm_id(package)

    if not active_flight(glider_ids, towing_ids, package, database_con):


        if package.speed > threshold_speed:
            if helpers.array_contains(glider_ids, package_flarm_id):
                if not database.new_flight(database_con, package_flarm_id, None, package.timestamp):
                    logging.add_log(2, "failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
            elif helpers.array_contains(towing_ids, package_flarm_id):
                if not database.new_flight(database_con, None, package_flarm_id, package.timestamp):
                    logging.add_log(2, "failed to start a new fligt for glider -> %s" %package.orig_packet.encode('string-escape'))
        else:
            logging.add_log(0, "plane package recived, not moving fast enough and not active_flight ---> %s" %package.orig_packet.encode('string-escape'))


def determine_connected_plane(package):


    return ""

def active_flight(glider_ids, towing_ids, packet, database_con):
    plane_falarms = database.get_started_flight(database_con)
    if plane_falarms is not -1:
        if helpers.array_contains(plane_falarms, helpers.get_flarm_id(packet)):
            return True
        else:
            return False

    return True

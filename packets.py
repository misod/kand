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

def processing(glider_ids, towing_id, package, database_con):

    #determin if plane is on ground
    #se which is the towing plane
    #log to database
    #starting flight or landing?
    if not active_flight(package):
        if package.speed > threshold_speed :
            database.new_flight(database_con, helpers.get_flarm_id(package))



def determine_towing_plane(package):


    return ""

def active_flight(packet, database_con):
    plane_falarms = database.get_started_flight(database_con)
    if plane_falarms is not -1:
        if helpers.array_contains(plane_falarms, helpers.get_flarm_id(packet)):
            return True
        else:
            return False

    return True

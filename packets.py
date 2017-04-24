# for packet processing and evaluation

import logging
import helpers

threshold_speed = 4

def relevant_package(array_whit_id, package):
    if package[0].src_callsign is not None and len(package[0].src_callsign) > 6:

        try:
            id_hex = helpers.hex_string_to_int(package[0].src_callsign[3:])
            if helpers.array_contains(array_whit_id, id_hex):
                return True

        except Exception as e:
            logging.add_log(1, ("galet->packets, funk relevant_package, %s, %s" % (e, package[0].orig_packet)))

    return False

def processing(package):

    #determin if plane is on ground
    #se which is the towing plane
    #log to database
    #starting flight or landing?
    plane_stationary = plane_on_ground(package)

    if active_flight(package):
        #do some more processing
        # se if it's time to regiser ended flight
        return False
    elif not plane_stationary:
        # time to register a new_flight
        # find out towing plane
        return False
    return True

def determine_towing_plane(package):


    return ""

def active_flight(packet):

    return True

def plane_on_ground(package):


    return True

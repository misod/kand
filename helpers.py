# helper functions that doesnt belong in any of the other files
import logging

def hex_string_to_int(str):

    val = int(str, 16)

    return val

def array_contains(array, element):

    for e in array:
        if e == element:
            return True

    return False

def get_flarm_id(packet):

    try:
        flarm_id = hex_string_to_int(packet.src_callsign[3:])
    except Exception as e:
        logging.add_log(1, "failed to get flarm id ----> %s" %e)
        flarm_id = -1

    return flarm_id

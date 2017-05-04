# helper functions that doesnt belong in any of the other files
import logging

def hex_string_to_int(str):
    try:
        val = int(str, 16)
        return val
    except Exception as e:
        return None

def array_contains(array, element):

    for e in array:
        if e == element:
            return True

    return False

def get_element_index(array, element):
    i = 0;
    for e in array:
        if e == element:
            return element
        i = i+1

    return -1

def timestamp_to_seconds(timestamp):
    try:
        i = int(timestamp[:5])
        return i
    except Exception as e:
        logging.add_log(1, "failed CONVERTING timestamp to int----> %s" %e)
        return None

def get_flarm_id(packet):

    try:
        flarm_id = hex_string_to_int(packet.src_callsign[3:])
    except Exception as e:
        logging.add_log(1, "failed to get flarm id ----> %s" %e)
        flarm_id = -1

    return flarm_id

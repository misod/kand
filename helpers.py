# helper functions that doesnt belong in any of the other files
import logging
import packets
import struct

def hex_string_to_int(str):
    try:
        val = int(str, 16)
        return val
    except Exception as e:
        return None

def long_to_hex_str(l):
    return hex(struct.unpack('<I', struct.pack('<l', l))[0])

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

def raw_timestamp_to_seconds(raw_timestamp):
    try:
        sec = int(raw_timestamp[0:2])*3600
        sec += int(raw_timestamp[2:4])*60
        sec += int(raw_timestamp[4:6])

        return sec
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

def main_func(libfap, glider_id_array, towingplane_id_array, active_database_connection, packet_str):

    # Parse packet using libfap.py into fields to process, eg:
    packet_parsed = libfap.fap_parseaprs(packet_str, len(packet_str), 0)

    if packets.relevant_package(glider_id_array+towingplane_id_array, packet_parsed[0]):
        if not logging.log_packet(packet_str):
            logging.add_log(1, "Logging the flight packets went wrong, %s" % packet_str)

        if not packets.processing(glider_id_array, towingplane_id_array, packet_parsed[0], active_database_connection):
            logging.add_log(2, "Main -> processing packet went wrong")

    if len(packet_str) == 0:
        print "Read returns zero length string. Failure.  Orderly closeout"
        return -2

    return True

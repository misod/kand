# helper functions that doesnt belong in any of the other files
import logging

def relevant_package(array_whit_id, package):
    if package[0].src_callsign is not None and len(package[0].src_callsign) > 4:
        try:
            id_hex = hex_string_to_int(package[0].src_callsign[3:])
            if array_contains(array_whit_id, id_hex):
                return True

        except Exception as e:
            logging.add_log(1, "galet-> helpers, funk relevant_package")

        return False

def hex_string_to_int(str):

    val = int(str, 16)

    return val

def array_contains(array, element):

    for e in array:
        if e == element:
            return True

    return False

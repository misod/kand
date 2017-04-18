# for packet processing and evaluation

import logging
import helpers

def relevant_package(array_whit_id, package):
    if package[0].src_callsign is not None and len(package[0].src_callsign) > 4:
        try:
            id_hex = helpers.hex_string_to_int(package[0].src_callsign[3:])
            if helpers.array_contains(array_whit_id, id_hex):
                return True

        except Exception as e:
            logging.add_log(1, "galet->helpers, funk relevant_package")

        return False

def processing(package):



    return True

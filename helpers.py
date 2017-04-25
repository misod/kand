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

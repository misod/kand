import logging
import database
import sys

#logging.add_log(0, "Testar en simple log")
#logging.add_log(1, "Testar en small error log")
#logging.add_log(2, "Testar en big error log")
#logging.log_packet("Testar en log_packet")

DBCon = database.login()
print("Gliders registered:")
print(database.get_glider_ids(DBCon))
print("Tow planes registered:")
print(database.get_tow_plane_ids(DBCon))
#print("All planes registered:")
#print(database.get_plane_ids(DBCon))
print("Gliders in the air:")
print(database.get_started_flight(DBCon))
#database.new_flight(DBCon, 7, 'TEST7', '0xABCCBA', '0xBBBCCC')
#database.new_flight(DBCon, 8, 'TEST7', '0xAAABBB', '0xBBBAAA')
#database.add_glider(DBCon, 'AAA', '0xAAABBB')
#database.add_tow_plane(DBCon, 'BCD', '0xBBBCCC')
#database.tow_plane_landing(DBCon, '0xBBBAAA')
#database.end_flight(DBCon, '0xABCCBA')
#database.add_flight_notes(DBCon, 2, 'This is a test note')
database.logout(DBCon)

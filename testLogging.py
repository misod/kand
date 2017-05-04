import logging
import database
import datetime
import sys

#logging.add_log(0, "Testar en simple log")
#logging.add_log(1, "Testar en small error log")
#logging.add_log(2, "Testar en big error log")
#logging.log_packet("Testar en log_packet")

DBCon = database.login()
#Setup test environment
#database.add_pilot(DBCon, 1, 'JockTori')
#database.add_pilot(DBCon, 2, 'Nicole')
#database.add_pilot(DBCon, 3, 'Micke')
#database.add_pilot(DBCon, 4, 'Conraaaado')

#database.add_glider(DBCon, 'UDP', '0xAAAAAA')
#database.add_glider(DBCon, 'APM', '0xAAAAAB')
#database.add_glider(DBCon, 'UCM', '0xAAAAAC')
#database.add_glider(DBCon, 'UPU', '0xAAAAAD')

#database.add_tow_plane(DBCon, 'TAP', '0xBBBBBA')
#database.add_tow_plane(DBCon, 'TUC', '0xBBBBBB')
#database.add_tow_plane(DBCon, 'TEM', '0xBBBBBC')

print("Gliders registered:")
print(database.get_glider_ids(DBCon))
print("Tow planes registered:")
print(database.get_tow_plane_ids(DBCon))
#print("All planes registered:")
#print(database.get_plane_ids(DBCon))
print("Gliders in the air:")
print(database.get_started_flight(DBCon))
#print("Please corona")
#database.new_flight(DBCon, None, '0xBBBBBA', datetime.datetime.time(datetime.datetime.now()))
#database.assign_glider(DBCon, '0xAAAAAD', '0xBBBBBA')
#database.assign_tow_plane(DBCon, '0xAAAAAA', '0xBBBBBB')
#print(int)
#database.new_flight(DBCon, 8, 'TEST7', '0xAAABBB', '0xBBBAAA')
#database.add_glider(DBCon, 'AAA', '0xAAABBB')
#database.add_tow_plane(DBCon, 'BCD', '0xBBBCCC')
#database.tow_plane_landing(DBCon, '0xBBBAAA')
#database.end_flight(DBCon, '0xABCCBA')
#database.add_flight_notes(DBCon, 2, 'This is a test note')
#database.add_pilot(DBCon, 4, 'JockTori')
#print(database.list_pilot(DBCon))
#database.assign_flight(DBCon, 512, 4, 'Trial Flight')
#database.reset_surveillance(DBCon)
#database.surveilled_glider(DBCon, '0xAAAAAA', 4, 'Tyyp')
#database.surveilled_tow_plane(DBCon, '0xBBBBBB', 1, 'Igen')
database.logout(DBCon)

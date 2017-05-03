import logging
import database
import sys

#logging.add_log(0, "Testar en simple log")
#logging.add_log(1, "Testar en small error log")
#logging.add_log(2, "Testar en big error log")
#logging.log_packet("Testar en log_packet")

DBCon = database.login()
#print(database.get_glider_ids(DBCon))
#print(database.get_tow_plane_ids(DBCon))
#print(database.get_plane_ids(DBCon))
#print(database.get_started_flight(DBCon))
database.new_flight(DBCon, 2, 'TEST3', '0xABCDEF', None)
database.logout(DBCon)

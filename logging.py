import os.path
import sys

directory = os.path.join(sys.path[0], "logFiles")

"""
Param:
logType, an int corresponding to which type of log, 0 is a regular log, 1 is a smaller error log and 2 is a major error log
logMessage, which message to add to the errorlog
Output:
Returns 1 if successfull, otherwise 0
Summary:
Evaluates the sent logType, chooses a correct auxilliary function for each type of error.
"""
def add_log(logType, logMessage):
    val_return = 0

    if logType == 0:

        if log(logMessage, "simpleLog.txt"):
            val_return = 1
            #print("Message logged")

        else:
            print("Error: Problem logging the message, simpleLog.txt")

    elif logType == 1:

        if log(logMessage, "smallErrorLog.txt"):
            val_return = 1
            #print("Message logged")

        else:
            print("Error: Problem logging the message, smallErrorLog.txt")

    elif logType == 2:

        if log(logMessage, "bigErrorLog.txt"):
            val_return = 1
            #print("Message logged")

        else:
            print("Error: Problem logging the message, bigErrorLog")

    else:
        print("Error: Invalid log type")

    return val_return


"""
Param:
logMessage, which message to add to the log file
logFile, which log file to add the message to
Output:
1 if message logged, 0 if log failed
Summary:
Attempts to write the given log message to the regular log file
"""
def log(logMessage, logFile):
    logFile = os.path.join(directory, logFile)
    val_return = 0

    if os.path.isfile(logFile) and (os.access(logFile, os.W_OK)):

        with open(logFile, 'a') as log:

            try:
                logMessage = logMessage + "\n"
                log.write(logMessage)
                val_return = 1

            except Exception:
                print("Error writing to logfile, packet")

            finally:
                log.close()
                return val_return

    else:
        print("Logfile doesn't exist")
        file = open(logFile, 'w+')
        file.close()
        return val_return

"""
Param:
logMessage, what to log
Output:
returns 1 if message logged, 0 if failed
Summary:
used to store FLARM data packets during development
"""
def log_packet(logMessage):
    val_return = 0
    path = os.path.join(directory, "packetLog.txt")

    if os.path.isfile(path) and os.access(path, os.W_OK):

        with open(path, 'a') as log:

            try:
                logMessage = logMessage + "\n"
                log.write(logMessage)
                val_return = 1

            except Exception as e:
                print("Error writing to logfile")

            finally:
                log.close()
                return val_return

    else:
        print("Logfile doesn't exist")
        file = open(path, 'w+')
        file.close()
        return val_return

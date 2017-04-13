"""
Param:
logType, an int corresponding to which type of log, 0 is a regular log, 1 is a smaller error log and 2 is a major error log
logMessage, which message to add to the errorlog
Output:
Returns 1 if successfull, otherwise 0
Summary:
Evaluates the sent logType, chooses a correct auxilliary function for each type of error.
"""
def addLog(logType, logMessage):
    val_return = 0

    if logType == 0:

        if Log(logMessage, simpleLog):
            val_return = 1
            print("Message logged")

        else:
            print("Error: Problem logging the message")

    elif logType == 1:

        if Log(logMessage, smallErrorLog):
            val_return = 1
            print("Message logged")

        else:
            print("Error: Problem logging the message")

    elif logType == 2:

        if Log(logMessage, bigErrorLog):
            val_return = 1
            print("Message logged")

        else:
            print("Error: Problem logging the message")

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
def Log(logMessage, logFile):
    val_return = 0

    if os.path.isfile(logFile) and (os.access(logFile), os.W_OK):

        with open(logFIle, 'a') as log:

            try:
                log.write(logMessage)
                val_return = 1

            except Exception:
                print("Error writing to logfile")

            finally:
                log.close()
                return val_return

    else:
        print("Logfile doesn't exist")
        return val_return

"""
Param:
logMessage, what to log
Output:
returns 1 if message logged, 0 if failed
Summary:
used to store FLARM data packets during development
"""
def logPacket(logMessage):
    val_return = 0

    if os.path.isfile(packetLog) and os.access(packetLog, os.W_OK):

        with open(packetLog, 'a') as log:

            try:
                log.write(logMessage)
                val_return = 1

            except Exception:
                print("Error writing to logfile")

            finally:
                log.close()
                return val_return

    else:
        print("Logfile doesn't exist")
        return val_return

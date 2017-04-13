"""
Param:
logType, an int corresponding to which type of log, 0 is a regular log, 1 is a smaller error log and 2 is a major error log
logMessage, which message to add to the errorlog
Output:
Void
Summary:
Evaluates the sent logType, chooses a correct auxilliary function for each type of error.
"""
def addLog(logType, logMessage):
    if logType == 0:
        if simpleLog(logMessage):
            print("Message logged")
        else:
            print("Error: Problem logging the message")
    elif logType == 1:
        if smallErrorLog(logMessage):
            print("Message logged")
        else:
            print("Error: Problem logging the message")
    elif logType == 2:
        if bigErrorLog(logMessage):
            print("Message logged")
        else:
            print("Error: Problem logging the message")
    else:
        print("Error: Invalid log type")

"""
Param:
logMessage, which message to add to the errorlog
Output:
1 if message logged, 0 if log failed
Summary:
Attempts to write the given log message to the regular log file
"""
def simpleLog(logMessage):
    val_return = 0

    if os.path.isfile(simpleLog) and os.access(simpleLog, os.W_OK):
        with open(simpleLog, 'a') as log:
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
logMessage, which message to add to the errorlog
Output:
1 if message logged, 0 if log failed
Summary:
Attempts to write the given log message to the small error log file
"""
def smallErrorLog(logMessage):
    val_return = 0

    if os.path.isfile(smallErrorLog) and os.access(smallErrorLog, os.W_OK):
        with open(smallErrorLog, 'a') as log:
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
logMessage, which message to add to the errorlog
Output:
1 if message logged, 0 if log failed
Summary:
Attempts to write the given logmessage to the major error log file
"""
def bigErrorLog(logMessage):
    val_return = 0

    if os.path.isfile(bigErrorLog) and os.access(bigErrorLog, os.W_OK):
        with open(bigErrorLog, 'a') as log:
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

import time
import os
import sys


def iapmPrintAndLog(object, loglevel = 1):
    # There is 7 log level.
    # 1 - INFO; 2 - NOTICE; 3 - WARN; 4 - ERROR; 5 - CRITICAL; 6 - DEBUG; 7 - VERBOSE.
    level = ["INFO", "NOTICE", "WARN", "ERROR", "CRITICAL", "DEBUG", "VERBOSE"]
    # With debug mode and verbose mode off, IAPM will print the log with level 5 at most as default. 
    # If the loglevel is not set, IAPM will use log level 1 as default.
    
    # Make the log and initialize the be-print.
    log = "%s[%s]%s" % (time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), level[loglevel - 1], object)
    bePrint = object
    
    # According the log level to add something to show
    if verbose or (debug and loglevel <= 6):
        # But who cares? lol.
        print(log)
    elif loglevel <= 5:
        # That means CRITICAL at most.
        if loglevel >= 3:
            bePrint = "%s: %s" % (level[loglevel - 1], object)
        print(bePrint)
    
    # Finally write the log(Not finished)
        
        

def main():
    global debug
    global verbose
    debug = False
    verbose = False
    
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--debug":
            print("IAPM is running in debug mode now.")
            debug = True
        if sys.argv[i] == "--verbose" or sys.argv[i] == "-v":
            print("IAPM is running in verbose mode now.")
            verbose = True
    iapmPrintAndLog("hello info")
    iapmPrintAndLog("hello critical", 5)
    iapmPrintAndLog("hello debug", 6)
    iapmPrintAndLog("hello verbose", 7)


main()
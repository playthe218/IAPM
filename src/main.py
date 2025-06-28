import time
import os
import sys
import signal


def iapmDoProcess(action, packages):
    iapmPrintAndLog("Entered \"iapmDoProcess\".", 6)
    done = "ed"
    if action == "update":
        done = "d"
    iapmPrintAndLog("These packages will be %s%s:" % (action, done))
    for i in range(0, len(packages)):
        print(packages[i], end = " ")
    print() # lol, but need this.
    print("Allow IAPM to operate?", end = "")
    go = None
    while go == None:
        confirm = input(' [Y/n] ')
        YES = ["Y", "y"]
        NO = ["N", "n"]
        if confirm in YES:
            iapmPrintAndLog("User allowed to operate.", 6)
            go = True
        elif confirm in NO:
            iapmPrintAndLog("User stopped to operate.", 6)
            go = False
        else:
            print("Sorry, can't understand \"%s\"." % confirm, end = "")
    
    # Not Finished
    
    iapmPrintAndLog("Exiting \"iapmDoProcess\".", 6)
            

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
    
    # First(Basic) argv check.
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--debug":
            print("IAPM is running in debug mode now.")
            debug = True
        if sys.argv[i] == "--verbose" or sys.argv[i] == "-v":
            print("IAPM is running in verbose mode now.")
            verbose = True
    
    # Check if no more argv provided.
    if len(sys.argv) == 1:
        iapmPrintAndLog("Usage: iapm [ action ] [ packages ] [options]")
        iapmPrintAndLog("       iapm clean")
        sys.exit(0)
    
    # Second argv check.
    action = sys.argv[1]
    global targets
    global options
    targets = []
    options = []
    
    iapmPrintAndLog("The action is %s" % action, 6)
    for i in range(2, len(sys.argv)):
        if sys.argv[i].startswith("--") or sys.argv[i].startswith("-"):
            options.append(sys.argv[i])
            iapmPrintAndLog("Found an option \"%s\"." % sys.argv[i], 6)
        else:
            targets.append(sys.argv[i])
            iapmPrintAndLog("Found a target \"%s\"." % sys.argv[i], 6)
    iapmPrintAndLog("Final targets list: %s" % targets, 6)
    iapmPrintAndLog("Final options list: %s" % options, 6)
   
    # iapmPrintAndLog("hello info")
    # iapmPrintAndLog("hello critical", 5)
    # iapmPrintAndLog("hello debug", 6)
    # iapmPrintAndLog("hello verbose", 7)
    
    # Not finished: depend resolve
    packages = targets
    
    # Start Process.
    iapmDoProcess(action, packages)
    
    # Completed. ll1 or ll6 or ll7?
    iapmPrintAndLog("Completed!", 7)


main()
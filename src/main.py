import time
import os
import sys
import signal


def iapmDoProcess(action, packages):
    clean = False
    iapmPrintAndLog("Entered \"iapmDoProcess\".", 6)
    done = "ed"
    if action == "update":
        done = "d"
    iapmPrintAndLog("These following packages will be %s%s:" % (action, done), 2)
    for i in range(0, len(packages)):
        print(packages[i], end = " ")
    print() # lol, but need this.
    print("\033[34mContinue?\033[0m", end = "")
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
    
    stage = 0
    if action == "install":
        # For install: 1 - Download packages, 2, Unpack Packages, 3 - Run pre-install scripts, 4 - Install packages, 5 - Run post-install scripts.
        while go:
            # if im crazy, if it failed, why not let stage -= 1 and do again?
            stage += 1
            if stage == 1:
                # Download packages.
                try:
                    iapmPrintAndLog("[1/5] Download packages.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Downloading packages %s." % (i + 1, len(packages), targetPackage))
                        os.system('')
                except:
                    iapmPrintAndLog("An error occurred when *Downloading packages*. Exit now.", 4)
                    go = False
            if stage == 2:
                # Unpack packages.
                try:
                    iapmPrintAndLog("[2/5] Unpack packages.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Unpacking packages %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.
                except:
                    iapmPrintAndLog("An error occurred when *Unpacking packages*. Exit now.", 4)
                    go = False
            if stage == 3:
                # Do pre-install scripts.
                try:
                    iapmPrintAndLog("[3/5] Run pre-install scripts.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Running pre-install script of %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.
                except:
                    iapmPrintAndLog("An error occurred when *Running pre-install scripts*. Exit now.", 4)
                    go = False
            if stage == 4:
                # Install packages.
                try:
                    iapmPrintAndLog("[4/5] Install packages.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Installing packages %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.
                except:
                    iapmPrintAndLog("An error occurred when *Installing packages*. Exit now.", 4)
                    go = False
            if stage == 5:
                # Do post-install scripts.
                try:
                    iapmPrintAndLog("[5/5] Run post-install scripts.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Running post-install script of %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.
                    go = False
                except:
                    iapmPrintAndLog("An error occurred when *Running post-install scripts*. Exit now.", 4)
                    go = False
    if action == "remove":
        # For remove: 1 - Run pre-remove scripts, 2, Remove packages, 3 - Clean if asked, 4 - Run post-remove scripts.
        while go:
            stage += 1
            if stage == 1:
                # Run pre-remove scripts
                try:
                    iapmPrintAndLog("[1/4] Run pre-remove scripts.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Running pre-remove script of packages %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.(When this, 23:45.)
                except:
                    iapmPrintAndLog("An error occurred when *Running pre-remove scripts*. Exit now.", 4)
                    go = False
            if stage == 2:
                # Remove packages
                try:
                    iapmPrintAndLog("[2/4] Remove packages", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Removing packages %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.
                except:
                    iapmPrintAndLog("An error occurred when *Removing packages*. Exit now.", 4)
            if stage == 3:
                # Clean if asked
                if clean == True:
                    try:
                        iapmPrintAndLog("[3/4] Cleaning.", 1)
                        for i in range(0, len(packages)):
                            targetPackage = packages[i]
                            iapmPrintAndLog("(%d/%d) Cleaning %s." % (i + 1, len(packages), targetPackage))
                            # Not finished.
                    except:
                        iapmPrintAndLog("An error occurred when *Cleaning*. Skipped.", 3)
            if stage == 4:
                # Run post-remove scripts.
                try:
                    iapmPrintAndLog("[4/4] Run post-remove scripts.", 1)
                    for i in range(0, len(packages)):
                        targetPackage = packages[i]
                        iapmPrintAndLog("(%d/%d) Running post-remove scripts %s." % (i + 1, len(packages), targetPackage))
                        # Not finished.
                    go = False
                except:
                    iapmPrintAndLog("An error occurred when *Running post-remove scripts*. Exit now.", 4)
                    go = False
    
    iapmPrintAndLog("Exiting \"iapmDoProcess\".", 6)
            

def iapmPrintAndLog(object, loglevel = 1):
    # There is 7 log level.
    # 1 - INFO; 2 - NOTICE; 3 - WARN; 4 - ERROR; 5 - CRITICAL; 6 - DEBUG; 7 - VERBOSE.
    level = ["INFO", "NOTICE", "WARN", "ERROR", "CRITICAL", "DEBUG", "VERBOSE"]
    # With debug mode and verbose mode off, IAPM will print the log with level 5 at most as default. 
    # If the loglevel is not set, IAPM will use log level 1 as default.
    
    # Make the log and initialize the be-print.
    log = "%s[%s] %s" % (time.strftime('[%Y-%m-%d %H:%M:%S]', time.localtime()), level[loglevel - 1], object)
    bePrint = object
    
    # According the log level to add something to show
    # maybe it had already became a piece of shit. 
    if verbose or (debug and loglevel <= 6):
        # But who cares? lol.
        bePrint = log
    elif loglevel <= 5:
        # That means CRITICAL at most.
        if loglevel >= 3:
            bePrint = "%s: %s" % (level[loglevel - 1], object)
        
    # Color. make it a piece of shit. lol.
    if enable_color:
        if loglevel == 1:
            bePrint = "\033[1;37m%s\033[0m" % bePrint
        if loglevel == 2:
            bePrint = "\033[34m%s\033[0m" % bePrint
        if loglevel == 3:
            bePrint = "\033[33m%s\033[0m" % bePrint
        if loglevel == 4:
            bePrint = "\033[31m%s\033[0m" % bePrint
        if loglevel == 5:
            bePrint = "\033[1;31m%s\033[0m" % bePrint
        if loglevel >= 6:
            bePrint = "\033[38m%s\033[0m" % bePrint
    
    # Print it.
    if loglevel <= 5 or (verbose or (debug and loglevel <=6)): 
        print(bePrint)
    
    # Finally write the log(Not finished)

def main():
    global debug
    global verbose
    global enable_color
    debug = False
    verbose = False
    enable_color = True
    
    # First(Basic) argv check.
    for i in range(1, len(sys.argv)):
        if sys.argv[i] == "--debug":
            print("IAPM is running in debug mode now.")
            debug = True
        if sys.argv[i] == "--verbose" or sys.argv[i] == "-v":
            print("IAPM is running in verbose mode now.")
            verbose = True
    
    # the version of iapm is testing. (HEY THE TRUTH IS THAT I WANT TO TEST THE COLOR LOL ;D)
    iapmPrintAndLog("The version of iapm is testing and not stable.", 3)
    iapmPrintAndLog("The version of iapm is testing and not stable.", 4)
    iapmPrintAndLog("The version of iapm is testing and not stable.", 5)
        
    # (no finish) Get some DIRECTORY from /etc/iapm.conf
    
    
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
#! /usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM main program.

# This part will handle the parameters and configurations in /etc/iapm/iapm.conf
# IAPM will handle these following dictories settings like this: The finnal DataBase Dir it use is $ROOTDIR/$DBDIR instead of $DBDIR.

import sys
import time
import os
import signal
import gettext


def main():
    # Set default configurations.
    rootdir = "/"
    dbdir = "/var/lib/iapm/"
    cachedir = "/var/cache/iapm/"
    logfile = "/var/log/iapm.log"
    lockfile = "/var/lib/iapm/iapm.lock"
    gpgdir = "/etc/iapm/gpg/"

    verbose = False
    color = False
    test = False

    action = None
    targets = []
    options = []

    # Set configurations, according to /etc/iapm.conf, the piece of shit is already fucked up.
    #try:
    #    configfile = open("/etc/iapm/iapm.conf", "r")
    #    for line in configfile:
    #        line = line.strip()
    #        if line.startswith("#") or line == "":
    #            continue
    #        key, value = line.split("=", 1)
    #        key = key.strip()
    #        value = value.strip().strip('"').strip("'")
    #        if key == "ROOTDIR":
    #            rootdir = value
    #        elif key == "DBDIR":
    #            dbdir = value
    #        elif key == "CACHEDIR":
    #            cachedir = value
    #        elif key == "LOGFILE":
    #            logfile = value
    #        elif key == "LOCKFILE":
    #            lockfile = value
    #        elif key == "GPGDIR":
    #            gpgdir = value
    #        elif key == "Verbose":
    #            verbose = value.lower() in ("True")
    #        elif key == "Color":
    #            color = value.lower() in ("True")
    #    configfile.close()
    #except FileNotFoundError:
    #    print("Error: /etc/iapm/iapm.conf not found, can not continue.")
    #    sys.exit(1)
        
    # Check what user want to do. 
    for args in sys.argv[1:]:
        if args.startswith("--") or args.startswith("-"):
            continue
        else:
            action = args
            break

    # Make a list of targets and options.
    for arg in sys.argv[2:]:
        if arg.startswith("--") or arg.startswith("-"):
            options.append(arg)
        else:
            targets.append(arg)
    
    # Finish initialization.
    #if "--sysroot=" in options:
    #    rootdir = options[options.index("--sysroot=")+1] # This pieces of shit is fucked up.
    if "--verbose" in options:
        verbose = True
    if "--test" in options:
        test = True
        print("Notice: You are running IAPM in test mode.")
        print("Notice: Check ~/.iapm/fakeroot")
        os.system("mkdir -p ~/.iapm/fakeroot")
        rootdir = "~/.iapm/fakeroot"
        

    availActions = ["install", "reinstall", "update", "upgrade", "remove", "clean", "autoremove", "version", "search", "info", "help"]
    betaActions = ["autoremove", "search", "info"]  
    permissiveActions = ["install", "reinstall", "update", "upgrade", "remove", "clean", "autoremove"]

    # (Testing) list results.
    if verbose:
        print("Dictionary Settings:")
        print(f"  ROOTDIR: {rootdir}")
        print(f"  DBDIR: {dbdir} ({rootdir}/{dbdir})")
        print(f"  CACHEDIR: {cachedir} ({rootdir}/{cachedir})")
        print(f"  LOGFILE: {logfile} ({rootdir}/{logfile})")
        print(f"  LOCKFILE: {lockfile} ({rootdir}/{lockfile})")
        print(f"  GPGDIR: {gpgdir} ({rootdir}/{gpgdir})")
        print(f"  Verbose: {verbose}")
        print(f"  Color: {color}")
        print(f"  Action: {action}")
        print(f"  Targets: {targets}")
        print(f"  Options: {options}")
        print("Initialization completed.")
        print()

    # Start IAPM main program.(Preparing)
    import iapm
    
    # Check Permissions and if the action is valid.
    if action == None:
        iapm.base.echo("No action specified.", 1)
        sys.exit(1)
    
    if action not in availActions:
        iapm.base.echo(f"Action '{action}' is not available.", 1)
        sys.exit(1)
    
    if action in betaActions:
        iapm.base.echo(f"Action '{action}' is testing.", 2)
    
    isroot = os.geteuid() == 0
    if action in permissiveActions and not isroot and not test:
        iapm.base.echo(f"Action '{action}' needs root permissions. did you run as root?", 1)
        sys.exit(1)
    if test and isroot:
        iapm.base.echo(f"Never test IAPM with root permissions, this may break your system badly.", 1)
        sys.exit(1)
    
    # Make dependency list.
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nError: Interrupted by user. Exiting...")
        sys.exit(1)
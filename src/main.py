#! /usr/bin/env python3

# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM main program.

# This part will handle the parameters and configurations in /etc/iapm/iapm.conf
# IAPM will handle these following dictories settings like this: The finnal DataBase Dir it use is $ROOTDIR/$DBDIR instead of $DBDIR.

import sys
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

    targets = []
    options = []

    # Set configurations, according to /etc/iapm.conf
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
    for args in sys.argv[0:]:
        if args.startswith("--") or args.startswith("-"):
            continue
        else:
            action = args
            break

    # Make a list of targets and options.
    for arg in sys.argv[1:]:
        if arg.startswith("--") or arg.startswith("-"):
            options.append(arg)
        else:
            targets.append(arg)
    
    # Finish initialization.
    if "--sysroot=" in options:
        index = options.index("--sysroot=")
        if index + 1 < len(options):
            rootdir = options[index + 1]
    if "--verbose" in options:
        verbose = True
    

    # (Testing) list results.
    if verbose:
        print("IAPM Initializations:")
        print(f"  ROOTDIR: {rootdir}")
        print(f"  DBDIR: {dbdir}")
        print(f"  CACHEDIR: {cachedir}")
        print(f"  LOGFILE: {logfile}")
        print(f"  LOCKFILE: {lockfile}")
        print(f"  GPGDIR: {gpgdir}")
        print(f"  Verbose: {verbose}")
        print(f"  Color: {color}")
        print(f"  Action: {action}")
        print("Initialization completed.")

    # Start IAPM main program.(Preparing)
    import iapm
    iapm.echo("IAPM is starting...", 7)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nError: Interrupted by user. Exiting...")
        sys.exit(1)
#! /usr/bin/env python3
# Copyright (c) 2025 PLAYThe218 <playthe218@icloud.com>
#
# This software is licensed under the BSD 3-Clause License.
# For the full copyright and license information, please view the LICENSE
# file that was distributed with this source code.

# The IAPM initialization.
# This will handle the parameters and configurations in /etc/iapm/iapm.conf, and then send them to the main IAPM programs.
# Priority: User parameters > Profile > Default
# IAPM will handle these following dictories settings like this: The finnal DataBase Dir it use is $ROOTDIR/$DBDIR instead of $DBDIR.

import sys
import time
import os
import signal


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

    # Set configurations, according to /etc/iapm.conf
    try:
        configfile = open("/etc/iapm/iapm.conf", "r")
        for line in configfile:
            line = line.strip()
            if line.startswith("#") or line == "":
                continue
            key, value = line.split("=", 1)
            key = key.strip()
            value = value.strip().strip('"').strip("'")
            if key == "ROOTDIR":
                rootdir = value
            elif key == "DBDIR":
                dbdir = value
            elif key == "CACHEDIR":
                cachedir = value
            elif key == "LOGFILE":
                logfile = value
            elif key == "LOCKFILE":
                lockfile = value
            elif key == "GPGDIR":
                gpgdir = value
            elif key == "Verbose":
                verbose = value.lower() in ("True")
            elif key == "Color":
                color = value.lower() in ("True")
        configfile.close()
    except FileNotFoundError:
        print("Warning: /etc/iapm/iapm.conf not found, using default configurations.")
        print("Warning: In this case, IAPM may fail.")
    
    # Set configurations, according to user parameters.
    for arg in sys.argv[1:]:
        if arg.startswith("--sysroot="):
            rootdir = arg.split("=", 1)[1]
        if arg == "--verbose":
            verbose = True
    
    # Check what user want to do.
    for args in sys.argv[0:]:
        if args.startswith("--") or args.startswith("-"):
            continue
        else:
            action = args
            break
    
    # (Testing) list results.
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
    
    # Start IAPM main program.
    

if __name__ == "__main__":
    main()
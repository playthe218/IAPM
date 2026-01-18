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
import configparser
import iapm


def main():
    # NEVER change it unless testing.
    configfile = "/etc/iapm/iapm.conf"
    test = False

    action = None
    targets = []
    options = []

    # Set configurations, according to /etc/iapm/iapm.conf, and provide fallback if need.
    try:
        rootdir = iapm.base.readconfig(configfile, "GENERAL:ROOTDIR", "/")
        dbdir = iapm.base.readconfig(configfile, "GENERAL:DBDIR", "/var/lib/iapm/")
        cachedir = iapm.base.readconfig(configfile, "GENERAL:CACHEDIR", "/var/cache/iapm/")
        logfile = iapm.base.readconfig(configfile, "GENERAL:LOGFILE", "/var/log/iapm.log")
        lockfile = iapm.base.readconfig(configfile, "GENERAL:LOCKFILE", "/var/lib/iapm/iapm.lock")
        gpgdir = iapm.base.readconfig(configfile, "GENERAL:GPGDIR", "/etc/iapm/gpg/")
        verbose = iapm.base.readconfig(configfile, "MISCS:Color", False)
        color = iapm.base.readconfig(configfile, "MISCS:Color", True)
    except FileNotFoundError:
        iapm.base.echo("IAPM config file is not found.", 1)
        
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
        iapm.base.echo("You are running IAPM in test mode.", 3)
        iapm.base.echo("We will assume that this IAPM is in its src.", 3)
        iapm.base.echo("Check ~/.iapm/fakeroot", 3)
        os.system("mkdir -p ~/.iapm/fakeroot")
        rootdir = "~/.iapm/fakeroot"
        

    availActions = ["install", "reinstall", "update", "upgrade", "remove", "clean", "autoremove", "version", "search", "info", "help"]
    betaActions = ["autoremove", "search", "info"]  
    permissiveActions = ["install", "reinstall", "update", "upgrade", "remove", "clean", "autoremove"]

    # (Testing) list results.
    if verbose:
        iapm.base.echo(f"Dictionary Settings: {rootdir}", 5)
        iapm.base.echo(f"  ROOTDIR: {rootdir}", 5)
        iapm.base.echo(f"  DBDIR: {dbdir} ({rootdir}/{dbdir})", 5)
        iapm.base.echo(f"  CACHEDIR: {cachedir} ({rootdir}/{cachedir})", 5)
        iapm.base.echo(f"  LOGFILE: {logfile} ({rootdir}/{logfile})", 5)
        iapm.base.echo(f"  LOCKFILE: {lockfile} ({rootdir}/{lockfile})", 5)
        iapm.base.echo(f"  GPGDIR: {gpgdir} ({rootdir}/{gpgdir})", 5)
        iapm.base.echo(f"  Verbose: {verbose}", 5)
        iapm.base.echo(f"  Color: {color}", 5)
        iapm.base.echo(f"  Action: {action}", 5)
        iapm.base.echo(f"  Targets: {targets}", 5)
        iapm.base.echo(f"  Options: {options}", 5)
        iapm.base.echo("Initialization completed.", 5)
        print()

    # Start IAPM main program.(Preparing)
    
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
    
    # Make dependency list.(if action:install)
    if action == "install":
        packages = iapm.extra.addDeps(targets, dbdir)
    

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        iapm.base.echo("Interrupted by user. Exiting...", 1)
        sys.exit(1)
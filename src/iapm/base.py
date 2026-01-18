# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM base modules.

import configparser
import time
import os


def echo(msg, loglevel):
    # Here is a log level list:
    # 0: Critical/Fatal 1: Error 2: Warning 3: Notice 4: Normal 5: Debug 6: Verbose
    
    # An Error, or even worse, always can stop a operation.

    # Critical/Fatal: WORSE than Error, in case of it means errors must to be handled (For example, operation failed when IAPM is working on action:update/install and stage:install, means system is in a inconsistent status).
    # Error: In many failure (eg. may success if change a condition or even try again), Should use Error. (You forget to run as root? lol)
    # Warning: Needs user attention or handling.
    # Notice: Important informations, more important than Normal but not a Warning. (eg. Optional Depends.)
    # Normal: You see it again and again and again and again and again...
    
    # Adding colorful output and log file support in future.
    loglevels = ["Critical", "Error", "Warning", "Notice", "Normal", "Debug", "Verbose"]
    currentTime = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    fullmsg = f"[{currentTime}][{loglevels[loglevel]}]{msg}"
    if loglevel == 4:
        viewmsg = f"{msg}"
    else:
        viewmsg = f"{loglevels[loglevel]}: {msg}"

    print(viewmsg)

def readconfig(file, target, fallback=None):
    config = configparser.ConfigParser()
    config.read(file)
    
    section, option = target.split(":")
    return config.get(section, option, fallback=fallback)
    
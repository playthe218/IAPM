# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM action:help.

# Many thing action:help shows is not finished, but it can describe that what we want to make.

def main():
    print("Usage:")
    print("     iapm [options] <action> ...")

    print("General actions:")
    print("     install                 Install packages")
    print("     update / upgrade        Update installed packages")
    print("     remove                  Remove  packages")
    print("     reinstall               Reinstall packages")
    print("     autoremove              Remove all unused dependency packages")
    print("     clean                   Clean all cached files")
    print("     help                    Show this help and exit")
    print("     version                 Show IAPM version and exit")
    
    print("General options:")
    print("     --debug                 Enable IAPM debug mode")
    print("     --verbose               Enable IAPM verbose mode, provide more information than debug mode")
    print("     --no-confirm            Answer YES on all transaction confirm")
    
    print("Options for action:install")
    print("     --asdeps=[package]      Install packages as depends. By providing a package in this option, IAPM will assume they are Required Depends of the package.")
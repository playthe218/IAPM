# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM action:install.

def main(packages, targets, rootdir, dbdir, cachedir, gpgdir, reposList, color, printlevel):
    # packages: list of packages to install, including targeted pacakges and their dependencies.
    # targets: targeted packages.
    print("These folloing packages will be installed:")
    print("Name                 Version                 Arch                Repo                Size")
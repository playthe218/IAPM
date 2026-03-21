# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM action:install.

import shutil

def main(packages_summary, targets, os_summary, repos_summary):
    # packages: list of packages to install, including targeted pacakges and their dependencies.
    # targets: targeted packages.
    print("These folloing packages will be installed:")
    width = shutil.get_terminal_size().columns
    ROW_FMT = "{:<20} {:<20} {:<20} {:<20} {:<16} {:>10}"
    term_width = shutil.get_terminal_size().columns

    weights = [2, 2, 2, 2, 2, 2]
    total_weight = sum(weights)

    col_widths = [max(8, term_width * w // total_weight) for w in weights]

    diff = term_width - sum(col_widths)
    col_widths[0] += diff

    fmt = " ".join(f"{{:<{w}}}" for w in col_widths)
    ROW_FMT, col_widths = fmt, col_widths
    #                                                                   InstSize
    print(ROW_FMT.format("Name", "Version", "Category", "Arch", "Repo", "Size"))
    # list packages

    # list pkg size
    # B by default, and show MiB
    dlsize = 0
    instsize = 0
    for i in range(len(packages_summary)):
        dlsize += packages_summary[i]["DLSize"]
        instsize += packages_summary[i]["InstSize"]
    dlsize = round(dlsize / 1048576, 1)
    instsize = round(instsize / 1048576, 1)
    print("After this operation:")
    print("%f MiB will be downloaded, %f MiB will be installed." % (dlsize, instsize))
    print("%f MiB will be used in total." % (dlsize + instsize))

    confirmed = False
    while not confirmed:
        # can be better
        print("Would you like to continue?", end=" ")
        confirm = input("[y/N]")
        if confirm in ['y', 'Y', 'yes']:
            confirmed = True
        elif confirm in ['N', 'n', '', 'no']:
            print("Operation aborted.")
            return 0
        else:
            print("Sorry, can't understand \"%s\"." % confirm)
    
    # instsll process

    # if no error happenes, than return 0
    print("Completed!")
    return 0
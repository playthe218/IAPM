# SPDX-License-Identifier: GPL-3.0-or-later
# Copyright (C) 2025-2026 PLAYThe218 <playthe218@icloud.com>

# The IAPM action:install.

import shutil

def main(packages_summary, targets, os_summary, reposlist):
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

    print(ROW_FMT.format("Name", "Version", "Category", "Arch", "Repo", "Size"))
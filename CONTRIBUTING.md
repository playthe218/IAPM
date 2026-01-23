**Language / 语言 :**  [English](CONTRIBUTING.md) | [简体中文](CONTRIBUTING.zh-CN.md)

---
# Contributing Guide

IAPM has been developed slowly due to the fact that only `playthe218` has been maintaining it since its inception (as of January 24, 2026).
We appreciate the contributions from anyone who would like to contribute to IAPM, and we kindly ask that you follow the guidelines outlined below:

## Project Structure

```
IAPM/                       # Sometimes referred to as "SRC://".
|-share/
| |-exampleRepo             # Example repository.
| | |-os.repo               # Example: Software repository for an operating system.
| |-iapm.conf               # IAPM main program configuration file.
| |-repos.conf              # IAPM repository configuration file.
|-src/
| |-iapm/                   # IAPM built-in modules.
| | |-__init__.py
| | |-action.py             # Contains all IAPM actions.
| | |-base.py               # Basic internal functionalities of IAPM.
| | |-extra.py              # Advanced internal functionalities of IAPM.
| |-main.py                 # IAPM main program.
|-test/                     # Contains necessary content for testing IAPM.
| |-example/                # Non-packaged "example" software, useful for testing the mkiap functionality.
| |-repos/                  # Software repositories. Stores sample packages for testing downloads, updates, etc.
|-.gitignore                # Please use this file to ignore unnecessary temporary files.
```

## .iap Package Format

IAPM uses the **`.iap`** package format, <del>which is essentially just a tar file with a changed extension.</del>
Inside the repository, you will find an example `.iap` package structured as follows:

```
example.iap/
|-install/                  # Installation content.
| |-usr/
|   |-bin/
|     |-helloiapm           # A directly executable Python file that outputs "Hello, world!".
|-install_config/           # Installation configuration files.
|-post_install/             # Post-installation scripts.
| |-1_test.sh               # Runs first.
| |-2_test.sh               # Runs second.
|-post_install_imme/        # Immediate post-installation scripts.
| |-...                     # Same as above, omitted for brevity.
|-post_remove/              # Post-removal scripts.
|-post_remove_imme/         # Immediate post-removal scripts.
|-post_update/              # Post-update scripts.
|-post_update_imme/         # Immediate post-update scripts.
|-pre_install/              # Pre-installation scripts.
|-pre_remove/               # Pre-removal scripts.
|-pre_update/               # Pre-update scripts.
|-package.info              # Package metadata.
```

The installation, removal, and update scripts (or their "immediate execution" counterparts) in the `.iap` package are **not language-restricted**, as long as these scripts can be executed with `./xxx`.
For compatibility purposes, please start these scripts with the `#! /usr/bin/env xxx` interpreter declaration. It is recommended to use Shell or Python to write these scripts, as Shell is a standard package in almost all **generally usable Linux distributions**, and Python is a dependency of IAPM.

## Definitions & Terminology

The following terms may be used in the document. They are typically not translated elsewhere in the repository:

* `SRC://` : The root directory of the IAPM source code repository.
* `action` : The target operation of IAPM, typically recognized as the first parameter that does not begin with `--` or `-`. For example, `install`, `remove`, `update`, etc.
* `stage` : The operational stage of IAPM.
* `PR` : A Pull Request.
* `.iap` : The package format used by IAPM.
* `Generally usable Linux distribution` : We define this as a Linux distribution that can be entered via `chroot` and at least contains `coreutils`. We do not guarantee that `busybox` substitutes can fully replace the functionalities IAPM requires.

## Getting Started

1. Fork the repository, then clone your fork.
2. Create a branch, please **do not use `main`, `test`, `dev`, or `NUM.NUM`** (fixed versions):

```bash
git checkout -b xxx
```

3. Make your changes.
4. Commit your changes. To reduce review time, we recommend stating the purpose of the change:

```bash
git commit
```

5. Push the changes to your remote repository:

```bash
git push origin xxx
```

6. Submit a PR.

### PR Format

IAPM is still under development, and we welcome contributions. However, we may not always have the capacity to review all contributions.

To avoid having your PR rejected, you **must clearly state the changes** in your PR. Examples:

```
feature: Add xxx functionality.
fix: Fix xxx bug/issue.
performance: Improve parameter handling performance.
docs: Update README.md.
```

If this is not provided, your PR will likely be **queued last** or **rejected**.

To improve the review priority of your PR, we also recommend specifying the files that have been modified.

### Checks

In general, these checks are not strictly required, but completing them yourself and indicating the results in your PR may **significantly reduce review time**:

* `iapm --test --debug xxx`: `--test` will **skip root permission checks** and **create a fake root directory at `~/.iapm/fakeroot/`**. `--debug` will **show the level of most log information** and **display the time these messages were generated**.
* `iapm --test --verbose xxx`: `--test` behaves the same. `--verbose` will increase the precision of the time points displayed in `--debug` from seconds to **milliseconds**. If your changes improve performance, you can use this command to compare the original and your optimized results, showcasing your improvement.

### Common Reasons for PR Rejection

Here are some common reasons PRs may be rejected. Please avoid these situations:

1. **“Well-meaning” formatting**: Just running `black` on the code and submitting a PR with no other functional, bug-fixing, or optimization-related changes.
2. **Excessive optimization**: Attempting to improve performance or reduce code size (even if it's just removing a single newline) while severely neglecting readability; in the worst cases, such over-optimizations may lead to unreadable code without achieving any performance gains:

   ```python
   for x in range(1, 10):
       for y in range(1, x+1):
           print(str(y)+"x"+str(x)+"="+str(x*y), end=" ")
       print()
   ```

   ```python
   for x in range(1, 10): print(" ".join([str(y)+"x"+str(x)+"="+str(x*y) for y in range(1, x+1)]))
   ```
3. **Importing 100 packages**: Importing a large number of Python packages, including those that are not necessary and typically would not be installed in even the most minimal Linux installations.
4. **Unnecessary features**: Adding features that clearly don't belong in a package manager, such as calling ChatGPT, DeepSeek, or other AI APIs.
5. **Malicious code submissions**: Please do not submit PRs containing malicious code, such as mining programs or anything that could compromise the security of the repository. Any such submission will be immediately rejected.

If we encounter more typical issues or common mistakes in PRs, this section will be updated accordingly.

## License

IAPM has been released under the **GPL-3.0-or-later** license starting from version 3.0. Therefore, any code contributions you make to IAPM will also be released under the **GPL-3.0-or-later** license. By submitting your PR, you agree to this license.
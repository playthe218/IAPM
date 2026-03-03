**Language / 语言:** [English](README.md) | [简体中文](README.zh-CN.md)

---

# IAPM Package Manager 3.0 Dev

IAPM is a package manager under development (not yet completed!)

## Dependencies

If you have a basically usable Linux distribution, then `Python`, `Curl` and `Tar` are the current dependencies. <br>
With future feature updates, the following dependencies are expected to be added: <br>

* GnuPG (for signing and verifying packages)

## Development Progress & Feature List

Here are the completed and unfinished features: <br>

### To release the test version...

* [x] Some basic functionality
* [x] Reworked: Configuration file handling
* [ ] Reworked: Parameter handling
* [ ] Dependency resolution
* [ ] action:instll, action:update/upgrade, action:remove

### To release the stable version...

* [x] action:help
* [ ] Key and package verification

### To make it more usable...

* [ ] action:search, action:info, action:autoremove
* [ ] Clean cache items, auto-remove
* [ ] Very complex advanced dependency resolution system

## Quick Start ##

Although it's not finished yet, you can try the following steps: <br>

1. Clone the repository:

```bash
git clone https://github.com/playthe218/IAPM
```

2. Navigate to the program directory:

```bash
cd IAPM/src
```

3. Run:

```bash
./main.py --test
```

## **Important:** Since IAPM 3.0 is under development, please use `--test` to avoid potential issues with incomplete features breaking the system. <br>

## License

IAPM 3.0 is released under the GPL-3.0-or-later license. For more details, please [refer to the LICENSE file](LICENSE).

# Semi-Server Management Script


## Description

`semiservermgr` tool is used for manual control the power status of remote
"semi-server" (unusual server which isn't 24/7 online and works only few hours
a day)


## Examples

`semiservermgr wu` - wake up on LAN (using `wakeonlan` program)

`semiservermgr sd` - shutdown (using `shutdown` command)

`semiservermgr re` - reboot (using `reboot` command)

`semiservermgr hi` - turn on the hibrenation mode (using `pm-utils`)

`semiservermgr su` - turn on the suspend mode (using `pm-utils`)

`semiservermgr hy` - turn on the hybrid-suspend mode (using `pm-utils`)

`semiservermgr wu -c config.toml` - wake up on LAN using configuration from
`config.toml` in the current directory


## Target Requirements (Server)

1. Install `openssh-server` on target
```
apt-get install openssh-server
```

2. Install `pm-utils` on target
```
apt-get install pm-utils
```


## Client Requirements

1. Install `openssh-client` on client
```
apt-get install openssh-client
```

2. Install `wakeonlan` program on client
```
apt-get install wakeonlan
```

3. Install `toml` package on client
```
pip3 install toml
pip3 install xdg
```

4. Put `config.toml` in the `XDG_CONFIG_HOME/semiservermgr/` directory
   (`/home/user/.config/semiservermgr/`) with following content:
```
[semiservermgr]
# server hostname or ip
host="hostname"
# ssh user with login and execute rights for pm-utils
user="root"
# server MAC address for wakeonlan function
mac="00:00:00:00:00:00"
```

5. Use `semiservermgr --help` to see available commands


## Directory Structure

- [`src/`](src/) - sources

    - [`semiservermgr.py`](src/semiservermgr.py) - main program

- [`deb/`](deb/) - test Debian package directories and files

    - [`make_package.sh`](deb/make_package.sh) - shell script for making
        deb-package

    - [`semiservermgr/usr/local/bin/`](deb/semiservermgr/usr/local/bin) -
    Debian package destination path

    - [`control`](deb/semiservermgr/DEBIAN/control) - Debian package control file

- [`README.md`](README.md) - common information (this file)
- [`LICENSE.md`](LICENSE.md) - license text


## License

semiservermgr is licensed under the MIT license. Please read the license
file in this repository for more information.

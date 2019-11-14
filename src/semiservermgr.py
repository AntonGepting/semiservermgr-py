#!/usr/bin/python3

import argparse
import os
import toml
from xdg import XDG_CONFIG_HOME


PROG_NAME = 'semiservermgr'
PROG_DESC = 'simple semi-server power managment tool'


# class for managing semiserver via ssh or using mac address
class SemiServer:
    def __init__(self, host, mac, user):
        self.set(host, mac, user)

    # set up host variables
    def set(self, host, mac, user):
        self.host = host
        self.mac = mac
        self.user = user
        self.ssh_target = f'ssh -t {self.user}@{self.host}'

    def shutdown(self):
        cmd = f'{self.ssh_target} \'shutdown\''
        self.cmd(cmd)

    def cancel_shutdown(self):
        cmd = f'{self.ssh_target} \'shutdown\' -c'
        self.cmd(cmd)

    def wakeup(self):
        cmd = f'wakeonlan {self.mac}'
        self.cmd(cmd)

    def reboot(self):
        cmd = f'{self.ssh_target} \'reboot\''
        self.cmd(cmd)

    def suspend(self):
        cmd = f'{self.ssh_target} \'pm-suspend\''
        self.cmd(cmd)

    def hibernate(self, args):
        cmd = f'{self.ssh_target} \'pm-hibernate\''
        self.cmd(cmd)

    def suspend_hybrid(self):
        cmd = f'{self.ssh_target} \'pm-suspend-hybrid\''
        self.cmd(cmd)

    def cmd(self, cmd):
        print(f'sending: {cmd}')
        os.system(cmd)


class Cli:

    def __init__(self):

        cfg_file = 'config.toml'
        # default config can be placed in XDG_CONFIG_HOME
        default_cfg_file = os.path.join(XDG_CONFIG_HOME, PROG_NAME, cfg_file)

        # init CLI commmands
        parser = argparse.ArgumentParser(prog=PROG_NAME)
        parser.add_argument('-c', '--cfg', action='store', help='specify \
                custom configuration', type=argparse.FileType('r'),
                default=default_cfg_file)
        subparsers = parser.add_subparsers(help='subcommand help')

        sd = subparsers.add_parser('shutdown', aliases=['sd'], help='shutdown')
        sd.set_defaults(func=self.shutdown)
        sd.add_argument('-c','--cancel', dest='action', action='store_const',
                const=self.cancel_shutdown, help='cancel shutdown')

        wu = subparsers.add_parser('wakeup', aliases=['wu'], help='wakeonlan')
        wu.set_defaults(func=self.wakeup)

        re = subparsers.add_parser('reboot', aliases=['re'], help='reboot')
        re.set_defaults(func=self.reboot)

        su = subparsers.add_parser('suspend', aliases=['su'], help='suspend')
        su.set_defaults(func=self.suspend)

        hi = subparsers.add_parser('hibernate', aliases=['hi'], help='hibernate')
        hi.set_defaults(func=self.hibernate)

        hy = subparsers.add_parser('hybrid', aliases=['hy'], help='suspend-hybrid')
        hy.set_defaults(func=self.suspend_hybrid)
        # parser_a.add_argument('bar', type=int, help='bar help')

        # parse, exec
        args = parser.parse_args()

        # load config (not using callback, because of order of evaluation)
        self.load_cfg(args)

        # init server manager
        self.semiserver = SemiServer(self.host, self.mac, self.user)

        # print(args)
        args.func(args)

    def load_cfg(self, args):
        # load config
        conf = toml.load(args.cfg)

        self.host = conf[PROG_NAME]['host']
        self.user = conf[PROG_NAME]['user']
        self.mac = conf[PROG_NAME]['mac']

    def shutdown(self, args):
        self.semiserver.shutdown()

    def cancel_shutdown(self, args):
        self.semiserver.cancel_shutdown()

    def wakeup(self, args):
        self.semiserver.wakeup()

    def reboot(self, args):
        self.semiserver.reboot()

    def suspend(self, args):
        self.semiserver.suspend()

    def hibernate(self, args):
        self.semiserver.hibernate()

    def suspend_hybrid(self, args):
        self.semiserver.hybrid()


def main():
    cli = Cli()


if __name__ == '__main__':
    main()

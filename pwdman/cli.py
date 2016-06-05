#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: cli.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2016-06-05
"""

import click
from pwdman.core import PwdMan


@click.command()
@click.argument('service')
@click.option('--passphrase', envvar='PWDMAN_PASSPHRASE', prompt=True)
@click.option('--length', envvar='PWDMAN_LENGTH', default=25)
@click.option('--numbers/--no-numbers', default=True)
@click.option('--lowers/--no-lowers', default=True)
@click.option('--uppers/--no-uppers', default=True)
@click.option('--symbols/--no-symbols', default=True)
def cli(service, passphrase, length, numbers, lowers, uppers, symbols):
    pm = PwdMan(
        passphrase, length=length, numbers=numbers, lowers=lowers,
        uppers=uppers, symbols=symbols)
    print(pm.generate_password(service))


if __name__ == '__main__':
    cli()

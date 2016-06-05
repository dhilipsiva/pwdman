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
from json import dumps, loads
from hashlib import md5
from getpass import getuser
from Crypto.Cipher import AES
from os.path import expanduser, isfile
from pwdman.core import PwdMan

VERSION = "1"
SETUP_MESSAGE = """
Setup Done!
Please add these dollowing lines in your `.bashrc` or `.bash_profile`

export PWDMAN_SALT=%(salt)s
expoer PWDMAN_PATH=%(path)s

Be sure to open a new terminal - to load new ENV variables.

Example: To generate password for GitHub, Type:

`pwdman github`

"""


def save_config(salt, path, config):
    salt_md5 = md5(salt.encode()).hexdigest()
    obj = AES.new(
        salt_md5, AES.MODE_CTR, counter=lambda: salt_md5[:16].encode())
    message = dumps(config)
    ciphertext = obj.encrypt(message)
    with open(path, 'wb') as config_file:
        config_file.write(ciphertext)
    return ciphertext


def read_config(salt, path):
    salt_md5 = md5(salt.encode()).hexdigest()
    obj = AES.new(
        salt_md5, AES.MODE_CTR, counter=lambda: salt_md5[:16].encode())
    with open(path, 'rb') as config_file:
        data = obj.decrypt(config_file.read())
    return loads(data.decode())


def get_kwargs(config, service, length, numbers, lowers, uppers, symbols):
    s = config["services"].get(service)
    passphrase = config["passphrase"]
    if s is None:
        if length is None:
            length = 25
        if numbers is None:
            numbers = True
        if lowers is None:
            lowers = True
        if uppers is None:
            uppers = True
        if symbols is None:
            symbols = True
    else:
        if length is None:
            length = s["length"]
        if numbers is None:
            numbers = s["numbers"]
        if lowers is None:
            lowers = s["lowers"]
        if uppers is None:
            uppers = s["uppers"]
        if symbols is None:
            symbols = s["symbols"]

    return dict(
        passphrase=passphrase, length=length, numbers=numbers, lowers=lowers,
        uppers=uppers, symbols=symbols)


@click.command()
@click.argument('service')
@click.option('--salt', envvar='PWDMAN_SALT', type=str, default=getuser)
@click.option('--path', envvar='PWDMAN_PATH', type=str, default="~/pwdman")
@click.option('--length', type=int, default=None)
@click.option('--numbers/--no-numbers', default=None)
@click.option('--lowers/--no-lowers', default=None)
@click.option('--uppers/--no-uppers', default=None)
@click.option('--symbols/--no-symbols', default=None)
def cli(service, salt, path, length, numbers, lowers, uppers, symbols):
    path = expanduser(path)
    config = read_config(salt, path)
    kwargs = get_kwargs(
        config, service, length, numbers, lowers, uppers, symbols)
    pm = PwdMan(**kwargs)
    print(pm.generate_password(service))
    config["services"][service] = kwargs
    save_config(salt, path, config)


@click.command()
@click.option('--salt', envvar='PWDMAN_SALT', type=str, default=getuser)
@click.option('--path', envvar='PWDMAN_PATH', type=str, default="~/pwdman")
@click.option('--passphrase', type=str, prompt=True)
def setup(salt, path, passphrase):
    path = expanduser(path)
    if isfile(path):
        print("Setup Already Done!")
    else:
        config = dict(passphrase=passphrase, services={}, version=VERSION)
        save_config(salt, path, config)
        print(SETUP_MESSAGE % locals())

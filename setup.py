#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: setup.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2016-06-05
"""

from setuptools import setup, find_packages

setup(
    name='pwdman',
    version='0.2',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click',
        'pycrypto',
    ],
    entry_points='''
        [console_scripts]
        pwdman=pwdman.cli:cli
        pwdman-setup=pwdman.cli:setup
    ''',
)

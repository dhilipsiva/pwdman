#! /usr/bin/env python
# -*- coding: utf-8 -*-
#
# vim: fenc=utf-8
# vim: tabstop=4 expandtab shiftwidth=4 softtabstop=4
#
#

"""
File name: core.py
Author: dhilipsiva <dhilipsiva@gmail.com>
Date created: 2016-06-04
"""

from hashlib import md5
from itertools import cycle

NUMBERS = list("0123456789")
LETTERS_LOWER = list("abcdefghijklmnopqrstuvwxyz")
LETTERS_UPPER = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
SYMBOLS = list("~@#^&*()_+{|}:<>?-[];,.")


def _get_numerical_digest(text):
    text = text.encode()
    hex_digest = md5(text).hexdigest()
    list_digest = list(hex_digest)

    numerical_digest = []
    for element in list_digest:
        numerical_digest.append(int(element, 16))
    return numerical_digest


class PwdMan(object):
    def __init__(
            self, passphrase, length=25, numbers=True, lowers=True,
            uppers=True, symbols=True):

        self.true_count = list(locals().values()).count(True)
        self.min_count = int(length/self.true_count)
        self.allowed = []
        self.pwd = ""
        self.passphrase = passphrase
        self.length = length
        self.numbers = numbers
        self.lowers = lowers
        self.uppers = uppers
        self.symbols = symbols

    def password_segment(self, allowed, length=None):
        self.allowed += allowed
        length = length or self.min_count
        text = self.passphrase + self.service + str(length) + "".join(allowed)
        numerical_digest = _get_numerical_digest(text)
        cycler_digest = cycle(numerical_digest)
        cycler_allowed = cycle(allowed)
        segment = ""
        for l in range(length):
            letter = next(cycler_allowed)
            num = next(cycler_digest)
            for n in range(num):
                letter = next(cycler_allowed)
            segment += letter

        self.pwd += segment

    def shuffle_password(self):
        new_pwd = []
        old_pwd = list(self.pwd)
        numerical_digest = _get_numerical_digest(self.pwd)
        cycler_numerical = cycle(numerical_digest)
        for l in range(self.length):
            num = next(cycler_numerical)
            cycler_digest = cycle(old_pwd)
            letter = next(cycler_digest)
            for n in range(num):
                letter = next(cycler_digest)
            new_pwd.append(old_pwd.pop(old_pwd.index(letter)))
        self.pwd = "".join(new_pwd)

    def generate_password(self, service):
        self.pwd = ""
        self.service = service

        # Filters
        if self.numbers:
            self.password_segment(NUMBERS)
        if self.lowers:
            self.password_segment(LETTERS_LOWER)
        if self.uppers:
            self.password_segment(LETTERS_UPPER)
        if self.symbols:
            self.password_segment(SYMBOLS)

        count_remaining = self.length - (self.min_count * self.true_count)
        self.password_segment(self.allowed, count_remaining)

        self.shuffle_password()

        return self.pwd

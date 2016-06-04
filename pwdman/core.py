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

from md5 import md5
from itertools import cycle

NUMBERS = list("0123456789")
LETTERS_LOWER = list("abcdefghijklmnopqrstuvwxyz")
LETTERS_UPPER = list("ABCDEFGHIJKLMNOPQRSTUVWXYZ")
SYMBOLS = list("~@#$%^&*()_+{|}:<>?-=[];,.")
SPACE = list(" ")
PASSWORD_LENGTH = 25

ALLOWED = NUMBERS + LETTERS_LOWER + LETTERS_UPPER + SYMBOLS + SPACE

PASS_PHRASE = "test1234"
SERVICE = "facebook"
digest = PASS_PHRASE + SERVICE + str(PASSWORD_LENGTH) + "".join(ALLOWED)
digest = md5(digest).hexdigest()
digest = list(digest)
numerical_digest = []


for element in digest:
    numerical_digest.append(int(element, 16))

cycler_allowed = cycle(ALLOWED)
cycler_digest = cycle(numerical_digest)

pwd = ""

for l in range(PASSWORD_LENGTH):
    letter = ""
    num = next(cycler_digest)
    for n in range(num):
        letter = next(cycler_allowed)
    pwd += letter

print(pwd)

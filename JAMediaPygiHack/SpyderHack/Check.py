#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

retorno = True

def check(item):

    try:
        modulo = __import__("%s" % item)
    except:
        retorno = False

check(sys.argv[1])

print retorno

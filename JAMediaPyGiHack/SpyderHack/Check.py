#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def check(item):

    try:
        modulo = __import__("%s" % item)
        return True
    
    except:
        return False

print check(sys.argv[1])

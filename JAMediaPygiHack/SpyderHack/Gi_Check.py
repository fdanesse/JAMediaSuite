#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

def check(item):
    
    try:
        pygi = __import__("gi.repository")
        modulo = pygi.module.IntrospectionModule(item)
        return True
    
    except:
        return False
    
print check(sys.argv[1])

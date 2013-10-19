#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

retorno = True

def check(item):
    
    try:
        pygi = __import__("gi.repository")
        modulo = pygi.module.IntrospectionModule(item)
        retorno = True
    
    except:
        retorno = False
    
check(sys.argv[1])

print retorno

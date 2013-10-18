#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pydoc

BASEPATH = os.path.dirname(__file__)
os.chdir(BASEPATH)

def get_modulo(modulo, attrib):

    mod = __import__(modulo)
    clase = getattr(mod, attrib)

    archivo = os.path.join(BASEPATH, '%s.html' % attrib)
    ar = open(archivo, "w")
    ar.write("")
    ar.close()
    
    try:
        pydoc.writedoc(clase)
    except:
        pass
    
    if modulo == 'os' and attrib == 'path':
        attrib = 'posixpath'
        
    return os.path.join(BASEPATH, '%s.html' % attrib)

print get_modulo(sys.argv[1], sys.argv[2])
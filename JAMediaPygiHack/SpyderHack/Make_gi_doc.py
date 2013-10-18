#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import pydoc

BASEPATH = os.path.dirname(__file__)
os.chdir(BASEPATH)

def get_modulo(modulo, attrib):
    #pygi = __import__("gi.repository")
    #modulo = pygi.module.IntrospectionModule(modulo_name)

    mod = __import__("%s.%s" % ("gi.repository", modulo))
    new = mod.importer.modules.get(modulo)
    clase = getattr(new, attrib)

    archivo = os.path.join(BASEPATH, '%s.html' % attrib)
    ar = open(archivo, "w")
    ar.write("")
    ar.close()
    
    try:
        pydoc.writedoc(clase)
    except:
        pass
    
    return os.path.join(BASEPATH, '%s.html' % attrib)

print get_modulo(sys.argv[1], sys.argv[2])
#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Dir_Modulo_gi.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
Caso:
    from gi.repository import Gtk, Gdk, otros . . .
"""

import os
import sys
import shelve

path = os.path.join("/dev/shm", "shelvein")

try:
    base_key = sys.argv[1]
    attrib = sys.argv[2]
    
except:
    sys.exit(0)
    
try:
    dict = {
        "lista": [],
        "doc": "",
        "path": "",
        }

    mod = __import__("%s.%s" % ("gi.repository", attrib)) # __import__("%s.%s" % ("gi.repository", name))

    dict["lista"] = dir(mod.importer.modules.get(attrib))

    try:
        dict["doc"] = mod.__doc__
        dict["path"] = mod.__path__
        
    except:
        pass

    modulos = shelve.open(path)
    if not modulos.get(base_key, False):
        modulos[base_key] = {}
    
    key_dict = {}
    for key in modulos[base_key].keys():
        key_dict[key] = modulos[base_key][key]
        
    key_dict[attrib] = dict
    modulos[base_key] = key_dict
    modulos.close()
    
except:
    print "Dir_Modulo_gi: No se pudo importar: %s\n" % attrib
    sys.exit(0)
    
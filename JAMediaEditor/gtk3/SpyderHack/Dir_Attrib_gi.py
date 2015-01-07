#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Dynamic_Cero_Run.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
Caso:
    from gi.repository.Gtk import Window
"""

import os
import sys
import shelve

path = os.path.join("/dev/shm", "shelvein")

try:
    base_key = sys.argv[1]
    modulo = sys.argv[2]
    attrib = sys.argv[3]
    
except:
    #print "sys.argv[3] no existe en Dir_Attrib"
    sys.exit(0)

dict = {
    "lista": [],
    "doc": "",
    "path": "",
    }
    
try:
    mod = __import__("%s.%s" % ("gi.repository", modulo))
    new = mod.importer.modules.get(modulo)
    clase = getattr(new, attrib)

    dict["lista"] = dir(clase)

    try:
        dict["doc"] = clase.__doc__
        dict["path"] = clase.__path__
        
    except:
        pass

    modulos = shelve.open(path)
    if not modulos.get(base_key, False):
        modulos[base_key] = {}

    key_dict = {}
    for key in modulos[base_key].keys():
        key_dict[key] = modulos[base_key][key]
        
    key_dict[attrib] = dict                       ### attrib
    modulos[base_key] = key_dict
    modulos.close()
    
except:
    print "Dir_Attrib_gi: No se pudo importar: %s\n" % attrib
    sys.exit(0)
    
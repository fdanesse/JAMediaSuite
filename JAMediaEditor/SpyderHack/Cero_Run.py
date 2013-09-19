#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Cero_Run.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
Caso:
    from gi.repository import Gtk, Gdk, otros . . .
"""

import os
import sys
import shelve

arch = open("/tmp/JAMediaEditorLogCero_Run.txt", "w") ### LOG

path = os.path.join(sys.argv[1])
imports = sys.argv[2:]

modulos = shelve.open(path)

temp_list = imports
prev = temp_list[1]
mod_temp_list = temp_list[3:]

for name in mod_temp_list:
    name = name.replace(",", "").strip()
    
    try:
        dict = {
            "lista": [],
            "doc": "",
            "path": "",
            }
        
        mod = __import__("%s.%s" % (prev, name))            # __import__("%s.%s" % ("gi.repository", name))
        arch.write("Módulo Importado: %s\n" % str(mod))
        
        dict["lista"] = dir(mod.importer.modules.get(name))
        
        try:
            dict["doc"] = mod.__doc__
            dict["path"] = mod.__path__
            
        except:
            pass
        
        modulos[name] = dict
        
    except:
        arch.write("\t\tNo se pudo Cargar: %s\n" % str(mod))
        
arch.close()
modulos.close()

print "OK"

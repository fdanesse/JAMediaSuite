#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Dynamic_Cero_Run.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
Caso:
    El usuario ha escrito:
        Gtk.Window.
"""

import os
import sys
import shelve

arch = open("/tmp/JAMediaEditorLogDynamic_Cero_Run.txt", "w") ### LOG

path = os.path.join(sys.argv[1])
expresion = sys.argv[2]

arch.write("Caso: %s\n" % (expresion))

prevs = expresion.split(".")
modulos = shelve.open(path)

arch.write("Prevs: %s\n" % (prevs))

if len(prevs) == 2:
    mod_prev = prevs[0].strip()
    prev = prevs[1].strip()
    
    arch.write("Prev in Lista: %s\n" % (prev))
    
    try:
        dict = {
            "lista": [],
            "doc": "",
            "path": "",
            }
            
        mod = __import__("%s.%s" % ("gi.repository", mod_prev))
        arch.write("Modulo: %s\n" % str(mod))
        
        new = mod.importer.modules.get(mod_prev)
        arch.write("Modulo: %s\n" % str(new))
        
        clase = getattr(new, prev)
        arch.write("Clase: %s\n" % str(clase))
        
        dict["lista"] = dir(clase)
        
        try:
            dict["doc"] = clase.__doc__
            dict["path"] = clase.__path__
            
        except:
            pass
        
        modulos[expresion] = dict
        
    except:
        arch.write("\t\tNo se pudo Cargar: %s\n" % str(mod))
        
else:
    arch.write("Caso no previsto o no encontrado: %s\n" % (expresion))

modulos.close()
arch.close()

print "OK"
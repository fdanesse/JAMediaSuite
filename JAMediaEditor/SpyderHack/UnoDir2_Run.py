#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   DosDir2_Run.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
    ¡¡ Sólo para Importar Clases !!
    
    mod = __import__("%s" % modulo)
    attr_name = getattr(mod, name)
    
Casos:
    from JAMedia.JAMedia import JAMediaPlayer, otros . . .
    
    FIXME:
        No funciona en casos donde se importa algo que se encuentra
        en un directorio superior, por ejemplo, si tenemos la estructura
        de directorios:
            
            JAMediaObjetcs/
                ...
            JAMedia/
                Widgets.py
                
        Si en Widgets.py dice: import JAMediaObjetcs, SpyderHack falla.
"""

import os
import sys
import shelve

MIPATH = os.path.dirname(__file__)

arch = open("/tmp/JAMediaEditorLogUnoDir2_Run.txt", "w") ### LOG

path = os.path.join(sys.argv[1])
modulo = sys.argv[2]
imports = sys.argv[3:]

arch.write("Intentando importar: %s de %s en: %s\n" % (imports, modulo , MIPATH))

os.chdir(os.path.join(MIPATH))

modulos = shelve.open(path)

for item in imports:
    name = item.replace(",", "").replace("[", "").replace("]", "").strip()
    
    arch.write("Intentando importar: %s en: %s/%s.py\n" % (name, MIPATH, modulo))
    
    modulos[name] = []
    
    try:
        dict = {
            "lista": [],
            "doc": "",
            "path": "",
            }
            
        mod = __import__("%s" % modulo)
        arch.write("Se importó: %s\n" % modulo)
        
        attr_name = getattr(mod, name)
        
        #for n in dir(attr_name):
        #    if not n.endswith("__"):
        #        dict["lista"].append(n)
        
        dict["lista"] = dir(attr_name)
        
        arch.write("Se importó Atributo: %s\n" % name)
        
        try:
            dict["doc"] = mod.__doc__
            dict["path"] = mod.__file__
            
        except:
            pass
        
        modulos[name] = dict
        
    except:
        arch.write("\t\tNo se pudo importar: %s\n" % name)
    
modulos.close()
arch.close()

print "OK"

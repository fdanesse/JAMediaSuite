#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   UnoDir_Run.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
    ¡¡ Sólo para Importar módulos !!
    
Casos:
    from JAMediaObjects.JAMediaGstreamer import JAMediaBins, otros . . .
    
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

arch = open("/tmp/JAMediaEditorLogUnoDir_Run.txt", "w") ### LOG

path = os.path.join(sys.argv[1])
imports = sys.argv[2:]

os.chdir(os.path.join(MIPATH))

modulos = shelve.open(path)

for item in imports:
    name = item.replace(",", "").replace("[", "").replace("]", "").strip()
    
    arch.write("Intentando importar: %s en: %s\n" % (name, MIPATH))
    modulos[name] = []
    
    try:
        dict = {
            "lista": [],
            "doc": "",
            "path": "",
            }
            
        mod = __import__("%s" % name)
        arch.write("Se importó: %s\n" % name)
        
        ### Modo 1
        """
        dict["lista"] = dir(mod)
        
        try:
            dict["doc"] = mod.__doc__
            dict["path"] = mod.__file__
            
        except:
            pass
        
        modulos[name] = dict
        """
        
        ### Modo 2
        for func in dir(mod):
            try:
                attr_name = getattr(mod, func).__name__
                dict["lista"].append(attr_name)
                
            except:
                """
                Quita:
                    __builtins__
                    __doc__
                    __file__
                    __name__
                    __package__
                """
                #arch.write("\t\tNo se pudo leer: %s\n" % (str(func)))
                pass
            
        try:
            dict["doc"] = mod.__doc__
            dict["path"] = mod.__file__
            
        except:
            pass
        
        modulos[name] = dict
        
    except:
        arch.write("\t\tNo se pudo importar: %s\n" % name)
    
arch.close()
modulos.close()

print "OK"

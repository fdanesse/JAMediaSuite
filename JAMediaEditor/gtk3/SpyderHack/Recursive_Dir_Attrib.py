#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Recursive_Dir_Attrib.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
    ¡¡ Sólo para Importar Clases !!
    
    mod = __import__("%s" % modulo)
    attr_name = getattr(mod, name)
    
    mod = __import__("%s" % prev)
    modulo = mod.__getattribute__(str(prev.split(".")[-1]))
    modulos_name = modulo.__getattribute__(name)
    #arch.write("\t1- Se importó: %s\n" % (str(modulos_name)))
    
    for func in dir(modulos_name):
        try:
            attr_name = getattr(modulos_name, func).__name__
            if not "GObjectMeta" in attr_name and not attr_name.endswith("__"):
                modulos[name].append(attr_name)
                #arch.write("\t1- Se importó: %s\n" % getattr(modulos_name, func).__name__)
            
        except:
            #arch.write("\t\t1- No se pudo importar: %s %s %s\n" % (str(prev), str(name), str(func)))
            # FIXME: casos como: JAMedia.JAMedia JAMediaPlayer __dict__
            pass
    
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

path = os.path.join("/dev/shm", "shelvein")

try:
    base_key = sys.argv[1]
    modulo1 = sys.argv[2] # gtk.gdk
    modulo2 = sys.argv[3] # gdk
    modulo3 = sys.argv[4] # Color

except:
    sys.exit(0)
    
if MIPATH:
    if os.path.exists(MIPATH):
        os.chdir(os.path.join(MIPATH))

dict = {
"lista": [],
"doc": "",
"path": "",
}

try:
    mod = __import__("%s.%s" % (modulo1, modulo2))
    modulo = mod.__getattribute__(modulo2)
    attr_name = modulo.__getattribute__(modulo3)

    dict["lista"] = dir(attr_name)

    try:
        dict["doc"] = attr_name.__doc__
        dict["path"] = attr_name.__file__
        
    except:
        pass

    modulos = shelve.open(path)
    if not modulos.get(base_key, False):
        modulos[base_key] = {}

    key_dict = {}
    for key in modulos[base_key].keys():
        key_dict[key] = modulos[base_key][key]
        
    key_dict["%s.%s.%s" % (modulo1, modulo2, modulo3)] = dict

    modulos[base_key] = key_dict
    modulos.close()
    
except:
    print "Recursive_Dir_Attrib: No se pudo importar: %s %s %s\n" % (modulo1, modulo2, modulo3)
    sys.exit(0)
    
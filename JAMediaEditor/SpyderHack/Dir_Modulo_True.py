#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Dir_Modulo_True.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
    ¡¡ Sólo para Importar módulos del Usuario!!
    
Casos:
    import JAMedia
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

path = os.path.join("/dev/shm", "shelvein")

try:
    base_key = sys.argv[1]
    name = sys.argv[2]
    
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
    mod = __import__("%s" % name)
    
    #dict["lista"] = dir(mod)
    
    for n in dir(mod):
        if not n.endswith("__"):
            dict["lista"].append(n)
            
    '''
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
            pass'''
        
    try:
        dict["doc"] = mod.__doc__
        dict["path"] = mod.__file__
        
    except:
        pass
    
    modulos = shelve.open(path)
    if not modulos.get(base_key, False):
        modulos[base_key] = {}
    
    key_dict = {}
    for key in modulos[base_key].keys():
        key_dict[key] = modulos[base_key][key]
        
    key_dict[name] = dict
    modulos[base_key] = key_dict
    modulos.close()
    
except:
    print "Dir_Modulo_True: No se pudo importar: %s\n" % name
    sys.exit(0)

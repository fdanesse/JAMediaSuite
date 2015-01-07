#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Dir_Attrib_True.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
    ¡¡ Sólo para Importar Modulos del Usuario desde un path
    o Clases en um módulo del Usuario !!
    
    mod = __import__("%s" % modulo)
    attr_name = getattr(mod, name)
    
Casos:
    import JAMedia.Widgets
    from JAMedia.JAMedia import JAMediaPlayer
    
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
    modulo = sys.argv[2]
    name = sys.argv[3]
    
except:
    #print "sys.argv[3] no existe en Dir_Attrib"
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
    mod = __import__("%s" % modulo)

    attr_name = getattr(mod, name)
    
    for n in dir(attr_name):
        if not n.endswith("__"):
            dict["lista"].append(n)

    #dict["lista"] = dir(attr_name)
    
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
        
    key_dict["import"] = dict
    modulos[base_key] = key_dict
    modulos.close()
    
except:
    print "Dir_Attrib_True: No se pudo importar: %s\n" % name
    sys.exit(0)
    
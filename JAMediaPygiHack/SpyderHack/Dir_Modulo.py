#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Dir_Modulo.py por:
#       Flavio Danesse <fdanesse@activitycentral.com>
#       ActivityCentral

"""
    ¡¡ Sólo para Importar módulos del "Sistema"!!
Casos:
    import os, sys, commands
"""

import os
import sys
import shelve
import types

path = os.path.join("/dev/shm", "shelvein")

name = sys.argv[1]

PATH = ""
CONSTANTES = []
DESCONOCIDOS = []
FUNCIONES = []
CLASES = []

modulo = False

try:
    modulo = __import__("%s" % name)
except:
    pass
    
if modulo:
    try:
        PATH = modulo.__path__
    except:
        pass
    
    if not PATH:
        try:
            PATH = modulo.__file__
        except:
            pass

    for func in dir(modulo):
        if func.startswith("__") and func.endswith("__"):
            continue
        
        else:
            objeto = "%s.%s" % (name, func)
            attr = False
            gdoc = ''
            
            try:
                attr = getattr(modulo, func)
                
            except:
                DESCONOCIDOS.append( (objeto, func, dir(func), str(type(func))) )
                continue
        
            if isinstance(attr, type):
                try:
                    gdoc = attr.__gdoc__
                except:
                    pass
                
                CLASES.append( (objeto, gdoc, dir(attr), str(type(attr))) )
                continue
                
            elif isinstance(attr, types.FunctionType) or \
                isinstance(attr, types.BuiltinFunctionType) or \
                isinstance(attr, types.BuiltinMethodType) or \
                isinstance(attr, types.MethodType):
                    FUNCIONES.append( (objeto, '', dir(attr), str(type(attr))) )
                    continue
            
            else:
                if not type(attr) == types.ModuleType:
                    CONSTANTES.append( (objeto, '', dir(attr), str(type(attr))) )
                    continue
                
                else:
                    # FIXME: hurgar aquí.
                    #print type(attr), attr
                    #mod = __import__("%s.%s" % (name, func))
                    #new = mod.__getattribute__(func)
                    #print "\t***", "%s.%s" % (name, func), func
                    #print dir(new)
                    pass
                    
modulos = shelve.open(path)
dict = {
    'CLASES':CLASES,
    'FUNCIONES':FUNCIONES,
    'CONSTANTES':CONSTANTES,
    'DESCONOCIDOS':DESCONOCIDOS,
    'PATH':PATH,
    }
for key in dict.keys():
    modulos[key]= dict[key]
modulos.close()

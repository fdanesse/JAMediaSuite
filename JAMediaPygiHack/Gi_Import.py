#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Gi_Import.py por:
#       Flavio Danesse <fdanesse@gmail.com>, <fdanesse@activitycentral.com>
#       CeibalJAM - Uruguay - Activity Central

# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

import types

pygi = __import__("gi.repository")

def get_info(modulo_name):
    """
    Devuelve las clases, funciones y constantes de
    un modulo determinado en un paquete dado.
    """
    
    PATH = ""
    CONSTANTES = []
    DESCONOCIDOS = []
    FUNCIONES = []
    CLASES = []
    
    modulo = False
    
    try:
        modulo = pygi.module.IntrospectionModule(modulo_name)
        
    except:
        return [False, False, False, False, False]
    
    if not modulo:
        return [False, False, False, False, False]

    PATH = dir(modulo)
    
    for func in dir(modulo):
        if func.startswith("__") and func.endswith("__"):
            """
            Funciones de módulo:
                __class__
                __delattr__
                __dict__
                __dir__
                __doc__
                __format__
                __getattr__
                __getattribute__
                __hash__
                __init__
                __module__
                __name__
                __new__
                __path__
                __reduce__
                __reduce_ex__
                __repr__
                __setattr__
                __sizeof__
                __str__
                __subclasshook__
                __weakref__
                """
            continue
        
        else:
            objeto = "%s.%s" % (modulo_name, func)
            attr = False
            gdoc = ''
            
            try:
                attr = getattr(modulo, func)
                
            except:
                DESCONOCIDOS.append( (objeto, func, '', str(type(func))) )
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
                    print type(attr), attr
                    
    return [CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS, PATH]

if __name__=="__main__":
    import sys
    get_info(sys.argv[1])
    
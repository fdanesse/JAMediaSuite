#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   gtkintrospection.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   ActivityCentran

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

import os
import sys
import shelve

### Obtener los datos para hacer autocompletado.
path = os.path.join(sys.argv[1])

archivo = shelve.open(path)
lista = archivo["Lista"]
archivo.close()

imports = lista[:-1]
linea_activa = lista[-1]

### Hacer importaciones previas.
modulos = {}

def append_modulo(name):
    """
    Importa un módulo según su nombre y lo
    almacena importado.
    """
    
    # FIXME: Requiere analisis con mayor detenimiento.
    try:
        if not modulos.get(name, ""):
            modulos[name] = __import__(name)
            
    except:
        arch = open("/dev/shm/log", "w")
        arch.write(name)
        arch.close()
    
def append_modulo_to_prev(name, prev):
    """
    Importa un módulo que se encuentra dentro de
    un paquete, según su nombre y el nombre
    del paquete que lo contiene y lo almacena importado.
    """
    
    # FIXME: Requiere analisis con mayor detenimiento.
    try:
        if not modulos.get(prev, ""):
            append_modulo(prev)
            
        modulos[name] = modulos[prev].__getattribute__(name)
        
    except:
        pass
    
def append_modulo_to_prev_for_path(path):
    """
    Importa los módulos necesarios segun path y lo almacena.
    """
    
    # FIXME: Requiere analisis con mayor detenimiento.
    try:
        # FIXME: Esta función Falla con tipos from modulo1.modulo2.modulo3 import modulo4
        items = path.split(".")

        contador = 0
        prev = items[0]
        
        for item in items:
            contador += 1
            
            if not contador == len(items):
                dos = items[contador]
                prev = "%s.%s" % (prev, items[contador])
                
                mod = __import__(prev).__dict__[dos]
                
                if not modulos.get(prev, ""):
                    modulos[prev] = mod
                    
    except:
        pass
    
for im in imports:
    
    ### Caso 1: import os
    ### Caso Especial: import os, sys, ...
    if not "from " in im and not " *" in im and not " as" in im:
        temp_list = im.split()[1:]          # quitando "import" y separando los módulos.
        
        for item in temp_list:
            name = item.replace(",", "")    # quitando ",".
            append_modulo(name)             # importar y almacenar.
            
    ### Caso 1: import os
    ### Caso Especial: from os import *
    elif "from " in im and " *" in im and not " as" in im:
        pass
    
    ### Caso 2: from os import path
    ### Caso Especial: from os import path, chmod, ...
    elif "from " in im and not " *" in im and not "." in im and not " as" in im:
        temp_list = im.split()
        prev = temp_list[1]
        temp_list = temp_list[3:]
        
        for item in temp_list:
            name = item.replace(",", "")
            append_modulo_to_prev(name, prev)
            
    ### Caso 2: from os import path
    ### Caso Especial: from os import *
    elif "from " in im and " *" in im and not "." in im and not " as" in im:
        pass # http://stackoverflow.com/questions/2916374/how-to-import-with-import
        
    ### caso 3: from Coso.Ventana import JAMediaPlayer
    ### Caso Especial: from Coso.Ventana.Otro import JAMediaPlayer, OtraCosa, ...
    elif "from " in im and not " *" in im and "." in im and not " as" in im:
        temp_list = im.split()
        prev = temp_list[1]
        mod_temp_list = temp_list[3:]
        
        if len(prev.split(".")) < 3: # FIXME la funcion falla para caso especial
            ### Caso Especial: módulos de pygi.
            if "gi.repository" in prev:
                name = mod_temp_list[0]
                mod = __import__("%s.%s" % (prev, name))
                modulos[name] = mod.importer.modules.get(name)
                
            else:
                append_modulo_to_prev_for_path(prev)
                
                for item in mod_temp_list:
                    name = item.replace(",", "")
                    append_modulo_to_prev(name, prev)

### Importar el o los modulos sobre los que se está haciendo auto completado.
lista = []

# FIXME: Requiere análisis de casos especiales.
if len(linea_activa) == 1:
    name = linea_activa[0]
    #append_modulo(name)

    lista = dir(modulos[name])
    #print dir(modulos[name])
    
'''
for key in modulos.keys():
    print key, modulos[key]'''

### Guardar la lista para autocompletar.
path = os.path.join("/dev/shm", "shelveout")

archivo = shelve.open(path)
archivo["Lista"] = lista
archivo.close()

print path

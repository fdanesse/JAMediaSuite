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
import types

'''
def append_modulo(name):
    """
    Importa un módulo según su nombre y lo
    almacena importado.
    """
    
    try:
        if not modulos.get(name, ""):
            modulos[name] = __import__(str(name), globals(), locals(), [], -1)
            
            arch.write("1- Se importó: %s\n" % str(modulos[name]))
            
    except:
        arch.write("\t1- No se pudo importar: %s\n" % modulos[name])
        
def append_modulo_to_prev(name, prev):
    """
    Importa un módulo que se encuentra dentro de
    un paquete, según su nombre y el nombre
    del paquete que lo contiene y lo almacena importado.
    """
    
    try:
        if not modulos.get(prev, ""):
            append_modulo(prev)
            
        modulos[name] = modulos[prev].__getattribute__(name)
        arch.write("1- Se importó: %s.%s\n" % (str(modulos[prev]), str(modulos[name])))
        
    except:
        arch.write("\t1- No se pudo importar: %s.%s\n" % (str(prev), str(name)))
    
def append_modulo_to_prev_for_path(path):
    """
    Importa los módulos necesarios segun path y lo almacena.
    """
    
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
                    
                    arch.write("4- Se importó: %s\n" % (str(modulos[prev])))
                    
    except:
        arch.write("\t4- No se pudo importar: %s\n" % (str(modulos[prev])))'''

def evaluar_import(im):
    
    if "from" in im:
        if "gi.repository" in im and not " as " in im and not "*" in im:
            return 0
        
        elif "." in im and not " as " in im and not "*" in im:
            # from JAMedia.JAMedia import JAMediaPlayer, otros . . .
            return 1
        
        elif not "." in im and not " as " in im and not "*" in im:
            # from JAMedia import JAMediaPlayer, otros . . .
            return 2
        
    else:
        if not "." in im and not " as " in im and not "*" in im:
            # import os, sys, commands
            return 3
        
        """
        FIXME: recordar caso: import gi.repository - import gi.repository.Gtk
        
        elif "." in im and " as " in im and not "*" in im:
            # import JAMediaObjects.JAMediaGstreamer as G
            return 2
        
        elif "." in im and not " as " in im and "*" in im:
            # import JAMediaObjects.JAMediaGstreamer import uno, dos
            return 3
        """

"""
Comienzo del Análisis.
"""

lista = []

arch = open("/tmp/JAMediaEditorLog.txt", "w") ### LOG

### Obtener los datos para hacer autocompletado.
path = os.path.join(sys.argv[1])
basepath = sys.argv[2]

if basepath:
    if os.path.exists(basepath):
        arch.write("Cambiando a Directorio: %s\n" % str(basepath))
        os.chdir(basepath) # Importante para paquetes personalizados

archivo = shelve.open(path)
lista = archivo["Lista"]
archivo.close()

imports = lista[:-1]
linea_activa = lista[-1]

arch.write("Imports:\n")
for imp in imports:
    arch.write("\t%s\n" % str(imp))
arch.write("AutoCompletando Sobre: %s\n" % str(linea_activa))

### Hacer importaciones previas.
modulos = {}

for im in imports:
    
    valor = evaluar_import(im)

    if valor == 0:
        #arch.write("0- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()
        prev = temp_list[1]
        mod_temp_list = temp_list[3:]
        
        for name in mod_temp_list:
            name = name.replace(",", "").strip()
            
            try:
                mod = __import__("%s.%s" % (prev, name))
                #modulos[name] = mod.importer.modules.get(name)
                modulos[name] = dir(mod.importer.modules.get(name))
                #arch.write("0- Módulo Importado: %s\n" % str(mod))
                
            except:
                arch.write("\t\t0- No se pudo Cargar: %s\n" % str(mod))
                
    elif valor == 1:
        #arch.write("1- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()
        prev = temp_list[1]
        temp_list = temp_list[3:]
    
        for item in temp_list:
            name = item.replace(",", "").strip()
            modulos[name] = []
            
            try:
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
                
            except:
                # FIXME: caso: JAMediaObjects.JAMediaGstreamer.JAMediaBins JAMedia_Efecto_bin
                # La solucion parece ser copiar el instrospector a ese directorio y hacer el import allí.
                # Esto además cambiará el caso de importacion actual, ya que sería: from JAMediaBins JAMedia_Efecto_bin
                arch.write("\t\t1- No se pudo importar: %s %s\n" % (str(prev), str(name)))
                
    elif valor == 2:
        #arch.write("2- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()
        prev = temp_list[1]
        temp_list = temp_list[3:]
    
        for item in temp_list:
            name = item.replace(",", "").strip()
            modulos[name] = []
            
            try:
                mod = __import__("%s.%s" % (prev, name))
                modulos[name] = dir(mod)
                
            except:
                # FIXME: caso: JAMediaObjects.JAMediaGstreamer.JAMediaBins JAMedia_Efecto_bin
                # La solucion parece ser copiar el instrospector a ese directorio y hacer el import allí.
                # Esto además cambiará el caso de importacion actual, ya que sería: from JAMediaBins JAMedia_Efecto_bin
                arch.write("\t\t2- No se pudo importar: %s %s\n" % (str(prev), str(name)))
                
    elif valor == 3:
        #arch.write("3- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()
        #prev = temp_list[1]
        mod_temp_list = temp_list[1:]
        
        for name in mod_temp_list:
            name = name.replace(",", "").strip()
            
            try:
                mod = __import__("%s" % name)
                modulos[name] = dir(mod)
                
                arch.write("\t3- Se importó: %s\n" % str(mod))
                
            except:
                arch.write("\t\t3- No se pudo importar: %s\n" % str(name))
                
'''
    if not "from " in im and not " *" in im and not " as" in im:
        """
        Funciona para:
            import os
            import os, sys, commands
        """
        
        arch.write("0- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()[1:]          # quitando "import" y separando los módulos
        
        for item in temp_list:
            name = item.replace(",", "")    # quitando ","
            name = name.strip()
            arch.write("0- Intentando importar: %s\n" % str(name))
            append_modulo(name)             # importar y almacenar
    
    elif "from " in im and not " *" in im and not "." in im and not " as" in im:
        """
        Funciona para:
            from os import path
            from os import path, chmod
        """
        
        arch.write("0- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()
        prev = temp_list[1]
        temp_list = temp_list[3:]
        
        for item in temp_list:
            name = item.replace(",", "")
            name = name.strip()
            append_modulo_to_prev(name, prev)
            
    ### caso 3: from Coso.Ventana import JAMediaPlayer
    ### Caso Especial: from Coso.Ventana.Otro import JAMediaPlayer, OtraCosa, ...
    elif "from " in im and not " *" in im and "." in im and not " as" in im:
        
        arch.write("0- Intentando importar: %s\n" % str(im))
        
        temp_list = im.split()
        prev = temp_list[1]
        mod_temp_list = temp_list[3:]
        
        if len(prev.split(".")) < 3: # FIXME la funcion falla para caso especial
            ### Caso Especial: módulos de pygi.
            if "gi.repository" in prev:
                arch.write("***: %s\n" % (str(prev)))
                name = mod_temp_list[0]
                mod = __import__("%s.%s" % (prev, name))
                modulos[name] = mod.importer.modules.get(name)
                
            else:
                append_modulo_to_prev_for_path(prev)
                
                for item in mod_temp_list:
                    name = item.replace(",", "")
                    name = name.strip()
                    append_modulo_to_prev(name, prev)
                    arch.write("###: %s.%s\n" % (str(prev), str(name)))
                    
    """
    ### Caso 1: import os
    ### Caso Especial: from os import *
    elif "from " in im and " *" in im and not " as" in im:
        pass
    
    ### Caso 2: from os import path
    ### Caso Especial: from os import *
    elif "from " in im and " *" in im and not "." in im and not " as" in im:
        pass # http://stackoverflow.com/questions/2916374/how-to-import-with-import
    """
'''



# FIXME: Requiere análisis de casos especiales.

if len(linea_activa) == 1:
    name = linea_activa[0]
    #lista = dir(modulos[name])
    lista = modulos.get(name, [])
    
else:
    arch.write("!!!  linea_activa != 1\n")
    
arch.write("Lista: %s\n" % (str(lista)))

### Guardar la lista para autocompletar.
path = os.path.join("/dev/shm", "shelveout")

archivo = shelve.open(path)
archivo["Lista"] = lista
archivo.close()

arch.close()

print path

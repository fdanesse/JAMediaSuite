#!/usr/bin/env python
# -*- coding: utf-8 -*-

import commands

def get_inspect(elemento):
    """Devuelve inspect de elemento."""
    
    return commands.getoutput('gst-inspect-1.0 %s' % (elemento))

def get_gst_elements():
    """Devulve la lista de elementos
    Gstreamer instalados en el sistema."""
    
    returndata = []
    
    inspect = commands.getoutput('gst-inspect-1.0')
    elementos = inspect.split('\n')
    
    for elemento in elementos:
        partes = elemento.split(':')
        
        if len(partes) == 5:
            returndata.append(partes)
            
        else:
            while len(partes) < 5:
                partes.append('')
            returndata.append(partes)
            
    return returndata

elementos = get_gst_elements()

# clase, nombre, paquete al que pertenece
# Visualizadores de Audio
print "\n*** Visualizadores de Audio ***"
for elemento in elementos:
    datos = get_inspect(elemento[1])
    if 'Visualization' in datos and 'gst-plugins-good' in datos: # puedes agregar por ejemplo: 'gst-plugins-good'
        print "\t%s" % (elemento) # Para obtener solo lista de nombres: print "\t%s" % (elemento[1])
'''
# clase, nombre, paquete al que pertenece
# Efectos y Transformaciones sobre Video
print "\n*** Efectos y Transformaciones sobre Video ***"
for elemento in elementos:
    datos = get_inspect(elemento[1])
    if 'Filter/Effect/Video' in datos or 'Transform/Effect/Video' in datos: # puedes agregar por ejemplo: 'gst-plugins-good'
        print "\t%s" % (elemento) # Para obtener solo lista de nombres: print "\t%s" % (elemento[1])'''
        
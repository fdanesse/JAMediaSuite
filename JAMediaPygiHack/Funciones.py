#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Funciones.py por:
#   Flavio Danesse <fdanesse@activitycentral.com>
#   CeibalJAM - Uruguay - Activity Central

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

# http://docs.python.org/library/functions.html?highlight=isinstance#isinstance
# http://docs.python.org/library/functions.html?highlight=__import__#__import__
# http://docs.python.org/library/modules.html?highlight=__import__
# http://docs.python.org/library/modulefinder.html
# http://docs.python.org/library/pydoc.html?highlight=pydoc#pydoc
# http://hg.python.org/cpython/file/2.7/Lib/pydoc.py
# http://docs.python.org/library/imp.html

# FIXME: Analizar la posibilidad de usar: self.__gdoc__

# http://www.roojs.org/seed/gir-1.1-gtk-2.0/
PaquetesObjetos1 = [
    'Atk',
    'Unity',
    'Gedit',
    'Atspi',
    'Avahi',
    'Clutter',
    'ClutterJson',
    'DBusGLib',
    'Epiphany',
    'Everything',
    'GConf',
    'GIMarshallingTests',
    'GIRepository',
    'GLib',
    'GObject',
    'GSSDP',
    'GUPnP',
    'Gda',
    'Gdaui',
    'Gdk',
    'GdkPixbuf',
    'Gio',
    'Gladeui',
    'GnomeVFS',
    'GooCanvas',
    'Gsf',
    'Gst',
    'GstApp',
    'GstAudio',
    'GstBase',
    'GstController',
    'GstInterfaces',
    'GstNet',
    'GstRtp',
    'GstTag',
    'GstVideo',
    'Gtk',
    'GtkClutter',
    'GtkSource',
    'Midgard',
    'Notify',
    'PanelApplet',
    'Pango',
    'PangoCairo',
    'PangoFT2',
    'PangoXft',
    'Peas',
    'PeasUI',
    'Polkit',
    'Poppler',
    'Soup',
    'SoupGNOME',
    'TelepathyGLib',
    'Unique',
    'Vte',
    'WebKit']

PaquetesNoObjetos1 = [
    'AvahiCore',
    'Babl',
    'Cogl',
    'DBus',
    'GL',
    'GMenu',
    'GModule',
    'GnomeKeyring',
    'GstCheck',
    'GstFft',
    'GstNetbuffer',
    'GstPbutils',
    'GstRiff',
    'GstRtsp',
    'GstSdp',
    'Gtop',
    'JSCore',
    'PangoX',
    'cairo',
    'fontconfig',
    'freetype2',
    'libbonobo',
    'libc',
    'libxml2',
    'sqlite3',
    'xfixes',
    'xft',
    'xlib',
    'xrandr']

# http://www.roojs.com/seed/gir-1.2-gtk-3.0/seed/
PaquetesObjetos2 = [
    'AccountsService',
    'Atk',
    'Cally',
    'Champlain',
    'Clutter',
    'ClutterGst',
    'ClutterX11',
    'DBusGLib',
    'Dbusmenu',
    'Dee',
    'EvinceDocument',
    'Wnck',
    'Totem',
    'Abi',
    'EvinceView',
    'GConf',
    'GIRepository',
    'GLib',
    'GObject',
    'GWeather',
    'Gdk',
    'GdkPixbuf',
    'GdkX11',
    'Gio',
    'Gkbd',
    'GnomeBluetooth',
    'Gtk',
    'GtkChamplain',
    'GtkClutter',
    'GtkSource',
    'Gucharmap',
    'Json',
    'MPID',
    'Nautilus',
    'Notify',
    'Pango',
    'PangoCairo',
    'PangoFT2',
    'PangoXft',
    'Peas',
    'PeasGtk',
    'Polkit',
    'PolkitAgent',
    'Soup',
    'SoupGNOME',
    'TelepathyGLib',
    'TelepathyLogger',
    'UPowerGlib',
    'Vte',
    'WebKit',
    'GES',
    'NetworkManager',
    'Rsvg',
    'SugarExt',
    'Cheese']

# GES : http://gstreamer.freedesktop.org/data/doc/gstreamer/head/gstreamer-editing-services/html/
PaquetesNoObjetos2 = [
    'Cogl',
    'DBus',
    'GL',
    'GMenu',
    'GModule',
    'JSCore',
    'cairo',
    'fontconfig',
    'freetype2',
    'libxml2',
    'xfixes',
    'xft',
    'xlib',
    'xrandr']

pygi = __import__("gi.repository")

import gi.types
import types

def get_info(modulo_name):
    """
    Devuelve las clases, funciones y constantes de
    un modulo determinado en un paquete dado.
    """
    
    CONSTANTES = []
    DESCONOCIDOS = []
    FUNCIONES = []
    CLASES = []
    
    modulo = False
    
    try:
        modulo = pygi.module.IntrospectionModule(modulo_name)
        
    except:
        return [False, False, False, False, False]
    
    if not modulo or modulo == None:
        return [False, False, False, False, False]

    attr = None
    
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
            ### Formar lista de "no atributos" del modulo
            try:
                attr = getattr(modulo, func)
                
            except:
                DESCONOCIDOS.append(func)
                continue

            ### Ejemplo: Gtk.Window
            objeto = "%s.%s" % (modulo_name, func)
            try:
                if isinstance(attr, type):
                    mod = __import__("%s.%s" % ("gi.repository", modulo_name))
                    new = mod.importer.modules.get(modulo_name)
                    clase = getattr(new, func)
                    CLASES.append( (objeto, attr, clase.__gdoc__) ) # La Clase
                    continue
                    
                elif isinstance(attr, types.FunctionType):
                    FUNCIONES.append( (objeto, attr) ) # La Función
                    continue
                
                else:
                    CONSTANTES.append( (objeto, attr) ) # La Constante
                    continue
                
            except:
                pass
        
    return [modulo, CLASES, FUNCIONES, CONSTANTES, DESCONOCIDOS]

def get_modulos():
    """
    Devuelve la lista de paquetes gi que
    se encuentra en el sistema.
    """
    
    modulos = []
    
    for paquete in PaquetesObjetos1 + PaquetesNoObjetos1 + PaquetesObjetos2 + PaquetesNoObjetos2:
        
        if not paquete in modulos:
            
            modulo = False
            
            try:
                modulo = pygi.module.IntrospectionModule(paquete)
        
            except:
                pass
            
            if modulo and modulo != None:
                modulos.append(paquete)
            
    modulos.sort()
    
    return modulos

''' Pa no olvidarme:
g = __import__( 'gi.repository.Gtk' )
Gtk=g.importer.modules.get('Gtk')

In [18]: g = __import__( 'gi.repository')
In [19]: Gtk=g.importer.modules.get('Gtk')
# print gtk.Window._doc_

In [55]: x=g.importer.repository.get_typelib_path('GLib')
In [56]: x
Out[56]: '/usr/lib/girepository-1.0/GLib-2.0.typelib'

#Buscando las librerias:
    m = __import__("gi.repository")
    path = m.importer.repository.get_typelib_path('GdkPixbuf')
    
# Introspeccion:
m = __import__("gi.repository")
i=m.module.IntrospectionModule('GdkPixbuf')
'''
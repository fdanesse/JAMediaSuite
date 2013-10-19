#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Globales.py por:
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

import os

BASEPATH = os.path.dirname(__file__)
WorkPath = os.environ["HOME"]

BASEDICT = {
    "python": [
        'cairo', 'commands', 'gobject', 'gst', 'json',
        'os', 'pygame', 'pygst', 'shelve', 'simplejson',
        'sys', 'gtk', 'pygtk'],
    "python-gi": [
        'Abi', 'AccountsService', 'Atk', 'Atspi',
        'Avahi', 'AvahiCore', 'Babl', 'Cally',
        'Champlain', 'Cheese', 'Clutter', 'ClutterGst',
        'ClutterJson', 'ClutterX11', 'Cogl', 'DBus',
        'DBusGLib', 'Dbusmenu', 'Dee', 'Epiphany', 'Everything',
        'EvinceDocument', 'EvinceView', 'GConf', 'GES',
        'GIMarshallingTests', 'GIRepository', 'GL', 'GLib',
        'GMenu', 'GModule', 'GObject', 'GSSDP', 'GUPnP',
        'GWeather', 'Gda', 'Gdaui', 'Gdk', 'GdkPixbuf',
        'GdkX11', 'Gedit', 'Gio', 'Gkbd', 'Gladeui',
        'GnomeBluetooth', 'GnomeKeyring', 'GnomeVFS',
        'GooCanvas', 'Gsf', 'Gst', 'GstApp', 'GstAudio',
        'GstBase', 'GstCheck', 'GstController', 'GstFft',
        'GstInterfaces', 'GstNet', 'GstNetbuffer', 'GstPbutils',
        'GstRiff', 'GstRtp', 'GstRtsp', 'GstSdp', 'GstTag',
        'GstVideo', 'Gtk', 'GtkChamplain', 'GtkClutter',
        'GtkSource', 'Gtop', 'Gucharmap', 'JSCore', 'Json',
        'MPID', 'Midgard', 'Nautilus', 'NetworkManager',
        'Notify', 'PanelApplet', 'Pango', 'PangoCairo',
        'PangoFT2', 'PangoX', 'PangoXft', 'Peas', 'PeasGtk',
        'PeasUI', 'Polkit', 'PolkitAgent', 'Poppler', 'Rsvg',
        'Soup', 'SoupGNOME', 'SugarExt', 'TelepathyGLib',
        'TelepathyLogger', 'Totem', 'UPowerGlib', 'Unique',
        'Unity', 'Vte', 'WebKit', 'Wnck', 'cairo', 'fontconfig',
        'freetype2', 'libbonobo', 'libc', 'libxml2', 'sqlite3',
        'xfixes', 'xft', 'xlib', 'xrandr'],
    "Otros":[],
        }
    
def set_dict(dict):
    """
    Crea el json base desde donde opera
    la función get_dict()
    """
    
    import json
    
    archivo = os.path.join(WorkPath, "JAMediaPyGiHack.cfg")
    archivo = open(archivo, "w")
    archivo.write(
            json.dumps(
                dict,
                indent=4,
                separators=(", ", ":"),
                sort_keys=True
            )
        )
    archivo.close()
    
def get_dict():
    """
    Devuelve Los módulos disponibles
    para cargar en el menu de la aplicación.
    """
    
    import json
    import codecs
    import commands
    
    archivo = os.path.join(WorkPath, "JAMediaPyGiHack.cfg")
    
    if not os.path.exists(archivo):
        set_dict(BASEDICT)
        
    archivo = codecs.open(archivo, "r", "utf-8")
    dict = json.JSONDecoder("utf-8").decode(archivo.read())
    
    disponibles = []
    for item in dict["python-gi"]:
        ejecutable = os.path.join(BASEPATH, "SpyderHack", "Gi_Check.py")
        ret = commands.getoutput('python %s %s' % (ejecutable, item))
        if str(True) in ret:
            disponibles.append(item)
        else:
            print item, "No se encuentra en el sistema", ret, type(ret)
    dict["python-gi"] = sorted(disponibles)
    
    disponibles = []
    for item in dict["python"]:
        ejecutable = os.path.join(BASEPATH, "SpyderHack", "Check.py")
        ret = commands.getoutput('python %s %s' % (ejecutable, item))
        if str(True) in ret:
            disponibles.append(item)
        else:
            print item, "No se encuentra en el sistema", ret, type(ret)
    dict["python"] = sorted(disponibles)
    
    return dict

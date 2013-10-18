#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   JAMediaPygiHack.py por:
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

from gi.repository import Gtk
from gi.repository import Gdk

import JAMediaObjects
JAMediaObjectsPath = JAMediaObjects.__path__[0]

from JAMediaPygiHack.Widgets import Toolbar
from JAMediaPygiHack.BasePanel import BasePanel

'''
screen = Gdk.Screen.get_default()
css_provider = Gtk.CssProvider()

style_path = os.path.join(
    BASEPATH, "JAMediaPygiHack.css")
    
css_provider.load_from_path(style_path)
context = Gtk.StyleContext()

context.add_provider_for_screen(
    screen,
    css_provider,
    Gtk.STYLE_PROVIDER_PRIORITY_USER)
'''

class Ventana(Gtk.Window):
    
    __gtype_name__ = 'JAMediaPygiHAck'
    
    def __init__(self):
        
        Gtk.Window.__init__(self)
        
        self.set_title("JAMediaPygiHAck")
        
        self.set_icon_from_file(
            os.path.join(JAMediaObjectsPath,
            "Iconos", "PygiHack.svg"))
            
        self.set_resizable(True)
        self.set_size_request(640, 480)
        self.maximize()
        self.set_border_width(2)
        self.set_position(Gtk.WindowPosition.CENTER)
        
        vbox = Gtk.Box(orientation = Gtk.Orientation.VERTICAL)
        self.add(vbox)
        
        toolbar = Toolbar()
        toolbar.connect("import", self.__import)
        toolbar.connect("accion-menu", self.__set_accion)
        vbox.pack_start(toolbar, False, False, 0)
        
        self.base_panel = BasePanel()
        vbox.pack_start(self.base_panel, True, True, 0)
        
        self.show_all()
        self.realize()

        self.connect("delete-event", self.__salir)
        
    def __set_accion(self, widget, menu, wid_lab, valor):
        
        self.base_panel.set_accion(menu, wid_lab, valor)
        
    def __import(self, widget, paquete, modulo):
        
        self.base_panel.import_modulo(paquete, modulo)

    def __salir(self, widget = None, senial = None):
        
        import sys
        sys.exit(0)

if __name__ == "__main__":
    Ventana()
    Gtk.main()

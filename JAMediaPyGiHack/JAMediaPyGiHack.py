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

from Widgets import Toolbar
from BasePanel import BasePanel

class JAMediaPyGiHack(Gtk.Box):
    
    #__gtype_name__ = 'JAMediaPyGiHack'
    
    def __init__(self):
        
        Gtk.Box.__init__(self, orientation = Gtk.Orientation.VERTICAL)
        
        self.toolbar = Toolbar()
        self.pack_start(self.toolbar, False, False, 0)
        
        self.base_panel = BasePanel()
        self.pack_start(self.base_panel, True, True, 0)
        
        self.show_all()

        self.toolbar.connect("import", self.__import)
        self.toolbar.connect("accion-menu", self.__set_accion)
        self.base_panel.connect("update", self.__update)
        
    def __update(self, widget, view):
        
        if view == "Terminal":
            pass
        
        elif view == "Gstreamer - Inspect 1.0" or \
            view == "Apis PyGiHack":
            self.toolbar.update(view)
        
    def __set_accion(self, widget, menu, wid_lab, valor):
        
        self.base_panel.set_accion(menu, wid_lab, valor)
        
    def __import(self, widget, paquete, modulo):
        
        self.base_panel.import_modulo(paquete, modulo)
        